📊 kapfinance — FinancialDataManager

KAP’tan indirilen finansal tablo .xls dosyalarını otomatik okuma, ayrıştırma ve zaman serilerine dönüştürme aracı kapfinance, Kamuyu Aydınlatma Platformu’ndan (KAP) indirilen finansal tablo dosyalarını otomatik olarak tarayan, işleyen, ölçeklendiren ve pandas DataFrame formatında zaman serilerine dönüştüren bir Python paketidir.

Desteklenen rapor türleri:

Bilanço

Kar veya Zarar Tablosu

Diğer Kapsamlı Gelir Tablosu

Nakit Akış Tablosu

🚀 Kurulum

PyPI üzerinden yükleyebilirsiniz:

pip install kapfinance

🔧 Hızlı Başlangıç

import kapfinance as kf

data_path = r"C:\Data\FinancialTables"

kap = kf.FinancialDataManager(data_path)

📂 Klasör Yapısı

kapfinance, verdiğiniz dizin altında yer alan tüm alt klasörleri otomatik olarak tarar.
Alt dizinlerin sayısı, isimlendirme şekli veya klasör derinliği önemli değildir.

Örnek klasör yapısı:

FinancialTables/
    FinancialTables_2025/
        FinancialTable_2025_1/
            THYAO_1430405_2025_1.xls


🧠 Kullanım Örnekleri

📌 1) Mevcut Ticker’ları Listeleme

kap.list_available_tickers()

📌 2) Bilanço Çekme

df = kap.get_balance_sheet("ASELS")
print(df)

📌 3) Gelir Tablosu Çekme

df = kap.get_income_statement("THYAO")

📌 4) Belirli Dönem Aralığı

df = kap.get_income_statement("THYAO", start="2016_01", end="2020_04")

📌 5) Nakit Akış Tablosu

df = kap.get_cash_flow("ASELS")
