const https = require('https');
const { RSI, SMA } = require('technicalindicators');

async function fetchYahoo(ticker, interval, range) {
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?range=${range}&interval=${interval}`;
    return new Promise((resolve, reject) => {
        https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (resp) => {
            let data = '';
            resp.on('data', chunk => data += chunk);
            resp.on('end', () => resolve(JSON.parse(data)));
        }).on('error', reject);
    });
}

async function run() {
    const tickers = ['YOU', 'CARG', 'DUOL', 'PLMR', 'MWA'];
    
    for (let ticker of tickers) {
        const res = await fetchYahoo(ticker, '1d', '2y');
        
        if (!res.chart || !res.chart.result) {
            console.log(`Failed to fetch ${ticker}`);
            continue;
        }

        const timestamps = res.chart.result[0].timestamp;
        const closes = res.chart.result[0].indicators.quote[0].close;
        
        const validData = [];
        for (let i = 0; i < closes.length; i++) {
            if (closes[i] !== null) {
                validData.push({ time: timestamps[i], price: closes[i] });
            }
        }
        
        const prices = validData.map(d => d.price);
        
        // Indicators
        const rsiPeriod = 5;
        const rsiArray = RSI.calculate({ values: prices, period: rsiPeriod });
        
        const smaPeriod = 20;
        const smaArray = SMA.calculate({ values: prices, period: smaPeriod });
        
        let capital = 200.0;
        let position = 0.0;
        let trades = 0;
        let buyDate = null;
        let holdingPeriods = [];
        
        // We need to align the arrays since SMA starts later than RSI
        const offset = Math.max(rsiPeriod, smaPeriod);
        
        for (let i = 0; i < prices.length - offset; i++) {
            let rsiIdx = i + (offset - rsiPeriod);
            let smaIdx = i + (offset - smaPeriod);
            
            let rsi = rsiArray[rsiIdx];
            let sma = smaArray[smaIdx];
            let price = prices[i + offset]; 
            let date = new Date(validData[i + offset].time * 1000);
            
            // BUY: RSI < 40 (Oversold Dip)
            if (rsi < 40 && capital > 0) {
                position = capital / price;
                capital = 0.0;
                buyDate = date;
                trades++;
            } 
            // SELL LOGIC
            else if (position > 0) {
                // Trend Filter: 
                // If price is ABOVE the 20-day SMA (strong uptrend), we hold until extreme overbought (RSI > 80)
                // If price is BELOW the 20-day SMA (weak/downtrend), we sell quickly at normal overbought (RSI > 60)
                let isUptrend = price > sma;
                let sellTrigger = isUptrend ? (rsi > 80) : (rsi > 60);
                
                if (sellTrigger) {
                    capital = position * price;
                    position = 0.0;
                    let daysHeld = (date - buyDate) / (1000 * 60 * 60 * 24);
                    holdingPeriods.push(daysHeld);
                    buyDate = null;
                    trades++;
                }
            }
        }
        
        let finalPrice = prices[prices.length - 1];
        let finalVal = capital > 0 ? capital : position * finalPrice;
        let bnhVal = (200.0 / prices[offset]) * finalPrice;
        let avgHold = holdingPeriods.length > 0 ? holdingPeriods.reduce((a,b)=>a+b)/holdingPeriods.length : 0;
        
        console.log(`\n--- ${ticker} (5-Day RSI + 20-Day SMA Trend Filter) ---`);
        console.log(`Final Balance (Bot): $${finalVal.toFixed(2)}`);
        console.log(`Final Balance (Buy & Hold): $${bnhVal.toFixed(2)}`);
        console.log(`Total Completed Trades: ${holdingPeriods.length}`);
        console.log(`Average Holding Period: ${avgHold.toFixed(1)} days`);
    }
}
run();
