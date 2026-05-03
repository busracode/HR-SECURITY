"""
Security Management Module

This module provides:
1. Password Hashing (bcrypt)
2. Data Encryption/Decryption (Fernet)
3. Input Validation
4. Security Utilities

Usage:
from utils.security import SecurityManager

# Hash a password
hashed = SecurityManager.hash_password('MyPassword123')

# Encrypt and decrypt data
encrypted = SecurityManager.encrypt_data('salary_info')
decrypted = SecurityManager.decrypt_data(encrypted)
"""

import os
import re
from cryptography.fernet import Fernet, InvalidToken
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


class SecurityManager:
    """
    Handles password hashing, data encryption, and input validation
    """

    # ------------------------------------------------------------------
    # AUTHENTICATION: Password Hashing
    # ------------------------------------------------------------------

    @staticmethod
    def hash_password(password):
        """
        Hash a password using scrypt. Salted and resistant to brute-force attacks.
        """
        try:
            hashed = generate_password_hash(
                password,
                method='scrypt',
                salt_length=16
            )
            return hashed
        except Exception as e:
            raise ValueError(f"Password hashing error: {str(e)}")

    @staticmethod
    def verify_password(password_hash, password):
        """
        Compare a plaintext password against its stored hash.
        """
        try:
            return check_password_hash(password_hash, password)
        except Exception as e:
            print(f"Password verification error: {str(e)}")
            return False

    # ------------------------------------------------------------------
    # ENCRYPTION: Data Encryption and Decryption (Fernet / AES)
    # ------------------------------------------------------------------

    @staticmethod
    def encrypt_data(data):
        """
        Encrypt sensitive data using Fernet symmetric encryption before storing.
        """
        try:
            key = current_app.config.get('ENCRYPTION_KEY')

            if not key:
                raise ValueError(
                    "ENCRYPTION_KEY is not defined in .env file!\n"
                    "Generate one with:\n"
                    "python -c \"from cryptography.fernet import Fernet; "
                    "print(Fernet.generate_key().decode())\""
                )

            data_str = str(data)
            cipher = Fernet(key)
            encrypted_bytes = cipher.encrypt(data_str.encode())
            return encrypted_bytes.decode()

        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"Data encryption error: {str(e)}")

    @staticmethod
    def decrypt_data(encrypted_data):
        """
        Decrypt a Fernet-encrypted string back to plaintext for display.
        """
        try:
            key = current_app.config.get('ENCRYPTION_KEY')

            if not key:
                raise ValueError("ENCRYPTION_KEY is not defined!")

            cipher = Fernet(key)
            decrypted_bytes = cipher.decrypt(encrypted_data.encode())
            return decrypted_bytes.decode()

        except InvalidToken:
            raise ValueError(
                "Decryption error: token authentication failed.\n"
                "Possible causes:\n"
                "1. The encryption key has been changed\n"
                "2. The ciphertext was modified after storage\n"
                "3. The wrong encrypted_data value was passed"
            )
        except Exception as e:
            raise ValueError(f"Data decryption error: {str(e)}")

    # ------------------------------------------------------------------
    # INPUT VALIDATION
    # ------------------------------------------------------------------

    @staticmethod
    def validate_email(email):
        """
        Validate email format and length.
        """
        if not email or len(email) > 120:
            return False

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password):
        """
        Validate password strength — requires uppercase, lowercase, digit, and special character.
        """
        if not password or len(password) < 8:
            return False

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)

        return has_upper and has_lower and has_digit and has_special

    @staticmethod
    def validate_username(username):
        """
        Validate username — alphanumeric, underscores, and hyphens only (3-30 chars).
        """
        if not username or len(username) < 3 or len(username) > 30:
            return False

        pattern = r'^[a-zA-Z0-9_-]+$'
        return re.match(pattern, username) is not None


class Validators:
    """
    Additional validation helpers
    """

    @staticmethod
    def validate_phone(phone):
        """Validate a Turkish phone number format."""
        if not phone:
            return True  # Optional field

        pattern = r'^(\+90|0)[0-9]{10}$'
        return re.match(pattern, phone) is not None

    @staticmethod
    def validate_salary(salary):
        """Validate that salary is a positive number."""
        try:
            sal = float(salary)
            return sal > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_gpa(gpa):
        """Validate that GPA is between 0.0 and 4.0."""
        try:
            g = float(gpa)
            return 0.0 <= g <= 4.0
        except (ValueError, TypeError):
            return False


def generate_encryption_key():
    """
    Generate a new Fernet encryption key. Run once at project setup and paste into .env.
    WARNING: If this key is lost, all encrypted data becomes unrecoverable.
    """
    key = Fernet.generate_key()
    print(f"ENCRYPTION_KEY={key.decode()}")
    print("\nWARNING: Paste this key into your .env file.")
    print("WARNING: If this key is lost, encrypted data cannot be decrypted!")


if __name__ == '__main__':
    print("Security Manager Test\n")

    # 1. Password Hashing Test
    print("1. Password Hashing Test")
    password = "TestPassword@123"
    hashed = SecurityManager.hash_password(password)
    print(f"   Plaintext:  {password}")
    print(f"   Hash:       {hashed[:50]}...")
    print(f"   Verify:     {SecurityManager.verify_password(hashed, password)}")
    print()

    # 2. Input Validation Test
    print("2. Input Validation Test")
    print(f"   Email 'test@example.com': {SecurityManager.validate_email('test@example.com')}")
    print(f"   Email 'invalid': {SecurityManager.validate_email('invalid')}")
    print(f"   Password 'Strong@123': {SecurityManager.validate_password('Strong@123')}")
    print(f"   Password 'weak': {SecurityManager.validate_password('weak')}")
    print()

    print("Tests completed!")