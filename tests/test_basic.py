from kapfinance import FinancialDataManager


def test_init():
    manager = FinancialDataManager(".")
    assert manager is not None