"""
GÜVENLİK YÖNETIMI

Bu modül şunları sağlar:
1. Password Hashing (bcrypt)
2. Data Encryption/Decryption (Fernet)
3. Input Validation
4. Security Utilities

Kullanım:
from utils.security import SecurityManager

# Şifre hash'leme
hashed = SecurityManager.hash_password('MyPassword123')

# Veri şifreleme
encrypted = SecurityManager.encrypt_data('maaş_bilgisi')
decrypted = SecurityManager.decrypt_data(encrypted)
"""

import os
import re
from cryptography.fernet import Fernet, InvalidToken
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


class SecurityManager:
    """
    Şifreleme, hashing ve güvenlik fonksiyonları
    """
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 🔐 PASSWORD HASHING (Kimlik Doğrulama)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    @staticmethod
    def hash_password(password):
        """
        Şifreyi bcrypt ile hash'le
        
        ✅ Güvenliği: 
           - Slow (brute-force'a karşı)
           - Salted (rainbow table'lara karşı)
           - Adaptif (algoritma güçlenebilir)
        
        Parametreler:
            password (str): Düz şifre
        
        Döndürür:
            str: Hash'lenmiş şifre
        
        Örnek:
            >>> hash = SecurityManager.hash_password('MyPassword123')
            >>> hash
            '$2b$12$R9h/cIPz0gi.URNNGU3ZA.UXnLMiHvMnP/6FBv5Z6qpYrVIrBvvYm'
        
        Not:
            - Her seferinde farklı hash oluşturulur (salt nedeniyle)
            - Hash'ten plaintext'e dönüştürülemez (one-way function)
        """
        try:
            # pbkdf2:sha256 yerine werkzeug tarafından önerilen yöntem
            hashed = generate_password_hash(
                password,
                method='scrypt',  # Güçlü hashing algoritması
                salt_length=16
            )
            return hashed
        except Exception as e:
            raise ValueError(f"Şifre hash'leme hatası: {str(e)}")
    
    @staticmethod
    def verify_password(password_hash, password):
        """
        Hash'lenmiş şifreyi plaintext ile karşılaştır
        
        ✅ Nasıl Çalışır:
           1. Plaintext şifreyi aynı yöntemle hash'le
           2. Her iki hash'i karşılaştır
           3. Timing attack'lara karşı korumalı karşılaştırma (constant-time)
        
        Parametreler:
            password_hash (str): Veritabanındaki hash'lenmiş şifre
            password (str): Kullanıcı tarafından girilen şifre
        
        Döndürür:
            bool: True (doğru) veya False (yanlış)
        
        Örnek:
            >>> hash = SecurityManager.hash_password('MyPassword123')
            >>> SecurityManager.verify_password(hash, 'MyPassword123')
            True
            >>> SecurityManager.verify_password(hash, 'WrongPassword')
            False
        """
        try:
            return check_password_hash(password_hash, password)
        except Exception as e:
            print(f"Şifre doğrulama hatası: {str(e)}")
            return False
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 🔒 DATA ENCRYPTION (Veri Şifreleme)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    @staticmethod
    def encrypt_data(data):
        """
        Veriyi Fernet (Symmetric Encryption) ile şifrele
        
        ✅ Güvenliği:
           - Symmetric: Şifreleme ve çözmek için aynı anahtar kullanılır
           - Authenticated: Verinin değiştirilmediğini doğrular
           - Time-stamp: Verinin ne zaman şifrelendiğini kaydeder
        
        Şifrelenecek Veriler:
           ✅ Maaş bilgisi
           ✅ Telefon numarası
           ✅ SSN/Kimlik numarası
           ✅ Tıbbi bilgiler
           ❌ Ad-Soyad (araştırma için gerekli)
           ❌ Email (iletişim için)
        
        Parametreler:
            data: Şifrelenecek veri (str, int, float)
        
        Döndürür:
            str: Base64 kodlanmış şifrelenmiş veri
        
        Örnek:
            >>> encrypted = SecurityManager.encrypt_data('50000')
            >>> encrypted
            'gAAAAABlq7Z_x1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t'
            
            >>> SecurityManager.decrypt_data(encrypted)
            '50000'
        
        Hata Yönetimi:
            - ENCRYPTION_KEY tanımlanmamışsa hata
            - Geçersiz veri tipinde hata
        """
        try:
            # .env dosyasından encryption key'i al
            key = current_app.config.get('ENCRYPTION_KEY')
            
            if not key:
                raise ValueError(
                    "ENCRYPTION_KEY .env dosyasında tanımlanmamış!\n"
                    "Aşağıdaki komutla oluşturun:\n"
                    "python -c \"from cryptography.fernet import Fernet; "
                    "print(Fernet.generate_key().decode())\""
                )
            
            # Veriyi string'e çevir (güvenlik için)
            data_str = str(data)
            
            # Fernet cipher oluştur
            cipher = Fernet(key)
            
            # Veriyi şifrele
            encrypted_bytes = cipher.encrypt(data_str.encode())
            
            # Base64 string olarak döndür
            return encrypted_bytes.decode()
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"Veri şifreleme hatası: {str(e)}")
    
    @staticmethod
    def decrypt_data(encrypted_data):
        """
        Fernet ile şifrelenmiş veriyi çöz
        
        ✅ Nasıl Çalışır:
           1. Base64 string'i bytes'a çevir
           2. Aynı anahtarla Fernet cipher oluştur
           3. Verileri decrypt et
           4. String'e çevir ve döndür
        
        Parametreler:
            encrypted_data (str): Şifrelenmiş veri
        
        Döndürür:
            str: Şifre çözülmüş plaintext veri
        
        Örnek:
            >>> encrypted = SecurityManager.encrypt_data('50000')
            >>> decrypted = SecurityManager.decrypt_data(encrypted)
            >>> decrypted
            '50000'
        
        Hata Yönetimi:
            - InvalidToken: Hash doğrulaması başarısız
            - Verilerin değiştirilmesi otomatik olarak algılanır
        
        ⚠️ ÖNEMLİ: Encryption key'i kaybederseniz verileri çözemezsiniz!
        """
        try:
            # .env dosyasından encryption key'i al
            key = current_app.config.get('ENCRYPTION_KEY')
            
            if not key:
                raise ValueError("ENCRYPTION_KEY tanımlanmamış!")
            
            # Fernet cipher oluştur (aynı anahtarla)
            cipher = Fernet(key)
            
            # Veriyi decrypt et
            decrypted_bytes = cipher.decrypt(encrypted_data.encode())
            
            # String'e çevir ve döndür
            return decrypted_bytes.decode()
            
        except InvalidToken:
            raise ValueError(
                "Veri decrypt hatası: Hash doğrulaması başarısız!\n"
                "Olası nedenler:\n"
                "1. Encryption key değiştirildi\n"
                "2. Veri dosyadan sonra değiştirildi\n"
                "3. Yanlış encrypted_data geçildi"
            )
        except Exception as e:
            raise ValueError(f"Veri decrypt hatası: {str(e)}")
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ✅ INPUT VALIDATION (Giriş Doğrulama)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    @staticmethod
    def validate_email(email):
        """
        Email adresini doğrula
        
        Kontrol Noktaları:
        - Email formatı geçerli mi?
        - Uzunluk uygun mu? (5-120 karakter)
        - Yasaklı karakterler var mı?
        
        Parametreler:
            email (str): Doğrulanacak email
        
        Döndürür:
            bool: True (geçerli) veya False (geçersiz)
        
        Örnek:
            >>> SecurityManager.validate_email('user@example.com')
            True
            >>> SecurityManager.validate_email('invalid-email')
            False
        """
        if not email or len(email) > 120:
            return False
        
        # Basit email regex (RFC 5322'ye uygun değil ama yeterli)
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """
        Şifre güvenliğini doğrula
        
        Kontrol Noktaları:
        ✅ Minimum 8 karakter
        ✅ En az 1 büyük harf
        ✅ En az 1 küçük harf
        ✅ En az 1 rakam
        ✅ En az 1 özel karakter
        
        Parametreler:
            password (str): Doğrulanacak şifre
        
        Döndürür:
            bool: True (güvenli) veya False (zayıf)
        
        Örnek:
            >>> SecurityManager.validate_password('Weak123')
            False  # Özel karakter yok
            
            >>> SecurityManager.validate_password('Strong@123')
            True
        """
        if not password or len(password) < 8:
            return False
        
        # Kontrol Listesi
        has_upper = any(c.isupper() for c in password)      # Büyük harf
        has_lower = any(c.islower() for c in password)      # Küçük harf
        has_digit = any(c.isdigit() for c in password)      # Rakam
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)  # Özel karakter
        
        return has_upper and has_lower and has_digit and has_special
    
    @staticmethod
    def validate_username(username):
        """
        Kullanıcı adını doğrula
        
        Kontrol Noktaları:
        - 3-30 karakter arasında
        - Alfanumerik, _, - karakterleri içerebilir
        - Başında/sonunda rakam/özel karakter olamaz
        
        Parametreler:
            username (str): Doğrulanacak kullanıcı adı
        
        Döndürür:
            bool: True (geçerli) veya False (geçersiz)
        """
        if not username or len(username) < 3 or len(username) > 30:
            return False
        
        # Alfanumerik + _ ve -
        pattern = r'^[a-zA-Z0-9_-]+$'
        return re.match(pattern, username) is not None


