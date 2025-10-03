import argparse
import os
from typing import Tuple, Any

# -------------------------------------------------------------------------
# Checks for arguments
# -------------------------------------------------------------------------
def check_file(path: str) -> bool:
    """Check if the given path exists"""
    return os.path.exists(path)

# -------------------------------------------------------------------------
# Handler for checking arguments and creation of options
# -------------------------------------------------------------------------
def get_args() -> Tuple[str, dict[str, Any]]:
    """
    Parse command-line arguments for Dropbox sync
    Returns:
        path (str): Path to output folder
        random (Optional[float]): Number of files to randomly sample
        out (bool): Whether to log downloaded files
    """
    parser = argparse.ArgumentParser(
        description="Update a given folder to the current Dropbox data."
    )
    parser.add_argument(
        "-p", "--path",
        required=True,
        type=str,
        help="Path to output folder"
    )
    parser.add_argument(
        "-r", "--random",
        required=False,
        default=1.0,
        type=float,
        help="Probability of files being downloaded (0.0, 1.0]"
    )
    parser.add_argument(
        "-o", "--out",
        action="store_true",
        help="If set, creates output txt of all new files"
    )
    parser.add_argument(
        "-l", "--log",
        action="store_true",
        help="If set, log downloaded files to terminal"
    )
    parser.add_argument(
        "-f", "--flat",
        action="store_true",
        help="If set, download all files with no subfolders"
    )
    parser.add_argument(
        "-e", "--exclude",
        type=str,
        nargs="*",
        default=[],
        help="List of all file types to exclude from download"
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Simulate the sync but won't download files"
    )

    args = parser.parse_args()

    if not check_file(args.path):
        RuntimeError("ERROR: User Folder Not Found!")

    if args.random < 0 or args.random > 1.0:
        RuntimeError("ERROR: Probability needs to be between 0 and 1!")

    options = {}
    options["log"] = args.log
    options["random"] = args.random
    options["dry-run"] = args.dry_run
    options["out"] = args.out
    options["flat"] = args.flat
    options["exclude"] = args.exclude

    return args.path, options
