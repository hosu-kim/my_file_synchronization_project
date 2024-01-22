import os
import sys
import shutil
from time import sleep
from datetime import datetime
from filehash import FileHash
import logging

"""
Please provide command line arguments in this order:
python my_file_sync_tool.py source replica log interval
"""

# assigned input constants
SOURCE_FOLDER_PATH = sys.argv[1]
REPLICA_FOLDER_PATH = sys.argv[2]
LOG_FILE_PATH = sys.argv[3]
INTERVAL = sys.argv[4]
SOURCE_DATA_FOLDER = os.path.basename(sys.argv[1])
REPLICA_DATA_FOLDER = os.path.basename(sys.argv[2])

# inform the assigned input
print(f"\nAssigned Input -"
      f"\nSource Folder Path: {SOURCE_FOLDER_PATH}"
      f"\nReplica Folder Path: {REPLICA_FOLDER_PATH}"
      f"\nLog File Path: {LOG_FILE_PATH}"
      f"\nSync Interval: {INTERVAL} seconds"
      f"\n\n(Ctrl + C) to stop the synchronization.")

for countdown in range(5, 0, -1):
    print(f"Synchronization starting in {countdown} seconds...", end="\r")
    sleep(1)


def file_finder():
    # create lists to synchronize. (0/3)
    source_file_list = os.listdir(SOURCE_FOLDER_PATH)
    replica_file_list = os.listdir(REPLICA_FOLDER_PATH)
    list_to_copy = []
    # get newly created files. (1/3)
    new_file_list = [file for file in source_file_list if file not in replica_file_list]
    for new_file in new_file_list:
        logging.info(f"{now} - {new_file} created in {SOURCE_DATA_FOLDER} folder.")
        list_to_copy.append(new_file)
    # 3. inspect if existing files have changed data. if so, add into files_to_copy (2/3)
    same_file_list = list(set(source_file_list) & set(replica_file_list))
    file_hash = FileHash("sha256")
    for file_to_inspect in same_file_list:
        source_file_hash = file_hash.hash_file(SOURCE_FOLDER_PATH + "/" + file_to_inspect)
        replica_file_hash = file_hash.hash_file(REPLICA_FOLDER_PATH + "/" + file_to_inspect)
        if not source_file_hash == replica_file_hash:
            list_to_copy.append(file_to_inspect)
    # get files to delete from replica folder (3/3)
    list_to_delete = [file for file in replica_file_list if file not in source_file_list]

    return list_to_copy, list_to_delete, new_file_list


def copy_files(files, new_additions):
    for file in files:
        try:
            source_file_path = os.path.join(SOURCE_FOLDER_PATH, file)
            replica_file_path = os.path.join(REPLICA_FOLDER_PATH, file)

            shutil.copy(source_file_path, replica_file_path)

            if file in new_additions:
                logging.info(f"{now} - {file} copied from {SOURCE_DATA_FOLDER} to {REPLICA_DATA_FOLDER} folder.")
            else:
                logging.info(f"{now} - existing file modified: {file}")
        except FileNotFoundError as error:
            logging.error(f"{now} - {error}: File {file} is not found in {SOURCE_FOLDER_PATH}.")
        except PermissionError as error:
            logging.error(f"{now} - {error}: No permission for the file {file} in {SOURCE_FOLDER_PATH}")


def delete_files(files):
    # delete the replica folder files which the source folder doesn't have.
    for file in files:
        try:
            os.remove(os.path.join(REPLICA_FOLDER_PATH, file))
            logging.info(f"{now} - {file} deleted from {REPLICA_DATA_FOLDER} during synchronization.")
        except FileNotFoundError as error:
            logging.error(f"{now} - {error}: File {file} is not found in {REPLICA_FOLDER_PATH}.")
        except PermissionError as error:
            logging.error(f"{now} - {error}: No permission for the file {file} in {REPLICA_FOLDER_PATH}.")


def logger():
    try:
        # configure the logger to leave logs on the console and save them to a log file.
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
        # set up to leave logs on the console.
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        log.addHandler(stream_handler)
        # set up to leave logs in the log file.
        file_handler = logging.FileHandler(LOG_FILE_PATH + f"/sync_log.log")
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
    except FileNotFoundError as error:
        print(f"{now} - {error}: File is not found during log setup in {LOG_FILE_PATH}.")
    except PermissionError as error:
        print(f"{now} - {error}: No permission for log setup in {LOG_FILE_PATH}.")


logger()
execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.info(f"{execution_time} - program executed.\n\n")

try:
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # if statement for which function will be executed.
        files_to_copy, files_to_delete, new_files = file_finder()

        if len(files_to_copy) == 0 and len(files_to_delete) == 0:
            print(f"{now} - The files in {REPLICA_DATA_FOLDER} folder is in sync with {SOURCE_DATA_FOLDER} folder")
        else:
            if len(files_to_copy) > 0:
                copy_files(files_to_copy, new_files)
            if len(files_to_delete) > 0:
                delete_files(files_to_delete)
            print("Synchronization completed.\n")
    # sleep for the assigned INTERVAL sec.
        sleep(int(INTERVAL))
except KeyboardInterrupt:
    print("\nSynchronization stopped by user.")
