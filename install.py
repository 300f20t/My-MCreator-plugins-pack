import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

def copy_files(source_folder, destination_folder):
    if not os.path.exists(source_folder):
        print(f"❌ The source folder does not exist: {source_folder}")
        return

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"The destination folder has been created: {destination_folder}")
    
    files = os.listdir(source_folder)
    
    for file in files:
        source_path = os.path.join(source_folder, file)
        destination_path = os.path.join(destination_folder, file)
        
        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
            print(f"Copied: {file}")
    
    print("Copying is complete!")

def delete_files_only(folder_path):
    folder = Path(folder_path)
    
    for item in folder.iterdir():
        if item.is_file():
            try:
                item.unlink()
                print(f"The file has been deleted: {item}")
            except Exception as e:
                print(f"❌ Error when deleting a file {item}: {e}")

# Creating a new backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

source = Path.home() / ".mcreator" / "plugins"
destination = Path.home() / ".mcreator" / "plugins-backup" / timestamp

copy_files(source, destination)

# Clearing the plugin folder
folder_to_delete = Path.home() / ".mcreator" / "plugins"

delete_files_only(folder_to_delete)

# Installing plugins
source = Path(__file__).parent / "Plugins"
destination = Path.home() / ".mcreator" / "plugins"
    
copy_files(source, destination)

if sys.platform.startswith('win'):
        input("Press Enter to exit...")