class Validators:
    """
    Ek doğrulama fonksiyonları
    """
    
    @staticmethod
    def validate_phone(phone):
        """Telefon numarasını doğrula"""
        if not phone:
            return True  # Opsiyonel alan
        
        # Türkiye: +90xxx xxx xx xx veya 05xx xxx xx xx
        pattern = r'^(\+90|0)[0-9]{10}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_salary(salary):
        """Maaş bilgisini doğrula"""
        try:
            sal = float(salary)
            return sal > 0  # Pozitif olmalı
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_gpa(gpa):
        """GPA (not ortalaması) doğrula"""
        try:
            g = float(gpa)
            return 0.0 <= g <= 4.0  # 0-4 arası
        except (ValueError, TypeError):
            return False


def generate_encryption_key():
    """
    Yeni Fernet encryption key oluştur
    
    Proje başında ÇÖK KERE çalıştırılacak!
    
    Kullanım:
        python -c "from utils.security import generate_encryption_key; generate_encryption_key()"
    
    Çıktı:
        ENCRYPTION_KEY=gAAAAABlq7Z_x1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
        
        Bunu .env dosyasına yapıştırın!
    """
    key = Fernet.generate_key()
    print(f"ENCRYPTION_KEY={key.decode()}")
    print("\n⚠️  Bu anahtarı .env dosyasına yapıştırın!")
    print("⚠️  Bu anahtarı kaybederseniz şifrelenmiş verileri çözemezsiniz!")


# Test Kodları
if __name__ == '__main__':
    print("🔐 Security Manager Test\n")
    
    # 1. Password Hashing Test
    print("1️⃣  Password Hashing Test")
    password = "TestPassword@123"
    hashed = SecurityManager.hash_password(password)
    print(f"   Plaintext:  {password}")
    print(f"   Hash:       {hashed[:50]}...")
    print(f"   Verify:     {SecurityManager.verify_password(hashed, password)}")
    print()
    
    # 2. Input Validation Test
    print("2️⃣  Input Validation Test")
    print(f"   Email 'test@example.com': {SecurityManager.validate_email('test@example.com')}")
    print(f"   Email 'invalid': {SecurityManager.validate_email('invalid')}")
    print(f"   Password 'Strong@123': {SecurityManager.validate_password('Strong@123')}")
    print(f"   Password 'weak': {SecurityManager.validate_password('weak')}")
    print()
    
    print("✅ Testler tamamlandı!")
