import pandas as pd
import pytest

from spendar.analyser import (
    load_transactions,
    calculate_total,
    category_breakdown,
)


@pytest.fixture
def sample_csv(tmp_path):
    """Create a small, known transaction CSV for predictable test assertions."""
    csv_content = (
        "date,amount,category,description\n"
        "2026-01-01,50.00,Groceries,Woolworths\n"
        "2026-01-05,200.00,Rent,Landlord\n"
        "2026-01-10,15.00,Coffee,Local Cafe\n"
        "2026-01-15,500.00,Electronics,Laptop\n"
        "2026-01-20,30.00,Groceries,Coles\n"
    )
    filepath = tmp_path / "transactions.csv"
    filepath.write_text(csv_content)
    return str(filepath)


def test_csv_loads(sample_csv):
    """CSV loads into a DataFrame with the expected shape and a parsed date column."""
    df = load_transactions(sample_csv)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert list(df.columns) == ["date", "amount", "category", "description"]


def test_total_calculated_correctly(sample_csv):
    """Total spent sums all transaction amounts correctly."""
    df = load_transactions(sample_csv)
    metrics = calculate_total(df)

    expected_total = 50.00 + 200.00 + 15.00 + 500.00 + 30.00  # 795.00
    assert metrics["total_spent"] == pytest.approx(expected_total)
    assert metrics["total_transactions"] == 5


def test_average_calculated_correctly(sample_csv):
    """Average transaction is total divided by transaction count."""
    df = load_transactions(sample_csv)
    metrics = calculate_total(df)

    expected_average = (50.00 + 200.00 + 15.00 + 500.00 + 30.00) / 5  # 159.0
    assert metrics["average_transaction"] == pytest.approx(expected_average)


def test_category_totals_calculated_correctly(sample_csv):
    """Category breakdown sums amounts per category correctly."""
    df = load_transactions(sample_csv)
    categories = category_breakdown(df)

    assert categories["Groceries"] == pytest.approx(80.00)   # 50 + 30
    assert categories["Rent"] == pytest.approx(200.00)
    assert categories["Coffee"] == pytest.approx(15.00)
    assert categories["Electronics"] == pytest.approx(500.00)


def test_largest_transaction_identified(sample_csv):
    """The largest single transaction is correctly identified."""
    df = load_transactions(sample_csv)
    idx = df["amount"].idxmax()

    assert df.at[idx, "amount"] == pytest.approx(500.00)
    assert df.at[idx, "category"] == "Electronics"
    assert df.at[idx, "description"] == "Laptop"