import os
import pandas as pd
import pytest
from unittest.mock import patch
from financial_data_manager import FinancialDataManager


# -------------------------------------------------------------------
# Helper: Sahte tablo üretici
# -------------------------------------------------------------------
def fake_html_table(desc_text, value_text, scale_text="1 TL"):
    """
    pd.read_html() çıktısına benzeyen sahte DataFrame listesi döndürür.
    """
    df_scale = pd.DataFrame({
        "A": [scale_text],
        "B": [""]
    })

    df_data = pd.DataFrame({
        "col0": ["X", "X"],
        "col1": ["AÇIKLAMA", desc_text],
        "col2": ["X", "X"],
        "col3": ["DEĞER", value_text],
    })

    return [df_scale, df_data]


# -------------------------------------------------------------------
# Mock read_html çağrısı
# -------------------------------------------------------------------
@patch("pandas.read_html")
def test_balance_sheet_loading(mock_read_html, tmp_path):
    """
    Finansal durum tablosu için parse test.
    """
    # Fake HTML table
    mock_read_html.return_value = fake_html_table(
        desc_text="Nakit ve Nakit Benzerleri",
        value_text="1.234"
    )

    # Test klasörü
    folder = tmp_path / "kap"
    folder.mkdir()

    # Fake XLS file
    fake_file = folder / "THYAO_2023_03.xls"
    fake_file.write_text("<html></html>")

    manager = FinancialDataManager(str(folder))

    # Load balance sheet
    df = manager.get_balance_sheet("THYAO")

    assert df is not None
    assert "Nakit ve Nakit Benzerleri" in df.columns
    assert df.iloc[0]["Nakit ve Nakit Benzerleri"] == 1234.0


# -------------------------------------------------------------------
# Ticker listesi test
# -------------------------------------------------------------------
def test_list_tickers(tmp_path):
    folder = tmp_path / "kap2"
    folder.mkdir()

    (folder / "ASELS_2022_12.xls").write_text("<html></html>")
    (folder / "KCHOL_2023_03.xls").write_text("<html></html>")

    manager = FinancialDataManager(str(folder))

    tickers = manager.list_available_tickers()

    assert len(tickers) == 2
    assert set(tickers) == {"ASELS", "KCHOL"}


# -------------------------------------------------------------------
# Ölçek (scale) tespiti testi
# -------------------------------------------------------------------
@patch("pandas.read_html")
def test_scale_detection(mock_read_html, tmp_path):
    mock_read_html.return_value = [
        pd.DataFrame({"A": ["Sunum Para Birimi 1.000 TL"], "B": [""]}),
        pd.DataFrame({
            "x": ["X", "X"],
            "y": ["AÇIKLAMA", "Varlıklar"],
            "z": ["X", "X"],
            "t": ["DEĞER", "5.000"],
        })
    ]

    folder = tmp_path / "kap"
    folder.mkdir()

    fake_file = folder / "SAHOL_2023_03.xls"
    fake_file.write_text("<html></html>")

    manager = FinancialDataManager(str(folder))
    df = manager.get_balance_sheet("SAHOL")

    # 5000 * 1000 = 5,000,000
    assert df.iloc[0]["Varlıklar"] == 5_000_000


# -------------------------------------------------------------------
# Hatalı dosya / tablo bulunamazsa sorun çıkmamalı
# -------------------------------------------------------------------
@patch("pandas.read_html", side_effect=Exception("read error"))
def test_read_error(mock_read_html, tmp_path):
    folder = tmp_path / "kap"
    folder.mkdir()
    (folder / "HALKB_2024_01.xls").write_text("<html></html>")

    manager = FinancialDataManager(str(folder))
    df = manager.get_balance_sheet("HALKB")

    # Başarısız okuma null döndürür ama çökmez
    assert df is None
