# File Synchronization Tool
This tool synchronizes files between a source folder and a replica folder at regular intervals. It ensures that any new or modified files in the source folder are copied to the replica folder, and any files not present in the source folder are deleted from the replica folder. The tool logs all synchronization activities.
## Requirements
- `Python 3.x`
- **`filehash`** library: Install using `pip install filehash`
## Usage
```python
python my_file_sync_tool.py <source_folder_path> <replica_folder_path> <log_file_path> <interval>
```
- **`source_folder_path`**: Path to the source folder.
- **`replica_folder_path`**: Path to the replica folder.
- **`log_file_path`**: Path to the log file.
- **`interval`**: Time interval (in seconds) between synchronizations.
## Example
```python
python my_file_sync_tool.py /path/to/source /path/to/replica /path/to/log 30
```
## Features
- **Automatic Synchronization**: The tool automatically synchronizes files at the specified interval.
- **Logging**: Detailed logs of all synchronization activities are saved to a log file and printed on the console.
- **File Integrity Check**: Uses SHA-256 hashing to detect changes in files.
## Code Explanation
### Imports
- **`os`**, **`sys`**, **`shutil`**: For file and directory operations.
- **`sleep`** from **`time`**: For interval-based synchronization.
- **`datetime`**: For timestamps in logs.
- **`FileHash`** from **`filehash`**: For file integrity checks using SHA-256.
- **`logging`**: For logging activities.
### Command Line Arguments
The script expects the following command line arguments:
1. **`source_folder_path`**
2. **`replica_folder_path`**
3. **`log_file_path`**
4. **`interval`**
### Initialization
- **Source and Replica Paths**: Extracted from command line arguments.
- **Logging Setup**: Configures logging to console and log file.
### Synchronization Process
1. **file_finder**: Identifies files to copy and delete.
   - **New Files**: Files present in the source but not in the replica.
   - **Modified Files**: Files with different hashes in source and replica.
   - **Files to Delete**: Files present in the replica but not in the source.
2. **copy_files**: Copies new and modified files from the source to the replica.
3. **delete_files**: Deletes files from the replica that are not present in the source.
### Logging
- Logs are saved to both the console and the specified log file.
- Log messages include timestamps and detailed descriptions of synchronization activities.
### Continuous Synchronization
- The script runs in an infinite loop, synchronizing at the specified interval.
- The loop can be stopped using **`Ctrl + C`**.
### Error Handling
- Handles **`FileNotFoundError`** and **`PermissionError`** during file operations and logging setup.
### Main Loop
- Continuously checks for file changes and performs synchronization.
- Sleeps for the specified interval between synchronizations.
### Stopping the Script
- Use **`Ctrl + C`** to stop the synchronization process.
## Example Log Output
```python
2023-07-17 10:00:00 - program executed.
2023-07-17 10:00:30 - new_file.txt created in source folder.
2023-07-17 10:00:30 - new_file.txt copied from source to replica folder.
2023-07-17 10:00:30 - existing_file.txt modified.
2023-07-17 10:00:30 - file_to_delete.txt deleted from replica during synchronization.
```
## Notes
- Ensure that the source and replica folders exist and have the necessary permissions before running the script.
- The log file path should be a valid directory where the script has write permissions.
