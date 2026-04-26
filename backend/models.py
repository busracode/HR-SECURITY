import sqlite3
from contextlib import contextmanager
# security_logic.py'den şifreleme fonksiyonlarını import ediyoruz
from security_logic import hash_password, encrypt_data

DB_NAME = "database.db"

# Veritabanı bağlantısını güvenli şekilde açıp kapatan context manager
@contextmanager
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Sonuçları sözlük gibi okumak için
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

# Tabloları oluşturan fonksiyon — app.py'de bir kere çağrılacak
def init_db():
    with get_db() as conn:
        cur = conn.cursor()

        # CORE REQUIREMENT 1 — Authentication:
        # Kullanıcı kayıt sistemi için users tablosu
        # role alanı RBAC için: 'User' veya 'Admin' değeri alır
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            password TEXT NOT NULL,        -- Plaintext değil, bcrypt hash saklanır
            role TEXT DEFAULT 'User',      -- CORE REQUIREMENT 2: RBAC için rol alanı
            UNIQUE(first_name, last_name)  -- Aynı isimde iki kullanıcı olamaz
        )
        """)

        # CORE REQUIREMENT 3 — Encryption:
        # Başvuru formu verileri — hassas alanlar şifreli saklanır
        # user_id ile hangi kullanıcının başvurduğunu takip ediyoruz
        cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,               -- Başvuruyu yapan kullanıcının ID'si
            first_name TEXT,
            last_name TEXT,
            job TEXT,
            school TEXT,                   -- Fernet ile şifreli saklanır
            department TEXT,               -- Fernet ile şifreli saklanır
            salary TEXT,                   -- Fernet ile şifreli saklanır
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

# CORE REQUIREMENT 1 — Authentication:
# Yeni kullanıcı kaydeder, şifreyi hashleyerek saklar (plaintext yasak)
def insert_user(first_name, last_name, password, role):
    hashed_password = hash_password(password)  # bcrypt ile hashle
    with get_db() as conn:
        try:
            conn.execute("""
            INSERT INTO users (first_name, last_name, password, role)
            VALUES (?, ?, ?, ?)
            """, (first_name, last_name, hashed_password, role))
            return True
        except sqlite3.IntegrityError:
            return False  # Aynı isimde kullanıcı varsa False döner

# Kullanıcıyı isim-soyisim ile veritabanından çeker (login için kullanılır)
def get_user(first_name, last_name):
    with get_db() as conn:
        return conn.execute("""
        SELECT * FROM users
        WHERE first_name = ? AND last_name = ?
        """, (first_name, last_name)).fetchone()

# CORE REQUIREMENT 3 — Encryption:
# Başvuru formunu kaydeder, hassas alanları Fernet (AES) ile şifreler
def insert_application(user_id, first_name, last_name, job, school, department, salary):
    encrypted_school = encrypt_data(school)           # Okul şifreleniyor
    encrypted_department = encrypt_data(department)   # Bölüm şifreleniyor
    encrypted_salary = encrypt_data(salary)           # Maaş beklentisi şifreleniyor
    with get_db() as conn:
        conn.execute("""
        INSERT INTO applications
        (user_id, first_name, last_name, job, school, department, salary)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, first_name, last_name, job, encrypted_school, encrypted_department, encrypted_salary))

# CORE REQUIREMENT 2 — Access Control:
# Tüm başvuruları getirir — sadece Admin rolündeki kullanıcılar erişebilir
# Erişim kontrolü middleware.py'deki @admin_required ile sağlanır
def get_all_applications():
    with get_db() as conn:
        return conn.execute("SELECT * FROM applications").fetchall()