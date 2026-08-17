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
    You are a friendly, supportive money coach helping someone understand their spending in plain,
    everyday language. Avoid financial jargon (no "discretionary consumption," "cash flow," "cooling-off
    periods," etc). Write like you're talking to a friend over coffee — warm, clear, and encouraging,
    not clinical or judgmental.

    Give a short, 3-bullet-point summary that:
    1. Describes their spending pattern in simple terms
    2. Points out where most of their money went
    3. Gives one easy, practical tip — not a lecture

    Keep each bullet to 1-2 short sentences. No bold headers, no financial-advisor tone.

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