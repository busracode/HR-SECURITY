# İK Güvenli Yönetim Sistemi (React & Flask)

## 🛠 Teknoloji Yığını
- **Frontend:** React.js (Arayüz ve Client-side Routing)
- **Backend:** Flask (RESTful API)
- **Güvenlik:** Bcrypt (Hashing), Cryptography.Fernet (AES Encryption)
- **Veritabanı:** SQLite

## 🔐 Güvenlik Uygulama Planı

### 1. Kimlik Doğrulama (Authentication)
- **Backend:** Kullanıcı şifresi `bcrypt.generate_password_hash` ile saklanır. Giriş yapılırken API üzerinden doğrulanır.
- **Frontend:** Giriş başarılıysa bir `token` veya `session` saklanır.
- **Rapora Eklenecek:** Bcrypt ile hashlenmiş DB verisi görüntüsü.

### 2. Erişim Kontrolü (RBAC) - İK vs Personel
- **Frontend Koruması:** `PrivateRoute` bileşeni ile Admin olmayan kullanıcının `/admin-panel` rotasına girmesi engellenir.
- **Backend Koruması:** API tarafında her istekte kullanıcının rolü kontrol edilir (Yetkisiz bir kullanıcı API'den veri çekemez).
- **Rapora Eklenecek:** "Yetkiniz yok" uyarısı alan kullanıcı ekran görüntüsü.

### 3. Hassas Veri Şifreleme (Encryption)
- **Senaryo:** Çalışanların "Maaş" ve "Ev Adresi" veritabanında şifreli tutulur.
- **İşlem:** Backend, DB'den aldığı şifreli veriyi API üzerinden göndermeden hemen önce `Fernet.decrypt()` ile çözer ve React'a gönderir.
- **Rapora Eklenecek:** DB'deki anlamsız şifreli veri (Ciphertext) ve React ekranındaki çözülmüş veri.

## 🚀 Geliştirme Adımları
1. Flask API rotalarını oluştur (Login/Data).
2. Bcrypt ve Fernet servislerini yaz.
3. React uygulamasını `npx create-react-app` ile kur.
4. Axios kullanarak React ile Flask'ı bağla.
5. RBAC için React Router korumalı rotaları (Protected Routes) ekle.