from cryptography.fernet import Fernet

class Encryptor:
    """Handles encryption and decryption using AES-based Fernet encryption."""
    
    def __init__(self, key=None):
        if key is None:
            key = Fernet.generate_key()
        self.cipher = Fernet(key)
        self.key = key  # Store the key for future use

    def encrypt(self, data: bytes) -> bytes:
        """Encrypts the given data."""
        return self.cipher.encrypt(data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypts the given data."""
        return self.cipher.decrypt(encrypted_data)

    def get_key(self) -> bytes:
        """Returns the encryption key."""
        return self.key

# Example usage
if __name__ == "__main__":
    encryptor = Encryptor()
    sample_data = b"Hello, P2P World!"
    encrypted = encryptor.encrypt(sample_data)
    decrypted = encryptor.decrypt(encrypted)
    
    print(f"Original: {sample_data}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
