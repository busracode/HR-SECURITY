# Güvenli Web Uygulaması Proje Planı

## Proje Hedefi
Bu proje, kimlik doğrulama, rol tabanlı erişim kontrolü (RBAC) ve veri şifreleme özelliklerine sahip güvenli bir web tabanlı yönetim paneli oluşturmayı amaçlar.

## Teknik Güvenlik Gereksinimleri

### 1. Kimlik Doğrulama (Authentication)
- **Algoritma:** Bcrypt (Hashing + Salting).
- **Akış:** - Kayıt sırasında şifreler hashlenir.
    - Giriş sırasında `check_password_hash` ile doğrulama yapılır.
- **Ekran Görüntüsü Gereksinimi:** Login sayfası ve veritabanındaki hashlenmiş şifrelerin görünümü.

### 2. Rol Tabanlı Erişim Kontrolü (RBAC)
- **Roller:** `Admin`, `User`.
- **Kısıtlamalar:** - `/admin` rotasına sadece Admin rolündeki kullanıcılar erişebilir.
    - Yetkisiz girişlerde "403 Forbidden" veya Login sayfasına yönlendirme yapılır.
- **Ekran Görüntüsü Gereksinimi:** Admin paneli erişimi ve bir User'ın admin sayfasına girmeye çalıştığında aldığı hata.

### 3. Veri Şifreleme (Encryption)
- **Kütüphane:** `cryptography.fernet`.
- **Süreç:**
    - Hassas bir veri alanı (örn: "Secret Note") belirlenecek.
    - Veri kaydedilirken AES ile şifrelenecek.
    - Dashboard'da gösterilirken anahtar (key) ile deşifre edilecek.
- **Ekran Görüntüsü Gereksinimi:** Veritabanındaki şifreli (okunamaz) veri ve uygulamanın içindeki çözülmüş hali.

## Uygulama Geliştirme Adımları
1. **[ ] Ortam Kurulumu:** Flask ve gerekli güvenlik kütüphanelerinin yüklenmesi.
2. **[ ] Veritabanı Tasarımı:** Kullanıcı tablosuna `role` ve `encrypted_data` sütunlarının eklenmesi.
3. **[ ] Hash Fonksiyonu:** Kayıt olma fonksiyonunda Bcrypt entegrasyonu.
4. **[ ] Yetkilendirme:** `@admin_required` gibi bir decorator yazılması.
5. **[ ] Şifreleme Modülü:** Veri saklama ve çekme sırasında Fernet metodlarının uygulanması.
6. **[ ] Raporlama:** PDF'deki 5-8 sayfa kuralına göre ekran görüntüleriyle dökümantasyonun yazılması.

## Rapor İçeriği (Taslak)
1. **Giriş:** Projenin amacı ve kapsamı.
2. **Sistem Tasarımı:** Mimari şeması ve akış diyagramı.
3. **Kimlik Doğrulama:** Bcrypt neden seçildi? Düz metin şifrenin riskleri.
4. **Erişim Kontrolü:** Roller nasıl yönetiliyor? Yetkisiz erişim nasıl engellendi?
5. **Şifreleme Uygulaması:** AES/Fernet süreci ve anahtar yönetimi.