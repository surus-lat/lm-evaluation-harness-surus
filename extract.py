from pathlib import Path
import shutil

laliga_tasks = Path("laliga/lm-evaluation-harness/lm_eval/tasks")
laliga_task_folders = [f for f in laliga_tasks.iterdir() if f.is_dir()]
laliga_task_folders_names = [f.name for f in laliga_task_folders]


repo_tasks = Path("lm_eval/tasks")
repo_task_folders = [f for f in repo_tasks.iterdir() if f.is_dir()]
repo_task_folders_names = [f.name for f in repo_task_folders]

unique_laliga_names = [f for f in laliga_task_folders_names if f not in repo_task_folders_names]
unique_laliga_folders = [f for f in laliga_task_folders if f.name in unique_laliga_names]

print(unique_laliga_folders)

export_tasks = Path("lm-evaluation-harness/exported_tasks")
export_tasks.mkdir(parents=True, exist_ok=True)
for folder in unique_laliga_folders:
    print(f"Exporting {folder.name}"	)
    shutil.copytree(folder, export_tasks / folder.name)
