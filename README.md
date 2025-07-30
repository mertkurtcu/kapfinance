
# 📊 kapfinance - Finansal Veri Yöneticisi

`kapfinance`, Türkiye'deki şirketlerin Kamuyu Aydınlatma Platformu (KAP) üzerinden indirilen `.xls` (HTML tabanlı) finansal tablo dosyalarını kolayca okuyup analiz edebilmeniz için geliştirilmiş bir Python kütüphanesidir.

> Bu araç, finansal tablo klasörlerinizi tarar, dosyaları periyot bazında düzenler ve istediğiniz şirketin dönemsel finansal verilerini hızlıca bir `pandas.DataFrame` yapısı olarak sunar.

---

## 🚀 Kurulum

```bash
pip install kapfinance
```

---

## 📂 Klasör Yapısı Beklentisi

KAP üzerinden indirilen dosyalar aşağıdaki gibi organize edilmelidir:

```
FinancialTable/
├── 2020_01/
│   ├── AKBNK.xls
│   ├── GARAN.xls
├── 2020_02/
│   ├── AKBNK.xls
│   └── GARAN.xls
...
```

Her alt klasör bir dönemi temsil etmeli (`YYYY_QQ` formatında), ve `.xls` dosyalarının isimlerinin ilk 5 karakteri ilgili şirketin **ticker** (hisse kodu) olmalıdır (örn. `AKBNK.xls`).

---

## 🧠 Temel Kullanım

```python
from kapfinance import FinancialDataManager

# 1. Verinin bulunduğu kök klasör yolunu belirtin
data_path = "C:/Users/kullanici_adi/Downloads/FinancialTable/"

# 2. Veri yöneticisini başlatın
kap = FinancialDataManager(data_path)

# 3. Mevcut tüm şirketleri listeleyin
print(kap.list_available_tickers())

# 4. Belirli bir şirketin tüm verisini yükleyin
df_akbnk = kap.download("AKBNK")
print(df_akbnk.head())

# 5. Belirli tarih aralığına göre filtreleme
df_garan = kap.download("GARAN", start="2020_01", end="2022_04")
print(df_garan.head())
```

---

## 📐 DataFrame Yapısı

`download()` fonksiyonu şu yapıda bir `pandas.DataFrame` döner:

| Description               | 2020_01 | 2020_02 | ... |
|---------------------------|---------|---------|-----|
| Hasılat                   | 1234    | 1300    | ... |
| Net Dönem Kar/Zararı      | 456     | 500     | ... |
| Öz Kaynaklar              | 789     | 810     | ... |

- **Satırlar:** Hesap kalemleri  
- **Sütunlar:** Finansal dönemler  
- **Değerler:** Sayısal büyüklükler (otomatik olarak `float`'a dönüştürülür)

---

## ⚠️ Önemli Notlar

- `.xls` dosyaları aslında HTML tabanlıdır ve `pandas.read_html()` ile işlenmektedir.
- Sayısal değerlerde Türkçe format desteği mevcuttur (örn. `1.234.567,89` → `1234567.89`)
- Eğer bir dosyada hata oluşursa veya okunamıyorsa, uyarı logu yazılır ancak program çalışmaya devam eder.

---

## 🛠 Geliştirici Notları

### Dosya Yapısı

- `kapfinance/`
  - `__init__.py`
  - `kapfinance.py`
- `setup.py`
- `README.md`
- `LICENSE`

---

## ✅ Yapılacaklar

- [ ] `matplotlib` desteği ile otomatik grafikleme
- [ ] Daha sağlam dosya formatı kontrolleri
- [ ] Türkçe/İngilizce çoklu dil desteği
- [ ] Finansal oran hesaplamaları (F/K, PD/DD vb.) için yardımcı sınıflar

---

## 📄 Lisans

MIT License. Detaylar için [LICENSE](./LICENSE) dosyasına bakabilirsiniz.

---

## 👨‍💻 Katkıda Bulun

Pull request’ler ve sorun bildirimi (issue) açmak serbesttir. İyileştirme önerilerinizi memnuniyetle karşılarız!

---

## 📬 İletişim

Herhangi bir sorunuz varsa GitHub üzerinden issue açabilir veya doğrudan iletişime geçebilirsiniz.
