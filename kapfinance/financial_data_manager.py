import numpy as np
import pandas as pd
import os
import logging
import re

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class FinancialDataManager:
    """
    Loads and structures financial statement data from exported KAP .xls files.
    Supports: Balance Sheet, Income Statement, Comprehensive Income, Cash Flow.
    """
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self._file_map = self._build_file_map()

        # Cached Data Stores
        self.balance_sheet_data = {}
        self.income_statement_data = {}
        self.comprehensive_income_statement_data = {}
        self.cash_flow_data = {}

    # --------------------------------------------------------------
    # Detect scale from "Sunum Para Birimi"
    # --------------------------------------------------------------
    def _detect_scale_from_tables(self, tables):
        try:
            df = tables[0]  # İlk tablo genelde scale bilgisini içerir.

            for i in range(len(df)):
                row_text = " ".join(df.iloc[i].astype(str).values).lower()

                if "sunum para birimi" in row_text:
                    # Örnek: "1.000 TL", "1000 TL", "1.000.000 TL"
                    match = re.search(r'([\d\.\,]+)\s*tl', row_text)
                    if match:
                        num = match.group(1).replace('.', '').replace(',', '.')
                        try:
                            return float(num)
                        except:
                            return 1

                    # Sadece TL yazıyorsa → scale = 1
                    if "tl" in row_text:
                        return 1

        except:
            pass

        return 1  # Varsayılan

    # --------------------------------------------------------------
    # Build file structure map (period from filename)
    # --------------------------------------------------------------
    def _build_file_map(self) -> dict:
        file_map = {}

        if not os.path.isdir(self.folder_path):
            logging.error(f"Folder '{self.folder_path}' not found.")
            return file_map

        logging.info(f"Indexing .xls files under '{self.folder_path}'...")

        for root, _, files in os.walk(self.folder_path):
            for filename in files:
                if not filename.lower().endswith('.xls'):
                    continue

                # ✅ Extract ticker: everything before first "_"
                match_ticker = re.match(r'^([^_]+)', filename)
                if not match_ticker:
                    continue
                ticker = match_ticker.group(1).upper()

                # ✅ Extract period: last year + quarter/period inside filename
                match_period = re.search(r'(\d{4})[_\-]?(\d{1,2})(?=\.xls|$)', filename)
                if not match_period:
                    continue

                year = match_period.group(1)
                quarter = match_period.group(2).zfill(2)
                period = f"{year}_{quarter}"

                file_path = os.path.join(root, filename)
                file_map.setdefault(ticker, {}).setdefault(period, []).append(file_path)

        logging.info(f"Indexed {len(file_map)} tickers.")
        return file_map

    # --------------------------------------------------------------
    # Table extraction
    # --------------------------------------------------------------
    def _extract_table(self, file_path: str, keywords: list[str]):
        try:
            tables = pd.read_html(file_path, encoding="utf-8", flavor="lxml")
        except Exception as e:
            logging.warning(f"Failed to read '{file_path}': {e}")
            return None, 1

        scale = self._detect_scale_from_tables(tables)

        for df in tables:
            combined_text = " ".join(df.astype(str).values.ravel()).lower()
            if any(keyword.lower() in combined_text for keyword in keywords):
                try:
                    desc_col = df.iloc[:, 1]
                    val_col = df.iloc[:, 3]
                except:
                    return None, scale

                extracted = []
                for desc, val in zip(desc_col, val_col):
                    if not (pd.isna(desc) or pd.isna(val)):
                        extracted.append((str(desc).strip(), str(val).strip(), scale))
                return extracted, scale

        return None, scale

    # --------------------------------------------------------------
    # Generic loader
    # --------------------------------------------------------------
    def _load_data(self, ticker: str, keywords: list[str], target_store: dict):
        ticker = ticker.upper()

        if ticker in target_store:
            return

        if ticker not in self._file_map:
            logging.warning(f"No files found for ticker '{ticker}'.")
            return

        logging.info(f"Loading data for '{ticker}'...")
        target_store[ticker] = []

        for period, files in self._file_map[ticker].items():
            for file in files:
                records, scale = self._extract_table(file, keywords)
                if records:
                    for (desc, val, scale) in records:
                        target_store[ticker].append(((desc, val, scale), period))

    # --------------------------------------------------------------
    # Explicit loaders
    # --------------------------------------------------------------
    def load_balance_sheet_data(self, ticker): 
        self._load_data(ticker, ["Finansal Durum Tablosu (Bilanço)"], self.balance_sheet_data)

    def load_income_statement_data(self, ticker): 
        self._load_data(ticker, ["Kar veya Zarar Tablosu"], self.income_statement_data)

    def load_comprehensive_income_statement_data(self, ticker): 
        self._load_data(ticker, ["Diğer Kapsamlı Gelir Tablosu"], self.comprehensive_income_statement_data)

    def load_cash_flow_data(self, ticker): 
        self._load_data(ticker, ["Nakit Akış Tablosu (Dolaylı Yöntem)"], self.cash_flow_data)

    # --------------------------------------------------------------
    # Data formatting into pivoted DataFrames
    # --------------------------------------------------------------
    def _format_dataframe(self, raw, start=None, end=None):
        rows = []

        for ((desc, val, scale), period) in raw:
            if start and period < start:
                continue
            if end and period > end:
                continue

            try:
                numeric_val = float(val.replace('.', '').replace(',', '.')) * scale
            except:
                numeric_val = np.nan

            rows.append((period, desc, numeric_val))

        if not rows:
            return None

        df = pd.DataFrame(rows, columns=['Period', 'Description', 'Value'])

        df = df.pivot_table(
            index='Period',
            columns='Description',
            values='Value',
            aggfunc='first'
        )

        df = df.sort_index(key=lambda periods: [tuple(map(int, p.split('_'))) for p in periods])
        return df

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------
    def get_balance_sheet(self, ticker, start=None, end=None):
        self.load_balance_sheet_data(ticker)
        return self._format_dataframe(self.balance_sheet_data.get(ticker, []), start, end)

    def get_income_statement(self, ticker, start=None, end=None):
        self.load_income_statement_data(ticker)
        return self._format_dataframe(self.income_statement_data.get(ticker, []), start, end)

    def get_comprehensive_income_statement(self, ticker, start=None, end=None):
        self.load_comprehensive_income_statement_data(ticker)
        return self._format_dataframe(self.comprehensive_income_statement_data.get(ticker, []), start, end)

    def get_cash_flow(self, ticker, start=None, end=None):
        self.load_cash_flow_data(ticker)
        return self._format_dataframe(self.cash_flow_data.get(ticker, []), start, end)

    def list_available_tickers(self) -> list:
        return list(self._file_map.keys())


if __name__ == "__main__":
    data_path = "C:/MERT/FinancialTables/"
    kapfinance = FinancialDataManager(data_path)