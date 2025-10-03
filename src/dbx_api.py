import os
import dropbox
import logging
from typing import Any
from dotenv import load_dotenv
import random
from datetime import date

# -------------------------------------------------------------------------
# Context for syncing
# -------------------------------------------------------------------------
class SyncContext:
    def __init__(self, dbx: dropbox.Dropbox, options: dict[str, Any], dest_root: str, user_dat_paths: [str]) -> None:
        self.dbx = dbx
        self.options = options
        self.dest_root = dest_root
        self.user_dat_paths = user_dat_paths
        self.output_txt = ""

# -------------------------------------------------------------------------
# Setup logging and logging colors
# -------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def log_red(message: str) -> None:
    logging.error(f"\033[91m{message}\033[0m")

def log_green(message: str) -> None:
    logging.info(f"\033[92m{message}\033[0m")

def log_blue(message: str) -> None:
    logging.info(f"\033[94m{message}\033[0m")


# -------------------------------------------------------------------------
# Dropbox Authentication
# -------------------------------------------------------------------------
def load_dbx_api() -> dropbox.Dropbox:
    """Load Dropbox API client using token from environment variable"""

    load_dotenv()

    token = os.getenv("DBX_TOKEN")
    if not token:
        raise RuntimeError("Dropbox token not found. Set DBX_TOKEN environment variable.")
    return dropbox.Dropbox(token)

# -------------------------------------------------------------------------
# File Ops
# -------------------------------------------------------------------------
def create_folder(ctx: SyncContext, folder_name: str, src_path: str, depth: int) -> None:
    """Create a folder locally"""
    try:
        os.makedirs(os.path.join(ctx.dest_root, src_path.strip("/"), folder_name), exist_ok=True)
        log_blue(f"Created folder: {folder_name} in {ctx.dest_root}")
        ctx.output_txt += "+d:" + '\t'*depth + f"{folder_name}\n"
    except Exception as err:
        logging.error(f"Failed to create folder {folder_name}: {err}")

def download_file(ctx: SyncContext, src_path: str, depth: int) -> None:
    """Download a file from Dropbox to local directory"""
    try:
        # Load in the file data
        metadata, res = ctx.dbx.files_download(src_path)
        # Create the local path of downloaded file
        local_path = os.path.join(ctx.dest_root, src_path.strip("/")) if not ctx.options["flat"] \
            else f"{ctx.dest_root}/{metadata.name}"
        if not ctx.options["dry-run"]:  # (skip if doing a dry run)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            # Write the file
            with open(local_path, "wb") as f:
                f.write(res.content)

        log_green(f"Downloaded {metadata.name} to {local_path}")
        ctx.output_txt += "+f:" + '\t'*depth + f"{metadata.name}\n"

    except dropbox.exceptions.ApiError as err:
        logging.error(f"Dropbox API error downloading {src_path}: {err}")

# -------------------------------------------------------------------------
# Recursive Sync
# -------------------------------------------------------------------------
def recursive_sync(ctx: SyncContext, src_path: str, depth: int) -> None:
    """Recursively sync Dropbox folder with local directory"""
    try:
        result = ctx.dbx.files_list_folder(src_path)
        for entry in result.entries:
            # Entry is a FILE
            if isinstance(entry, dropbox.files.FileMetadata):
                # Get the path of the file
                dbx_file_path = f"{entry.path_display}" if not ctx.options["flat"] else f"/{entry.name}"
                # Check if the file exists AND if it passes the probability
                if (f"file%{dbx_file_path}" not in ctx.user_dat_paths and
                        random.random() <= ctx.options["random"] and
                        (entry.name.split('.')[-1] not in ctx.options["exclude"] if len(ctx.options["exclude"]) > 0 else True)
                ):
                    # Download the missing file
                    download_file(ctx, entry.path_display, depth)

            # Entry is a FOLDER
            elif isinstance(entry, dropbox.files.FolderMetadata):
                # Get the path to the dir
                dbx_dir_path = f"{entry.path_display}"
                # Check if the dir exists (don't make new one if flat output)
                if f"dir%{dbx_dir_path}" not in ctx.user_dat_paths and not ctx.options["flat"]:
                    # Create the missing dir
                    create_folder(ctx, entry.name, src_path, depth)

                # Recurse inside the directory
                recursive_sync(ctx, entry.path_display, depth + 1)

    except dropbox.exceptions.ApiError as err:
        logging.error(f"Error listing folder {src_path}: {err}")

# -------------------------------------------------------------------------
# Main entry
# -------------------------------------------------------------------------
def update_local_dir(dbx: dropbox.Dropbox, options: dict[str, any], user_dir_path: str, user_dat_paths: [str]) -> None:
    """Update local directory with missing files from Dropbox"""
    # Create sync context
    ctx = SyncContext(dbx, options, user_dir_path, user_dat_paths)

    # Disable logging if wanted
    if not ctx.options["log"]:
        logging.disable(logging.INFO)

    logging.info("Starting Dropbox sync...")

    # Begin recursive walk through the dropbox
    recursive_sync(ctx, "", 0)

    logging.info("Sync completed successfully.")

    if ctx.options["out"]:
        with open(f"{user_dir_path}/dbx_{date.today()}.out", "w") as f:
            f.write(ctx.output_txt)
        print(f"Output written to dbx_{date.today()}.out")