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
        
        print("\nUpdate successful. Output:")
        print(pull_result.stdout)
        
        if pull_result.stderr:
            print("\nAdditional info:")
            print(pull_result.stderr)
        
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"\nError during git pull: {e.stderr}")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    
    return False

def main():
    print("Starting repository update...\n")
    
    success = update_repo_with_branch_handling()
    
    if success:
        print("\n✅ Repository updated successfully")
    else:
        print("\n❌ Failed to update repository")
    
    if sys.platform.startswith('win'):
        input("\nPress Enter to exit...")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()