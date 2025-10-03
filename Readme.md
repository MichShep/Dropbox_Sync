# 📦 Dropbox Sync Tool 📁

A Python script to synchronize a local folder with a Dropbox folder.
It recursively checks for files/folders in Dropbox and download any missing items to your local machine, with options for filtering, logging, and simulation.

---

## Features
- Recursive sync from Dropbox to local folder
- Skip specific file types
- Flat download option (no subfolders)
- Dry-run mode (simulate without downloading)
- Random sampling of files
- Terminal and file logging
- Configurable via `.env`

---

## Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/yourusername/dropbox_sync.git
cd dropbox_sync
pip install -r requirements.txt
```

## Setup
Create a `.env` file in the project root with your Dropbox API token:
```bash
DROPBOX_TOKEN=access_token_here
```
You can generate one by going here: https://www.dropbox.com/developers/apps and following their guides.

## Usage
To use the script run `./dropbox_sync` in  `src`  and provide the following command line arguments:

| Flag              | Type        | Default      | Description                                                          |
|-------------------|-------------|--------------|----------------------------------------------------------------------|
| `-p`, `--path`    | `str`       | **required** | Path to the output folder where files will be synced.                |
| `-r`, `--random`  | `float`     | `1.0`        | Probability of files being downloaded (0.0–1.0].                     |
| `-o`, `--out`     | `flag`      | `False`      | If set, creates an output `.out` listing all newly downloaded files. |
| `-l`, `--log`     | `flag`      | `False`      | If set, logs downloaded files to the terminal.                       |
| `-f`, `--flat`    | `flag`      | `False`      | If set, downloads all files into a flat structure (no subfolders).   |
| `-e`, `--exclude` | `list[str]` | `[]`         | List of file extensions to exclude (e.g. `.png .mp4`).               |
| `-d`, `--dry-run` | `flag`      | `False`      | Simulates the sync without downloading any files.                    |

## Examples

```bash
# Normal sync
python src/dropbox_sync.py -p ./files

# Sync but skip .png and .mp4 files
python src/dropbox_sync.py -p ./files -e .png .mp4

# Sync with logging to terminal
python src/dropbox_sync.py -p ./files --log

# Simulate without downloading
python src/dropbox_sync.py -p ./files --dry-run

# Download a flat structure (no subfolders)
python src/dropbox_sync.py -p ./files --flat

# Download files with only 50% probability
python src/dropbox_sync.py -p ./files -r 0.5
```

## Requirements 
- Python 3.9+
- Dependencies
  - dropbox
  - python-dotenv

Install with:
```bash
pip install -r requirements.txt
```