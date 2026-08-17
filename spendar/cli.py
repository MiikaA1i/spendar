import typer
from pathlib import Path
from .analyser import (
    load_transactions,
    calculate_total,
    category_breakdown,
    filtered_breakdown,
    monthly_breakdown,
    monthly_trends,
    detect_anomalies,
)
from .reporter import (
    display_baseline,
    display_categories,
    display_transactions,
    display_monthly,
    display_trends,
    display_anomalies,
    display_summary,
)

from .ai import generate_summary

app = typer.Typer()


@app.callback()
def callback():
    pass


@app.command()
def analyze(
    filepath: str,
    ai: bool = typer.Option(False, "--ai", help="Generate AI-powered spending insights"),
):
    """Analyze a transaction CSV file."""
    path = Path(filepath)

    # --- Validation: catch bad input before touching pandas ---
    if not path.exists():
        typer.secho(f"Error: file not found: {filepath}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if path.suffix.lower() != ".csv":
        typer.secho(f"Error: expected a .csv file, got: {path.suffix}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    try:
        df = load_transactions(filepath)
    except ValueError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if df.empty:
        typer.secho("Error: the CSV file is empty.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    # --- End validation ---

    # Baseline
    metrics = calculate_total(df)
    display_baseline(metrics)

    # Categories
    categories = category_breakdown(df)
    display_categories(categories)

    # Large transactions
    large_transactions = filtered_breakdown(df)
    display_transactions(
        large_transactions,
        "Above Average Transactions"
    )

    # Monthly spendings
    display_monthly(monthly_breakdown(df))

    # Monthly trends
    display_trends(monthly_trends(df))

    # Anomalies
    anomalies = detect_anomalies(df)
    display_anomalies(anomalies)

    # AI
    if ai:
        ai_payload = {
            "total_spent": metrics.get("total_spent"),
            "total_transactions": metrics.get("total_transactions"),
            "average_transaction": metrics.get("average_transaction"),
            "top_categories": categories,
            "anomalies_count": len(anomalies),
        }
        summary = generate_summary(ai_payload)
        display_summary(summary)


if __name__ == "__main__":
    app()