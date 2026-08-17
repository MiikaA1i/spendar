import os
import logging
from google import genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def generate_summary(summary_data: dict) -> str:
    """Send financial metrics to Gemini and receive a summary."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Variables not set. Skipping summary"

    client = genai.Client(api_key=api_key)

    top_categories = summary_data.get("top_categories", {})
    top_categories_str = ", ".join(
        f"{category}: ${amount:,.2f}" for category, amount in top_categories.items()
    ) or "None"

    prompt = f"""
    You are a senior personal finance assistant. Analyse the following spending metrics and provide
    a concise, 3-bullet-point summary highlighting spending behavior, key categories and actionable advice.

    Metrics:
    - Total Spent: ${summary_data.get('total_spent') or 0:,.2f}
    - Total Transactions: {summary_data.get('transaction_count') or 0}
    - Average Transaction: ${summary_data.get('average_transaction') or 0:,.2f}
    - Top Spending Categories: {top_categories_str}
    - Flagged Anomalies Count: {summary_data.get('anomalies_count') or 0}
    """

    try:
        interaction = client.interactions.create(
            model="gemini-3.1-flash-lite",
            input=prompt,
        )
        text = interaction.output_text
        if not text:
            logger.warning("Gemini returned an empty response")
            return "⚠️ AI summary was empty. Try again."
        return text.strip()
    except Exception as e:
        logger.exception("Failed to generate AI summary")
        return f"⚠️ Failed to generate AI summary: {str(e)}"