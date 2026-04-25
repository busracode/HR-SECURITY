# İnsan Kaynakları Güvenli Bilgi Sistemi - Proje Taslağı

## Proje Tanımı
Bu uygulama, bir şirketteki İK süreçlerini yönetirken çalışan verilerinin gizliliğini ve güvenliğini sağlamak amacıyla geliştirilmiştir.

## Güvenlik Bileşenleri Uygulama Planı

### Adım 1: Kimlik Doğrulama (Bcrypt)
- Kullanıcı kayıt olurken şifresi `salt` eklenerek hashlenir.
- Veritabanında asla `12345` gibi açık şifre görünmez.
- **Kanıt:** Veritabanı tablosundaki `password_hash` sütununun ekran görüntüsü.

### Adım 2: İK Rol Yönetimi (RBAC)
- **İK Müdürü (Admin):** Tüm çalışanların bilgilerini görüntüleme ve `/ik-panel` sayfasına erişim yetkisi.
- **Çalışan (User):** Sadece kendi dashboard sayfasını görüntüleme yetkisi.
- **Kontrol:** Kod içerisinde `@ik_yetkisi_gerekli` dekoratörü ile sayfalar korunur.

### Adım 3: Hassas Veri Şifreleme (AES-128/Fernet)
- **Şifrelenecek Alanlar:** Maaş Bilgisi, Telefon Numarası.
- **İşlem:** Veri formdan alınır, şifrelenir ve DB'ye kaydedilir. Görüntülenirken anlık olarak deşifre edilir.
- **Kanıt:** Veritabanındaki anlaşılmaz şifreli metin ile arayüzdeki gerçek verinin karşılaştırmalı görüntüsü.

## Veritabanı Model Taslağı (Örnek)
| Sütun | Tip | Güvenlik Metodu |
| :--- | :--- | :--- |
| Kullanıcı Adı | String | Açık Metin |
| Şifre | String | **Bcrypt Hash** |
| Rol | String | Admin / User |
| Maaş | String/Text | **Fernet Encryption** |
| Telefon | String/Text | **Fernet Encryption** |

## Rapor Akışı (PDF'e Uygun)
1. **Sistem Tasarımı:** İK uygulamasının genel akışı.
2. **Kimlik Doğrulama:** Şifre güvenliği neden önemli?
3. **Erişim Kontrolü:** İK verilerine neden herkes ulaşamaz?
4. **Şifreleme:** Veritabanı çalınsa bile maaş verileri nasıl güvende kalır?