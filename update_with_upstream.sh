#### Manual Sync Commands
# Fetch latest changes from upstream
git fetch upstream

# Switch to main and merge updates
git checkout main
git merge upstream/main

# Push updated main to your fork
git push origin main

# Update our LATAM branch with latest main
git checkout LATAM_leaderboard_v1
git rebase main
git push origin LATAM_leaderboard_v1
