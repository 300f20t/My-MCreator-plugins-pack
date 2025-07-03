import subprocess
import sys
from pathlib import Path

def get_current_branch(repo_path):
    result = subprocess.run(
        ["git", "-C", str(repo_path), "branch", "--show-current"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    return result.stdout.strip()

def update_repo_with_branch_handling(repo_path=None):
    try:
        if repo_path is None:
            repo_path = Path(__file__).parent.resolve()
        
        current_branch = get_current_branch(repo_path)
        if not current_branch:
            print("Error: Unable to determine current branch")
            return False
        
        print(f"Current branch: {current_branch}")
        
        fetch_result = subprocess.run(
            ["git", "-C", str(repo_path), "fetch"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if fetch_result.returncode != 0:
            print("Error during git fetch:")
            print(fetch_result.stderr)
            return False
        
        pull_result = subprocess.run(
            ["git", "-C", str(repo_path), "pull", "origin", current_branch],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        print("Update successful. Output:")
        print(pull_result.stdout)
        
        if pull_result.stderr:
            print("Additional info:")
            print(pull_result.stderr)
        
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error during git pull: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    
    return False

success = update_repo_with_branch_handling()
    
if success:
    print("✅ Repository updated successfully")
    sys.exit(0)
else:
    print("❌ Failed to update repository")
    sys.exit(1)

if sys.platform.startswith('win'):
        input("Press Enter to exit...")
