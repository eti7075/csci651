import os
from utils.logger import get_logger
from utils.config import CONFIG

logger = get_logger("Search")

class FileIndex:
    """Manages local file index and search functionality."""

    def __init__(self, shared_folder=CONFIG["SHARED_FOLDER"]):
        self.shared_folder = shared_folder
        os.makedirs(shared_folder, exist_ok=True)
        self.files = set(os.listdir(shared_folder))

    def list_files(self):
        """List all available files."""
        if not self.files:
            print("No files available for sharing.")
        else:
            print("\nAvailable Files:")
            for f in self.files:
                print(f)

    def search_files(self, query):
        """Search for a file in the local index."""
        matches = [f for f in self.files if query.lower() in f.lower()]
        if matches:
            print("\nSearch Results:")
            for match in matches:
                print(match)
        else:
            print("No matching files found.")
