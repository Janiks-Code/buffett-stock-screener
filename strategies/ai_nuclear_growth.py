import yfinance as yf
import pandas as pd

THEME_STOCKS = [
    "META", "MSFT", "NVDA", "PLTR", "TSLA",
    "CEG", "GEV",
    "ACHR", "LUNR", "NBIS",
    "NKE", "PCG"
]

def run_ai_nuclear_screen():
    results = []

    for ticker in THEME_STOCKS:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            revenue_growth = info.get("revenueGrowth")
            profit_margin = info.get("profitMargins")
            debt = info.get("totalDebt", 0)
            market_cap = info.get("marketCap")

            if (
                revenue_growth is not None and revenue_growth > 0.10 and
                profit_margin is not None and profit_margin > 0.10 and
                market_cap is not None and market_cap > 5e9
            ):
                results.append({
                    "Ticker": ticker,
                    "Revenue Growth": round(revenue_growth * 100, 1),
                    "Profit Margin": round(profit_margin * 100, 1),
                    "Market Cap ($B)": round(market_cap / 1e9, 1)
                })

        except Exception:
            continue

    return pd.DataFrame(results)
