import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .analyser import (
    load_transactions,
    calculate_total,
    category_breakdown,
    filtered_breakdown,
    find_duplicates,
    monthly_trends,
    detect_anomalies,
)

console = Console()

# =========================
# DISPLAY FUNCTIONS
# =========================

def display_baseline(metrics: dict):
    """Display baseline spending metrics as a table."""
    table = Table(title="💰 Baseline", title_style="bold cyan", border_style="cyan")
    table.add_column("Metric", style="white")
    table.add_column("Value", justify="right", style="bold green")

    table.add_row("Total Spent", f"${metrics['total_spent']:,.2f}")
    table.add_row("Transactions", str(metrics["total_transactions"]))
    table.add_row("Average Transaction", f"${metrics['average_transaction']:,.2f}")

    console.print(table)


def display_categories(categories: dict):
    """Display category breakdown as a table."""
    table = Table(title="📂 Category Breakdown", title_style="bold cyan", border_style="cyan")
    table.add_column("Category", style="white")
    table.add_column("Total Spent", justify="right", style="bold green")

    for category, amount in categories.items():
        table.add_row(category, f"${amount:,.2f}")

    console.print(table)


def display_transactions(df: pd.DataFrame, title: str):
    """Display transactions DataFrame as a Rich table."""
    if df.empty:
        return

    table = Table(title=f"📋 {title}", title_style="bold cyan", border_style="cyan")

    # Format dates cleanly without 00:00:00 timestamps
    df_display = df.copy()
    if "date" in df_display.columns:
        df_display["date"] = df_display["date"].dt.strftime("%Y-%m-%d")

    for column in df_display.columns:
        style = "bold green" if column == "amount" else "white"
        table.add_column(str(column).capitalize(), style=style)

    for _, row in df_display.iterrows():
        table.add_row(*[str(value) for value in row])

    console.print(table)


def display_monthly(monthly_data: dict):
    """Displaying Monthly Spending Breakdown"""
    table = Table(title="📅 Monthly Spending", title_style="bold cyan", border_style="cyan")
    table.add_column("Month", style="white")
    table.add_column("Total Spent", justify="right", style="bold green")

    for month, amount in monthly_data.items():
        table.add_row(month, f"${amount:,.2f}")

    console.print(table)


def display_trends(trends: dict):
    """Displaying month-over-month Spending"""
    table = Table(title="📈 Monthly Trends", title_style="bold cyan", border_style="cyan")
    table.add_column("Comparison", style="white")
    table.add_column("Change", justify="right")

    for comparison, change in trends.items():
        if change > 0:
            style = "bold yellow"
            sign = "+"
        elif change < 0:
            style = "bold green"
            sign = ""
        else:
            style = "white"
            sign = ""
        table.add_row(comparison, f"[{style}]{sign}{change:.1f}%[/{style}]")

    console.print(table)


def display_anomalies(anomalies: pd.DataFrame):
    """Displaying flagged transaction anomalies"""

    if anomalies.empty:
        console.print("[bold green]✓ No spending anomalies detected.[/bold green]")
        return

    table = Table(title="🚨 DETECTED ANOMALIES", title_style="bold red", border_style="red")
    table.add_column("Date", style="white")
    table.add_column("Description", style="white")
    table.add_column("Category", style="white")
    table.add_column("Amount", justify="right", style="bold red")
    table.add_column("Impact", justify="right", style="bold red")

    for _, row in anomalies.iterrows():
        table.add_row(
            str(row["date"].strftime("%Y-%m-%d")),
            str(row["description"]),
            str(row["category"]),
            f"${row['amount']:.2f}",
            f"{row['multiplier']}x average",
        )

    console.print(table)

# =========================
# AI DISPLAY
# =========================
def display_summary(summary_text: str):
    """Rendering AI summary in a styled panel."""
    console.print(
        Panel(
            summary_text,
            title="✨ AI Spendar Insight",
            title_align="left",
            border_style="cyan",
            expand=False,
            padding=(1, 2),
        )
    )

# =========================
# RUNNER / ENTRYPOINT
# =========================

def generate_report(filepath: str):
    """Runs the entire display pipeline for a given CSV file path."""
    df = load_transactions(filepath)

    display_baseline(calculate_total(df))
    display_transactions(find_duplicates(df), "Duplicate Transactions")
    display_categories(category_breakdown(df))
    display_transactions(filtered_breakdown(df), "Above Average Transactions")


if __name__ == "__main__":
    generate_report(
        r"C:\Users\malai\OneDrive\Desktop\Capstone Projects\spendar\sample\transactions.csv"
    )