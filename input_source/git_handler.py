import logging
import git
from tempfile import mkdtemp

# Configure logging to show debug messages
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def clone_repo(repo_url: str) -> str:
    """
    Clones a Git repository from a given URL into a temporary directory.
    Automatically adds .git suffix if missing.

    Args:
        repo_url (str): The URL of the Git repository to clone.

    Returns:
        str: The path to the temporary directory where the repo was cloned.
             Returns an empty string if cloning fails.
    """
    try:
        # Append .git if not present
        if not repo_url.endswith(".git"):
            repo_url += ".git"

        # Create a temporary directory to clone the repository into
        temp_dir = mkdtemp()
        logging.info(f"Cloning repository from {repo_url} into {temp_dir}")

        # Clone the repository
        git.Repo.clone_from(repo_url, temp_dir)

        logging.info(f"Successfully cloned repository into {temp_dir}")
        return temp_dir

    except git.exc.GitCommandError as e:
        logging.error(f"Error cloning repository: {e}")
        return ""