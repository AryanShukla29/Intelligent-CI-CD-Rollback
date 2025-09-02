import os
import subprocess
import logging
from datetime import datetime
 
# Setup logging
logging.basicConfig(
    filename="rollback.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
 
class RollbackManager:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
 
    def run_command(self, command: str) -> str:
        """Run shell commands safely and return output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.repo_path,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed: {command}\nError: {e.stderr}")
            return None
 
    def get_last_commit(self) -> str:
        """Fetch the last commit hash"""
        return self.run_command("git rev-parse HEAD")
 
    def get_previous_commit(self) -> str:
        """Fetch the previous commit hash"""
        return self.run_command("git rev-parse HEAD~1")
 
    def rollback_to_previous_commit(self) -> bool:
        """Rollback to previous commit"""
        prev_commit = self.get_previous_commit()
        if not prev_commit:
            logging.error("No previous commit found!")
            return False
 
        logging.info(f"Rolling back to commit: {prev_commit}")
        result = self.run_command(f"git reset --hard {prev_commit}")
        if result is not None:
            logging.info("Rollback successful.")
            return True
        return False
 
    def record_rollback(self):
        """Record rollback details"""
        commit = self.get_last_commit()
        with open("rollback_history.txt", "a") as f:
            f.write(f"{datetime.now()} - Rolled back to {commit}\n")
        logging.info(f"Rollback recorded: {commit}")