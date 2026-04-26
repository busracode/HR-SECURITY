from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

# ============================================================
# CORE REQUIREMENT 3 — Encryption (Fernet/AES)
# "Use a secure method (e.g., Fernet/AES)"
# ============================================================

FERNET_KEY = b'pbh2inlGkMB6BEvwGwhXhffc6vPESWLwH45spSK3vuU='
cipher_suite = Fernet(FERNET_KEY)

# ============================================================
# CORE REQUIREMENT 1 — Authentication
# "Passwords must be stored using secure hashing"
# "No plaintext passwords"
# ============================================================

def hash_password(password):
    """Şifreyi hashler — veritabanına plaintext asla yazılmaz."""
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    """Login sırasında girilen şifreyi hash ile karşılaştırır."""
    return check_password_hash(hashed_password, password)

# ============================================================
# CORE REQUIREMENT 3 — Encryption
# "Encrypt sensitive data before storing"
# "Decrypt data when displaying it"
# ============================================================

def encrypt_data(data):
    """Hassas veriyi DB ye yazmadan önce Fernet (AES) ile şifreler."""
    if data:
        return cipher_suite.encrypt(data.encode('utf-8')).decode('utf-8')
    return data

def decrypt_data(encrypted_data):
    """Admin sayfasında göstermek için şifreli veriyi çözer."""
    if encrypted_data:
        return cipher_suite.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')
    return encrypted_data