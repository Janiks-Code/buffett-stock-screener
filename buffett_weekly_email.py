pip install yfinance pandas schedule
import yfinance as yf
import pandas as pd
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

# ----------------------------
# CONFIGURATION
# ----------------------------

STOCK_UNIVERSE = [
    "AAPL", "MSFT", "KO", "PEP", "JNJ", "PG", "V", "MA",
    "BRK-B", "COST", "ADBE", "TXN", "UNH", "CVX", "XOM"
]

EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
RECIPIENT_EMAIL = "recipient_email@gmail.com"

# ----------------------------
# BUFFETT SCREEN
# ----------------------------

def passes_buffett_criteria(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        pe = info.get("trailingPE")
        roe = info.get("returnOnEquity")
        debt_to_equity = info.get("debtToEquity")
        current_ratio = info.get("currentRatio")
        price_to_book = info.get("priceToBook")
        free_cash_flow = info.get("freeCashflow")

        if None in [pe, roe, debt_to_equity, current_ratio, price_to_book]:
            return None

        if (
            pe <= 25 and
            roe >= 0.15 and
            debt_to_equity <= 60 and
            current_ratio >= 1.5 and
            price_to_book <= 4 and
            free_cash_flow and free_cash_flow > 0
        ):
            return {
                "Ticker": ticker,
                "P/E": round(pe, 2),
                "ROE": round(roe * 100, 2),
                "Debt/Equity": round(debt_to_equity, 2),
                "Current Ratio": round(current_ratio, 2),
                "P/B": round(price_to_book, 2)
            }
    except Exception:
        return None

    return None

# ----------------------------
# SCAN FUNCTION
# ----------------------------

def run_buffett_screen():
    results = []

    for ticker in STOCK_UNIVERSE:
        data = passes_buffett_criteria(ticker)
        if data:
            results.append(data)

    return pd.DataFrame(results)

# ----------------------------
# EMAIL FUNCTION
# ----------------------------

def send_email(df):
    subject = f"📈 Buffett-Style Stock Picks – {date.today()}"
    body = "No stocks met the criteria this week."

    if not df.empty:
        body = df.to_string(index=False)

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

# ----------------------------
# WEEKLY JOB
# ----------------------------

def weekly_job():
    df = run_buffett_screen()
    send_email(df)

# Run every Monday at 9 AM
schedule.every().monday.at("09:00").do(weekly_job)

print("📬 Buffett stock screener running...")

while True:
    schedule.run_pending()
    time.sleep(60)
