import sys
from pathlib import Path

def get_constants(repo: str):

    # Get path to repo where Constants.py lives.
    home = str(Path.home())
    repo_path = home + f"/repos/{repo}"

    # Dynamically reference repo in order to point to relevant Constants.py file.
    sys.path.insert(0, repo_path)
    import Constants

    return Constants