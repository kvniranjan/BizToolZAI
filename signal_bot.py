import yfinance as yf
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
warnings.filterwarnings("ignore")

tickers = [
    "YOU", "CARG", "DUOL", "PLMR", "MWA", "CELH", "BOOT", "CALM", 
    "DOCN", "PIPR", "SPSC", "TREX", "UPWK", "FSLY", "FVRR", "NET", 
    "OKTA", "PINS", "SNOW", "MED"
]

def get_fundamentals(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if not info or info.get("regularMarketPrice", info.get("currentPrice")) is None: return None
        roe = (info.get("returnOnEquity") or 0) * 100
        rev_growth = (info.get("revenueGrowth") or 0) * 100
        
        if roe > 15:
            return {"ticker": ticker, "roe": roe, "rev_growth": rev_growth}
    except:
        pass
    return None

results = []
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(get_fundamentals, t): t for t in tickers}
    for f in as_completed(futures):
        res = f.result()
        if res:
            results.append(res)

results.sort(key=lambda x: x["roe"], reverse=True)

buy_target = None
sell_targets = []

for stock_data in results:
    ticker = stock_data["ticker"]
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1mo")
        if len(df) < 10: continue
        
        delta = df['Close'].diff()
        gain = delta.clip(lower=0)
        loss = -1 * delta.clip(upper=0)
        
        avg_gain = gain.ewm(com=4, adjust=False).mean()
        avg_loss = loss.ewm(com=4, adjust=False).mean()
        
        rs = avg_gain / avg_loss
        df['RSI_5'] = 100 - (100 / (1 + rs))
        
        latest_rsi = df['RSI_5'].iloc[-1]
        latest_price = df['Close'].iloc[-1]

        if latest_rsi < 40 and buy_target is None:
            buy_target = {
                "ticker": ticker,
                "price": latest_price,
                "rsi": latest_rsi,
                "roe": stock_data["roe"]
            }
        
        if latest_rsi > 60:
            sell_targets.append({
                "ticker": ticker,
                "price": latest_price,
                "rsi": latest_rsi
            })
    except Exception as e:
        continue

print("=========================================")
print("🎯 THE WATERFALL SNIPER BOT")
print("=========================================\n")

if buy_target:
    stop_loss_price = buy_target['price'] * 0.90
    print("🚨 BUY ALERT (Deploy Full $200) 🚨")
    print(f"Target: {buy_target['ticker']}")
    print(f"Price: ${buy_target['price']:.2f} | 5-Day RSI: {buy_target['rsi']:.1f}")
    print(f"Why: Highest ranked fundamental stock (ROE: {buy_target['roe']:.1f}%) that is currently oversold.")
    print(f"🛡️ RISK MGMT: Set a 10% Stop Loss at ${stop_loss_price:.2f} immediately after buying.\n")
else:
    print("⏳ NO BUY TARGETS TODAY ⏳")
    print("None of our high-quality stocks are currently oversold (RSI < 40). Keep cash idle.\n")

if sell_targets:
    print("💰 SELL ALERTS (If Holding) 💰")
    for s in sell_targets:
        print(f"Sell: {s['ticker']} | Price: ${s['price']:.2f} | RSI: {s['rsi']:.1f} (Overbought)")
else:
    print("No overbought stocks to sell today.")

print("\n=========================================")
