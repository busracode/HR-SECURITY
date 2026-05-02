"""
Flask Uygulaması Konfigürasyonu

Kullanım:
from config import DevelopmentConfig, ProductionConfig
app.config.from_object(DevelopmentConfig)
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Tüm ortamlar için ortak konfigürasyon
    """
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 🔐 GÜVENLİK
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Flask Session Anahtarı
    # ⚠️ ÖNEMLİ: Üretim ortamında değiştirin!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Şifreleme Anahtarı (Fernet)
    # ⚠️ ÖNEMLİ: .env dosyasından okunmalı
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
    if not ENCRYPTION_KEY:
        print("⚠️  UYARI: ENCRYPTION_KEY .env dosyasında tanımlanmamış!")
        print("Aşağıdaki komutu çalıştırın:")
        print("python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\"")
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 🗄️ VERİTABANI
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # SQLite Veritabanı
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///recruitment.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLAlchemy Echo (SQL sorgularını göster - debug için)
    SQLALCHEMY_ECHO = False
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 🔑 SESSION ve COOKIE AYARLARI
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Session Süresi
    # Kullanıcı ne kadar süre hareketsiz kaldıktan sonra logout olsun?
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Cookie Ayarları
    # HTTPS (Secure): HTTPS üzerinden mi sadece gönderilsin?
    SESSION_COOKIE_SECURE = True  # Üretim: True, Geliştirme: False
    
    # HttpOnly: JavaScript tarafından erişilebilir mi? (XSS koruması)
    SESSION_COOKIE_HTTPONLY = True
    
    # SameSite: Cross-site request forgery (CSRF) koruması
    # Lax: Form submit'inde gönderilir, normal link tıklamasında gönderilmez
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Session Refresh Intervali (dakika)
    SESSION_REFRESH_EACH_REQUEST = True
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 🛡️ WTForms (Form Koruma)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # CSRF Protection Açık mı?
    WTF_CSRF_ENABLED = True
    
    # CSRF Token Geçerlilik Süresi
    # None = Varsayılan (session süresi kadar)
    WTF_CSRF_TIME_LIMIT = None
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 📊 LOGLAMA
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Access Log Dosyası
    ACCESS_LOG_FILE = 'logs/access.log'
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 📝 UYGULAMA AYARLARI
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Dosya Upload Ayarları
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ⚙️ DEĞİŞTİRİLEBİLİR AYARLAR
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Debug Modu (geliştirme için)
    DEBUG = False
    
    # Test Modu (unit testler için)
    TESTING = False
    
    # JSON Formatting (API responses)
    JSONIFY_PRETTYPRINT_REGULAR = True


class DevelopmentConfig(Config):
    """
    Geliştirme Ortamı Konfigürasyonu
    
    Özellikler:
    - DEBUG = True (Otomatik yeniden yükleme)
    - Detaylı hata mesajları
    - SQLAlchemy ECHO = True (SQL sorgularını göster)
    
    Kullanım:
    FLASK_ENV=development python app.py
    """
    DEBUG = True
    TESTING = False
    
    # Geliştirme sırasında HTTPS zorunlu değil
    SESSION_COOKIE_SECURE = False
    
    # SQL sorgularını konsola yaz (debug için)
    SQLALCHEMY_ECHO = True
    
    print("Gelistirme Ortami Yuklendi (DEBUG=True)")


class ProductionConfig(Config):
    """
    Üretim Ortamı Konfigürasyonu
    
    Özellikler:
    - DEBUG = False
    - Katı güvenlik ayarları
    - HTTPS zorunlu
    
    ⚠️ ÖNEMLİ: Üretim ortamında:
       1. SECRET_KEY'i değiştirin
       2. ENCRYPTION_KEY'i .env'ye ekleyin
       3. Database URI'ı PostgreSQL/MySQL olarak değiştirin
       4. HTTPS sertifikası kurun
    
    Kullanım:
    FLASK_ENV=production python app.py
    """
    DEBUG = False
    TESTING = False
    
    # Üretim ortamında HTTPS zorunlu
    SESSION_COOKIE_SECURE = True
    
    # SQL sorgularını loggalama
    SQLALCHEMY_ECHO = False
    
    # Strict Security Headers
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    print("Uretim Ortami Yuklendi (DEBUG=False)")


class TestingConfig(Config):
    """
    Test Ortamı Konfigürasyonu
    
    Özellikler:
    - In-memory SQLite database
    - CSRF koruması kapalı
    - Cookie ayarları test için optimize
    
    Kullanım:
    FLASK_ENV=testing python -m pytest
    """
    TESTING = True
    
    # In-memory database (hızlı test)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # CSRF'yi test sırasında kapalı tut
    WTF_CSRF_ENABLED = False
    
    # Session cookie ayarları
    SESSION_COOKIE_SECURE = False
    
    print("Test Ortami Yuklendi (TESTING=True)")


# Ortam değişkeninden konfigürasyon seç
def get_config():
    """
    Ortam değişkenine göre uygun konfigürasyonu döndür
    
    Ortam Değişkenleri:
    - FLASK_ENV=development → DevelopmentConfig
    - FLASK_ENV=production  → ProductionConfig
    - FLASK_ENV=testing     → TestingConfig
    
    Varsayılan: DevelopmentConfig
    """
    env = os.environ.get('FLASK_ENV', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }
    
    return config_map.get(env, DevelopmentConfig)
