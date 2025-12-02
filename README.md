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
- Proje klasöründeki tüm `.xls` dosyalarını tarar  
- Ticker → Dönem → Dosya haritası oluşturur  
- Şu örnek formatlarla uyumludur:  
  - `ASELS_2023_06.xls`  
  - `THYAO-2022-12.xls`  
  - `KCHOL_202101.xls`

---

### ✔ Ölçek algılama (Sunum Para Birimi)
Tablolarda yer alan `"Sunum Para Birimi 1.000 TL"` benzeri ifadelerden otomatik çarpan belirlenir.

Desteklenen formatlar:

- `1 TL`
- `1.000 TL`
- `1.000.000 TL`
- `1000 TL`
- Sadece `TL` → ölçek = 1

---

### ✔ Tablodan veri çekme  
Her tabloda açıklama ve değer kolonları okunur, ölçek uygulanır ve DataFrame’e dönüştürülür.

Örnek:

| Açıklama        | Değer  | Ölçek |
|-----------------|--------|-------|
| Dönen Varlıklar | 12.345 | 1000  |

Pivotlanmış DataFrame çıktısı:

| Period  | Dönen Varlıklar |
|---------|------------------|
| 2023_06 | 12,345,000       |

---

### ✔ Testler  
`tests/test_basic.py` dosyasında:

- Ticker tanıma testi  
- Ölçek algılama testi  
- Sahte tablo üzerinden veri çekme testi  
- Okuma hatası işleme testi  

---

## 📂 Proje Yapısı

