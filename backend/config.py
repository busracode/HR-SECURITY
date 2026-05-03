"""
Flask Application Configuration

Usage:
from config import DevelopmentConfig, ProductionConfig
app.config.from_object(DevelopmentConfig)
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file so all config values are available at import time
load_dotenv()


class Config:
    """
    Base configuration shared across all environments
    """

    # ------------------------------------------------------------------
    # SECURITY
    # ------------------------------------------------------------------

    # AUTHENTICATION: Secret key used to sign Flask sessions and JWT tokens
    # IMPORTANT: Must be overridden with a strong random value in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # ENCRYPTION: Fernet symmetric key used by SecurityManager to encrypt/decrypt sensitive fields (e.g., salary)
    # IMPORTANT: Must be set in .env — losing this key makes all encrypted data unreadable
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
    if not ENCRYPTION_KEY:
        print("WARNING: ENCRYPTION_KEY is not defined in .env file!")
        print("Run the following command to generate one:")
        print("python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\"")

    # ------------------------------------------------------------------
    # DATABASE
    # ------------------------------------------------------------------

    # Default to a local SQLite file; override with DATABASE_URL in production (e.g., PostgreSQL)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///recruitment.db'
    # Disable SQLAlchemy's event system for modification tracking — reduces overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Set to True in development to print all generated SQL queries to the console
    SQLALCHEMY_ECHO = False

    # ------------------------------------------------------------------
    # SESSION AND COOKIE SETTINGS
    # ------------------------------------------------------------------

    # AUTHENTICATION: How long a user's session remains valid without activity
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # Restrict session cookie to HTTPS-only connections (prevents interception over plain HTTP)
    SESSION_COOKIE_SECURE = True  # Production: True, Development: False

    # Prevent JavaScript from reading the session cookie — mitigates XSS-based session theft
    SESSION_COOKIE_HTTPONLY = True

    # Limit cookie sending to same-site requests — provides CSRF protection
    # 'Lax' allows top-level navigation but blocks cross-site subresource requests
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Refresh the session lifetime on every request to keep active users logged in
    SESSION_REFRESH_EACH_REQUEST = True

    # ------------------------------------------------------------------
    # WTFORMS (FORM PROTECTION)
    # ------------------------------------------------------------------

    # Enable CSRF token validation on all form submissions
    WTF_CSRF_ENABLED = True

    # None means the CSRF token expires with the session
    WTF_CSRF_TIME_LIMIT = None

    # ------------------------------------------------------------------
    # LOGGING
    # ------------------------------------------------------------------

    # Path to the file where incoming request logs are written
    ACCESS_LOG_FILE = 'logs/access.log'

    # ------------------------------------------------------------------
    # APPLICATION SETTINGS
    # ------------------------------------------------------------------

    # Maximum allowed size for file uploads (16 MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'uploads'
    # Only these file extensions are accepted for uploads
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    # Number of records shown per page in paginated list views
    ITEMS_PER_PAGE = 10

    # ------------------------------------------------------------------
    # GENERAL FLAGS
    # ------------------------------------------------------------------

    # Debug mode is off by default; enabled per environment subclass
    DEBUG = False

    # Testing mode is off by default; enabled in TestingConfig
    TESTING = False

    # Pretty-print JSON API responses for easier manual inspection
    JSONIFY_PRETTYPRINT_REGULAR = True


class DevelopmentConfig(Config):
    """
    Development environment configuration.

    Features:
    - DEBUG = True (auto-reload on code changes)
    - Detailed error messages
    - SQL query logging enabled

    Usage:
    FLASK_ENV=development python app.py
    """
    DEBUG = True
    TESTING = False

    # HTTPS is not required in local development
    SESSION_COOKIE_SECURE = False

    # Print every SQL query to the console to aid debugging
    SQLALCHEMY_ECHO = True

    print("Development environment loaded (DEBUG=True)")


class ProductionConfig(Config):
    """
    Production environment configuration.

    Features:
    - DEBUG = False
    - Strict security settings
    - HTTPS required

    IMPORTANT: Before deploying to production:
       1. Set a strong SECRET_KEY
       2. Add ENCRYPTION_KEY to .env
       3. Set DATABASE_URL to PostgreSQL/MySQL
       4. Install an HTTPS certificate

    Usage:
    FLASK_ENV=production python app.py
    """
    DEBUG = False
    TESTING = False

    # Enforce HTTPS-only cookie transmission in production
    SESSION_COOKIE_SECURE = True

    # SQL query logging is disabled in production to avoid log bloat
    SQLALCHEMY_ECHO = False

    # Apply the same secure flags to the "remember me" cookie
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

    print("Production environment loaded (DEBUG=False)")


class TestingConfig(Config):
    """
    Testing environment configuration.

    Features:
    - In-memory SQLite database for fast, isolated tests
    - CSRF protection disabled so test clients can submit forms freely
    - Cookie security relaxed for the test runner

    Usage:
    FLASK_ENV=testing python -m pytest
    """
    TESTING = True

    # Use an in-memory database so each test run starts with a clean state
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Disable CSRF checks during automated testing
    WTF_CSRF_ENABLED = False

    # HTTPS is not available in the test environment
    SESSION_COOKIE_SECURE = False

    print("Testing environment loaded (TESTING=True)")


# Select the correct configuration class based on the FLASK_ENV environment variable
def get_config():
    """
    Return the appropriate configuration class for the current environment.

    Environment variable values:
    - FLASK_ENV=development -> DevelopmentConfig
    - FLASK_ENV=production  -> ProductionConfig
    - FLASK_ENV=testing     -> TestingConfig

    Default: DevelopmentConfig
    """
    env = os.environ.get('FLASK_ENV', 'development')

    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }

    return config_map.get(env, DevelopmentConfig)