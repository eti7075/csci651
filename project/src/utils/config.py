import os

# Default configurations
CONFIG = {
    "PEER_DISCOVERY_PORT": 5000,
    "FILE_SENDER_PORT": 5001,
    "FILE_RECEIVER_PORT": 5002,
    "CHUNK_SIZE": 1024 * 2,  # 2 KB per chunk
    "MAX_CONNECTIONS": 10,
    "LOG_LEVEL": "INFO",
    "DOWNLOAD_FOLDER": "downloads",
    "SHARED_FOLDER": "shared"
}

# Ensure the download folder exists
os.makedirs(os.getcwd() + CONFIG["DOWNLOAD_FOLDER"], exist_ok=True)
os.makedirs(os.getcwd() + CONFIG["SHARED_FOLDER"], exist_ok=True)
