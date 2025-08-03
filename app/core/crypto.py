"""Cryptography service for handling encryption and decryption."""
from cryptography.fernet import Fernet
from app.core.settings import setting

class CryptoService:
    """Service for handling encryption and decryption of sensitive data."""
    
    _fernet = None
    
    @staticmethod
    def _get_fernet():
        """Get or create Fernet instance using the secret key."""
        if not CryptoService._fernet:
            CryptoService._fernet = Fernet(setting.ENCRYPTION_KEY.encode())
        return CryptoService._fernet
    
    @staticmethod
    def encrypt(data: str) -> str:
        """Encrypt a string.
        
        Args:
            data: String to encrypt
            
        Returns:
            str: Encrypted string in base64
        """
        if not data:
            return None
        return CryptoService._get_fernet().encrypt(data.encode()).decode()
    
    @staticmethod
    def decrypt(encrypted_data: str) -> str:
        """Decrypt an encrypted string.
        
        Args:
            encrypted_data: Base64 encoded encrypted string
            
        Returns:
            str: Decrypted string
        """
        if not encrypted_data:
            return None
        return CryptoService._get_fernet().decrypt(encrypted_data.encode()).decode()
