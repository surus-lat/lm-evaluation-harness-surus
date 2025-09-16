#!/usr/bin/env python3
"""
Model download and test script for lm-evaluation-harness.

This script downloads a model and runs a simple test to ensure it's working correctly.
It mimics the model loading process used by lm_eval but with minimal overhead.
"""

import argparse
import sys
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_model_args(model_args_str: str) -> dict:
    """Parse model arguments string into dictionary."""
    args_dict = {}
    if not model_args_str:
        return args_dict
    
    for arg in model_args_str.split(','):
        if '=' in arg:
            key, value = arg.split('=', 1)
            args_dict[key.strip()] = value.strip()
    
    return args_dict


def test_model(model_name: str, model_args_str: str = "", use_accelerate: bool = False, 
               num_gpus: int = 1, mixed_precision: str = "no") -> dict:
    """
    Download and test a model to ensure it's working correctly.
    
    Args:
        model_name: The model name/path to test
        model_args_str: Model arguments as comma-separated string
        use_accelerate: Whether accelerate will be used (affects device placement)
        num_gpus: Number of GPUs that will be used
        mixed_precision: Mixed precision mode
        
    Returns:
        Dictionary with test results
    """
    logger.info(f"Starting model test for: {model_name}")
    
    # Parse model arguments
    model_args = parse_model_args(model_args_str)
    logger.info(f"Model args: {model_args}")
    
    try:
        # Extract relevant arguments (ignore VLLM-specific args)
        pretrained = model_args.get('pretrained', model_name)
        dtype = model_args.get('dtype', 'auto')
        max_length = model_args.get('max_length')
        
        # Ignore VLLM-specific arguments that don't apply to HF transformers testing
        vllm_args = ['tensor_parallel_size', 'gpu_memory_utilization', 'data_parallel_size', 'max_model_len', 'enforce_eager', 'limit_mm_per_prompt']
        if any(arg in model_args for arg in vllm_args):
            logger.info("VLLM-specific arguments detected in model_args - these will be ignored for testing")
            logger.info("Test will use basic HuggingFace transformers for model validation")
        
        logger.info(f"Loading tokenizer for: {pretrained}")
        
        # Load tokenizer first (this will download if needed)
        tokenizer_kwargs = {
            'trust_remote_code': True
        }
        
        # Only add token if it exists
        hf_token = os.environ.get('HF_TOKEN')
        if hf_token:
            tokenizer_kwargs['token'] = hf_token
            
        tokenizer = AutoTokenizer.from_pretrained(pretrained, **tokenizer_kwargs)
        
        logger.info("Tokenizer loaded successfully")
        
        # Configure dtype
        torch_dtype = None
        if dtype == 'float16':
            torch_dtype = torch.float16
        elif dtype == 'bfloat16':
            torch_dtype = torch.bfloat16
        elif dtype == 'float32':
            torch_dtype = torch.float32
        elif dtype == 'auto':
            # For 'auto', let transformers decide (usually defaults to model's native dtype)
            torch_dtype = None
            logger.info("dtype=auto detected, letting transformers auto-detect dtype")
        else:
            logger.warning(f"Unknown dtype: {dtype}, using auto")
            torch_dtype = None
        
        # Determine device strategy
        if use_accelerate and num_gpus > 1:
            # For multi-GPU testing, just use a single GPU to avoid complexity
            # The actual evaluation will use accelerate properly
            device_map = None
            device = "cuda:0"
            logger.info(f"Multi-GPU mode detected, but using single GPU for testing: {device}")
            logger.info(f"(Actual evaluation will use {num_gpus} GPUs with accelerate)")
        elif torch.cuda.is_available():
            # Single GPU mode
            device_map = None
            device = "cuda:0"
            logger.info(f"Single GPU mode: {device}")
        else:
            # CPU mode
            device_map = None
            device = "cpu"
            logger.info("CPU mode")
        
        logger.info(f"Loading model: {pretrained}")
        
        # Load model with appropriate configuration
        model_kwargs = {
            'trust_remote_code': True
        }
        
        # Only add token if it exists
        if hf_token:
            model_kwargs['token'] = hf_token
        
        if torch_dtype is not None:
            model_kwargs['torch_dtype'] = torch_dtype
            
        if device_map is not None:
            model_kwargs['device_map'] = device_map
        else:
            model_kwargs['device_map'] = None
            
        # Load model with error handling for OOM
        try:
            model = AutoModelForCausalLM.from_pretrained(pretrained, **model_kwargs)
            
            if device is not None and device_map is None:
                model = model.to(device)
                
        except (torch.cuda.OutOfMemoryError, RuntimeError) as oom_error:
            if "out of memory" in str(oom_error).lower() and device != "cpu":
                logger.warning(f"CUDA OOM during model loading: {oom_error}")
                logger.info("Falling back to CPU mode for testing...")
                
                # Clear GPU memory
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                # Retry with CPU
                model_kwargs_cpu = model_kwargs.copy()
                model_kwargs_cpu['device_map'] = None
                if 'torch_dtype' in model_kwargs_cpu:
                    # Use float32 for CPU to avoid potential issues
                    model_kwargs_cpu['torch_dtype'] = torch.float32
                
                model = AutoModelForCausalLM.from_pretrained(pretrained, **model_kwargs_cpu)
                model = model.to("cpu")
                device = "cpu"
                logger.info("Successfully loaded model on CPU for testing")
            else:
                raise
            
        logger.info("Model loaded successfully")
        
        # Run a simple test generation
        test_prompt = "Hello, world! This is a test."
        logger.info(f"Testing with prompt: '{test_prompt}'")
        
        # Tokenize
        inputs = tokenizer(test_prompt, return_tensors="pt")
        
        # Move inputs to same device as model
        if device is not None:
            inputs = {k: v.to(device) for k, v in inputs.items()}
        elif hasattr(model, 'device'):
            inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # Generate
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=10,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode output
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"Generated text: '{generated_text}'")
        
        # Get model info
        num_parameters = sum(p.numel() for p in model.parameters())
        model_size_gb = num_parameters * 4 / (1024**3)  # Assuming float32
        
        logger.info(f"Model parameters: {num_parameters:,}")
        logger.info(f"Estimated size: {model_size_gb:.2f} GB")
        
        # Cleanup
        del model
        del tokenizer
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        logger.info("Model test completed successfully!")
        
        return {
            "status": "success",
            "model_name": model_name,
            "pretrained": pretrained,
            "num_parameters": num_parameters,
            "model_size_gb": model_size_gb,
            "test_prompt": test_prompt,
            "generated_text": generated_text,
            "device_strategy": "multi_gpu_accelerate" if (use_accelerate and num_gpus > 1) else ("single_gpu" if device.startswith("cuda") else "cpu")
        }
        
    except Exception as e:
        logger.error(f"Model test failed: {str(e)}")
        return {
            "status": "failed",
            "model_name": model_name,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description="Test model download and basic inference")
    parser.add_argument("--model_name", required=True, help="Model name to test")
    parser.add_argument("--model_args", default="", help="Model arguments as comma-separated string")
    parser.add_argument("--use_accelerate", action="store_true", help="Whether accelerate will be used")
    parser.add_argument("--num_gpus", type=int, default=1, help="Number of GPUs that will be used")
    parser.add_argument("--mixed_precision", default="no", choices=["no", "fp16", "bf16"], 
                       help="Mixed precision mode")
    # VLLM parameters (ignored for testing - we just test basic model loading)
    parser.add_argument("--use_vllm", action="store_true", help="Whether VLLM will be used (ignored for testing)")
    parser.add_argument("--gpus_per_model", type=int, default=1, help="GPUs per model for VLLM (ignored for testing)")
    parser.add_argument("--model_replicas", type=int, default=2, help="Model replicas for VLLM (ignored for testing)")
    
    args = parser.parse_args()
    
    result = test_model(
        model_name=args.model_name,
        model_args_str=args.model_args,
        use_accelerate=args.use_accelerate,
        num_gpus=args.num_gpus,
        mixed_precision=args.mixed_precision
    )
    
    if result["status"] == "success":
        print(f"✅ Model test successful: {result['model_name']}")
        print(f"   Parameters: {result['num_parameters']:,}")
        print(f"   Size: {result['model_size_gb']:.2f} GB")
        print(f"   Generated: {result['generated_text']}")
        sys.exit(0)
    else:
        print(f"❌ Model test failed: {result['model_name']}")
        print(f"   Error: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
