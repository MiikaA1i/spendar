import pandas as pd

# =========================
# LOADING DATA
# =========================

def load_transactions(filepath: str) -> pd.DataFrame:
    """Load CSV and convert date column to datetime objects."""
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"])
    return df


# =========================
# TOTAL ANALYSIS
# =========================

def calculate_total(df: pd.DataFrame) -> dict:
    """Calculate baseline spending metrics."""
    return {
        "total_spent": round(float(df["amount"].sum()), 2),
        "total_transactions": int(len(df)),
        "average_transaction": round(float(df["amount"].mean()), 2),
    }
# =========================
# SPENDING ANALYSIS
# =========================
def category_breakdown(df: pd.DataFrame) -> dict:
    """Calculate spending grouped by category."""
    return (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
        .to_dict()
    )
# =========================
# AVERAGE ANALYSIS
# =========================
def filtered_breakdown(df: pd.DataFrame, multiplier: float = 1.5) -> pd.DataFrame:
    """Find transactions significantly higher than average."""
    avg = df["amount"].mean()
    return df[df["amount"] > (avg * multiplier)]

def detect_anomalies(df: pd.DataFrame, threshold_multiplier: float = 2.0) -> pd.DataFrame:
    """Identify spending anomalies based on transactions"""
    if df.empty:
        return pd.DataFrame()

    mean_val = df["amount"].abs().mean()
    threshold = mean_val * threshold_multiplier

    anomalies = df[df["amount"].abs() >= threshold].copy()

    if not anomalies.empty:
        anomalies["multiplier"] = (anomalies["amount"].abs() / mean_val).round(1)

    return anomalies

# =========================
# DUPLICATE ANALYSIS
# =========================

def find_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Find duplicate transactions based on identical values."""
    return df[df.duplicated(keep=False)]

# =========================
# MONTHLY ANALYSIS
# =========================

def monthly_breakdown(df: pd.DataFrame) -> dict:
    """Calculating Monthly Spendings"""
    df_copy = df.copy()
    df_copy["month"] = df_copy["date"].dt.strftime("%B")
    return (
        df_copy.groupby("month", sort=False)["amount"]
        .sum()
        .round(2)
        .to_dict()
    )

def monthly_trends(df: pd.DataFrame) -> dict:
    """Calculating percentages change between the months"""
    df_copy = df.copy()
    df_copy["month"] = df_copy["date"].dt.strftime("%B")

    monthly_totals = df_copy.groupby("month", sort=False)["amount"].sum()
    pct_changes = monthly_totals.pct_change() * 100

    trends ={}
    months = list(monthly_totals.index)

    for i in range (1, len (months)):
        pct_m, curr_m = months[i-1], months[i]
        change = pct_changes.iloc[i]
        trends[f"{curr_m} vs {pct_m}"] = round(float(change), 1)

    return trends
