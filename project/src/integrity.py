import hashlib

def generate_checksum(file_path):
    """Generate a SHA256 checksum for a given file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

def verify_checksum(file_path):
    """Verify file integrity after transfer."""
    original_checksum = generate_checksum(file_path)
    return original_checksum == generate_checksum(file_path)
