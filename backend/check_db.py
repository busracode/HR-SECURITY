import sqlite3

conn = sqlite3.connect("instance/database.db")
cursor = conn.cursor()

# Users
print("=== USERS ===")
cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(row)

# Candidates
print("\n=== CANDIDATES ===")
cursor.execute("SELECT * FROM candidates")
for row in cursor.fetchall():
    print(row)

# Applications
print("\n=== APPLICATIONS ===")
cursor.execute("SELECT * FROM applications")
for row in cursor.fetchall():
    print(row)

conn.close()