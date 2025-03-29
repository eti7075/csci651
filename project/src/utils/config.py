import os

# Default configurations
CONFIG = {
    "PEER_DISCOVERY_PORT": 5000,
    "FILE_TRANSFER_PORT": 5001,
    "CHUNK_SIZE": 1024 * 64,  # 64 KB per chunk
    "MAX_CONNECTIONS": 10,
    "LOG_LEVEL": "INFO",
    "DOWNLOAD_FOLDER": os.path.join(os.getcwd(), "downloads"),
}

# Ensure the download folder exists
os.makedirs(CONFIG["DOWNLOAD_FOLDER"], exist_ok=True)
