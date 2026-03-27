import yfinance as yf
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings

warnings.filterwarnings("ignore")

# CONFIGURATION
max_market_cap = 2_000_000_000  # $2B
min_roe = 20.0
min_roic = 20.0
max_debt_to_equity = 0.25
min_revenue_growth = 20.0
min_insider_ownership = 10.0
min_net_income_growth = 20.0
min_operating_margin = 15.0
min_eps_growth = 20.0

min_market_cap = 50_000_000
min_avg_volume = 50_000
min_price = 5.0

print("Building stock universe (S&P 600)...")
try:
    sp600 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_600_companies")[0]
    col = "Symbol" if "Symbol" in sp600.columns else sp600.columns[0]
    tickers = [t.replace(".", "-").strip() for t in sp600[col].tolist() if isinstance(t, str)]
    print(f"Loaded {len(tickers)} tickers from S&P 600")
except Exception as e:
    print("Failed to load S&P 600:", e)
    tickers = ["BOOT", "CALM", "CARG", "DOCN", "MWA", "PIPR", "SPSC", "TREX", "YOU"] # tiny fallback

def analyze(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if not info or info.get("regularMarketPrice", info.get("currentPrice")) is None: return None

        market_cap = info.get("marketCap", 0) or 0
        price = info.get("regularMarketPrice", info.get("currentPrice", 0))
        avg_volume = info.get("averageVolume", 0) or 0
        
        roe = (info.get("returnOnEquity") or 0) * 100
        operating_margin = (info.get("operatingMargins") or 0) * 100
        
        debt_to_equity = info.get("debtToEquity")
        if debt_to_equity is not None: debt_to_equity /= 100
            
        revenue_growth = (info.get("revenueGrowth") or 0) * 100
        earnings_growth = (info.get("earningsGrowth") or 0) * 100
        insider_pct = (info.get("heldPercentInsiders") or 0) * 100
        
        trailing_eps = info.get("trailingEps") or 0
        forward_eps = info.get("forwardEps") or 0
        eps_growth = ((forward_eps - trailing_eps) / trailing_eps * 100) if trailing_eps and forward_eps else earnings_growth
        
        # Approximate ROIC
        roic = roe # fallback
        try:
            income = stock.financials
            if income is not None and not income.empty:
                op_income = income.loc["Operating Income"].iloc[0] if "Operating Income" in income.index else income.loc["EBIT"].iloc[0]
                tax_rate = 0.21
                nopat = op_income * (1 - tax_rate)
                total_debt = info.get("totalDebt", 0) or 0
                balance = stock.balance_sheet
                eq = balance.loc["Stockholders Equity"].iloc[0] if balance is not None and "Stockholders Equity" in balance.index else (info.get("bookValue", 0) * info.get("sharesOutstanding", 0))
                cash = info.get("totalCash", 0) or 0
                ic = total_debt + eq - cash
                if ic > 0: roic = (nopat / ic) * 100
        except: pass

        checks = {
            "market_cap": min_market_cap <= market_cap <= max_market_cap,
            "price": price >= min_price,
            "volume": avg_volume >= min_avg_volume,
            "roe": roe >= min_roe,
            "roic": roic >= min_roic,
            "debt_equity": debt_to_equity is not None and debt_to_equity <= max_debt_to_equity,
            "revenue_growth": revenue_growth >= min_revenue_growth,
            "insider_ownership": insider_pct >= min_insider_ownership,
            "net_income_growth": earnings_growth >= min_net_income_growth,
            "operating_margin": operating_margin >= min_operating_margin,
            "eps_growth": eps_growth >= min_eps_growth
        }
        
        if all(checks.values()) or sum(checks.values()) >= 8:
            return {
                "ticker": ticker,
                "price": price,
                "passed": sum(checks.values()),
                "failed": [k for k,v in checks.items() if not v]
            }
    except: pass
    return None

results = []
print("Screening...")
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(analyze, t): t for t in tickers}
    for i, f in enumerate(as_completed(futures)):
        res = f.result()
        if res: results.append(res)
        if i % 100 == 0: print(f"Progress: {i}/{len(tickers)}")

passed = [r for r in results if r["passed"] == 11]
near = [r for r in results if r["passed"] < 11]

print(f"\n--- PASSED ALL 11 FILTERS ({len(passed)}) ---")
for p in passed: print(p["ticker"])

print(f"\n--- NEAR MISSES (Passed 8+ Filters) ({len(near)}) ---")
for n in sorted(near, key=lambda x: x["passed"], reverse=True)[:10]:
    print(f"{n['ticker']} (Passed {n['passed']}/11) -> Failed: {', '.join(n['failed'])}")
