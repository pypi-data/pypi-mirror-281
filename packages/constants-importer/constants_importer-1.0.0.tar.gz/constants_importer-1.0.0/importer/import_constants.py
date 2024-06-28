import sys

from pathlib import Path

def get_constants(repo: str):

    # Get path to platform enablement repo
    home = str(Path.home())
    platform_enablement_repo_path = home + f"/repos/{repo}"

    # Dynamically reference platform enablement repo in order to point to Constants.py
    sys.path.insert(0, platform_enablement_repo_path)
    import Constants

    return Constants