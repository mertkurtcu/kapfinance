# FinancialDataManager  
KAP (Kamuyu Aydınlatma Platformu) tarafından yayımlanan finansal tablo `.xls` dosyalarını otomatik olarak  
okuyan, ölçeklendiren, temizleyen ve tekilleştirilmiş DataFrame formatına dönüştüren bir Python kütüphanesidir.

Desteklenen finansal tablolar:

- Bilanço (Finansal Durum Tablosu)
- Gelir Tablosu (Kar veya Zarar)
- Diğer Kapsamlı Gelir Tablosu
- Nakit Akış Tablosu (Dolaylı Yöntem)

Testler `pytest` ile yazılmıştır.

---

## 🚀 Özellikler

### ✔ Otomatik dosya eşleme  
- Klasör altında bulunan tüm `.xls` dosyalarını tarar  
- Ticker → Dönem → Dosya eşlemesi oluşturur  
- Örnek dosya adı formatlarıyla uyumlu:  
  - `ASELS_2023_06.xls`  
  - `THYAO-2022-12.xls`  
  - `KCHOL_202101.xls`  

---

### ✔ Ölçek algılama (Sunum Para Birimi)
Finansal tabloların çoğunda geçen `"Sunum Para Birimi 1.000 TL"` gibi ifadelerden otomatik çarpan tespit edilir.

Aşağıdaki formatlar desteklenir:

- `1 TL`
- `1.000 TL`
- `1.000.000 TL`
- `1000 TL`
- Sadece `TL` → ölçek = 1

---

### ✔ Tablodan veri çekme  
Her tablo içindeki açıklama ve değer kolonlarını tespit eder.  
Örnek:

| Açıklama | Değer | Ölçek |
|---------|--------|-------|
| Dönen Varlıklar | 12.345 | 1000 |

Bunları pivotlanmış bir DataFrame’e dönüştürür:

| Period   | Dönen Varlıklar |
|----------|------------------|
| 2023_06  | 12,345,000       |

---

### ✔ Testler  
`tests/test_basic.py` içinde:

- Ticker tanıma testi
- Ölçek algılama testi
- Sahte tablo üzerinden veri okuma testi
- Okuma hatasının handle edilmesi

---

## 📂 Proje Yapısı

