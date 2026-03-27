import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings

warnings.filterwarnings("ignore")

# Using a hardcoded list of high-volume small/mid caps since Wikipedia blocks the direct scrape
tickers = [
    "CELH", "PLMR", "MED", "BOOT", "CALM", "CARG", "DOCN", "MWA", "PIPR", "SPSC", 
    "TREX", "YOU", "UPWK", "DUOL", "FSLY", "FVRR", "NET", "OKTA", "PINS", "SNOW"
]

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
        
        return {
            "ticker": ticker,
            "price": round(price, 2),
            "roe": round(roe, 1),
            "rev_growth": round(revenue_growth, 1),
            "eps_growth": round(eps_growth, 1),
            "op_margin": round(operating_margin, 1)
        }
    except Exception as e:
        return None

results = []
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(analyze, t): t for t in tickers}
    for f in as_completed(futures):
        res = f.result()
        if res: results.append(res)

print(f"\n--- STOCK METRICS ({len(results)}) ---")
for r in sorted(results, key=lambda x: x["roe"], reverse=True):
    print(f"{r['ticker']}: Price ${r['price']} | ROE: {r['roe']}% | Rev Growth: {r['rev_growth']}% | EPS Growth: {r['eps_growth']}% | Margin: {r['op_margin']}%")
