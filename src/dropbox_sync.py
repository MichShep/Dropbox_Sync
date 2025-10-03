#!/usr/bin/env python3

import cmd_arguments
import input_folder
import dbx_api

if __name__ == "__main__":
    # Take in args
    user_folder_path, options = cmd_arguments.get_args()

    # Recursively go though and map of files
    usr_files = input_folder.create_file_list(user_folder_path, options["flat"])

    # Load Dropbox Api
    dbx = dbx_api.load_dbx_api()

    # Compare files in input dir to GRL files
    dbx_api.update_local_dir(dbx, options, user_folder_path, usr_files)
