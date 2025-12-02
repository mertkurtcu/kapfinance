# 📊 FinancialDataManager
**KAP’tan indirilen .xls finansal tabloları otomatik okuma, ayıklama ve dönemlendirme aracı**

Bu proje, Kamuyu Aydınlatma Platformu’ndan (KAP) indirilen finansal tablo `.xls` dosyalarını otomatik olarak indeksleyen, okuyan ve düzenli DataFrame’lere dönüştüren bir Python aracıdır.

Desteklenen tablolar:

- **Bilanço (Finansal Durum Tablosu)**
- **Kar veya Zarar Tablosu**
- **Diğer Kapsamlı Gelir Tablosu**
- **Nakit Akış Tablosu**

Bu araç, klasördeki tüm .xls dosyalarını tarar, dosya adlarından **şirket sembolü (ticker)** ve **dönem (YYYY_Q)** bilgisini çıkarır, tabloları okur ve her kalemi ölçek (bin TL, milyon TL vb.) ile çarparak normalize eder.

---

## 🚀 Özellikler

- Klasör altındaki tüm `.xls` dosyalarını otomatik indeksler  
- Dosya adından *ticker* ve *dönem* (YYYY_MM veya YYYY_Q) algılar  
- "Sunum Para Birimi" alanını okuyarak **ölçek çarpanını otomatik tespit eder**  
- Tabloları ayıklayıp `Period x Item` formatında pivot DataFrame’lere dönüştürür  
- Bilanço, gelir tablosu, nakit akış tablosu için ayrı yükleyiciler  
- Her şirket için tüm dönemleri tek DataFrame’de zaman serisi formatında döker  

---

## 📂 Klasör Yapısı

`FinancialTables/` klasörü altındaki **tüm .xls dosyaları**, klasör sayısı ve derinliği fark etmeksizin otomatik olarak taranır.

Örn:  
FinancialTables/FinancialTables_2025/FinancialTable_2025_1/THYAO_1430405_2025_1.xls

🧠 Kullanım Örneği
data_path = "C:/MERT/FinancialTables/"
kapfinance = FinancialDataManager(data_path)

✔ Mevcut ticker’ları listele
kapfinance.list_available_tickers()

✔ Bilanço çekme
df = kapfinance.get_balance_sheet("ASELS")
print(df)

✔ Gelir tablosu çekme (belirli dönem aralığı)
df = kapfinance.get_income_statement("THYAO", start="2020_03", end="2023_12")

✔ Nakit akış tablosu
kapfinance.get_cash_flow("ASELS")
