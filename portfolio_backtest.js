const https = require('https');
const { RSI } = require('technicalindicators');

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
    let marketData = {};
    let allDates = new Set();
    
    // Fetch and calculate RSI for all tickers
    for (let ticker of tickers) {
        const res = await fetchYahoo(ticker, '1d', '2y');
        if (!res.chart || !res.chart.result) continue;
        
        const timestamps = res.chart.result[0].timestamp;
        const closes = res.chart.result[0].indicators.quote[0].close;
        
        let prices = [];
        let validTimestamps = [];
        for (let i = 0; i < closes.length; i++) {
            if (closes[i] !== null) {
                prices.push(closes[i]);
                validTimestamps.push(timestamps[i]);
                allDates.add(timestamps[i]);
            }
        }
        
        const rsiArray = RSI.calculate({ values: prices, period: 5 });
        
        marketData[ticker] = {};
        for (let i = 0; i < rsiArray.length; i++) {
            marketData[ticker][validTimestamps[i + 5]] = {
                price: prices[i + 5],
                rsi: rsiArray[i]
            };
        }
    }
    
    let sortedDates = Array.from(allDates).sort((a, b) => a - b);
    
    function runStrategy(name, maxSlots) {
        let cash = 200.0;
        let positions = {};
        let tradesCount = 0;
        
        for (let date of sortedDates) {
            // Calculate total equity for sizing
            let currentEquity = cash;
            for (let tk in positions) {
                if (marketData[tk][date]) {
                    currentEquity += positions[tk] * marketData[tk][date].price;
                }
            }
            
            // 1. Sell Phase (RSI > 60)
            for (let tk in positions) {
                let dayData = marketData[tk][date];
                if (dayData && dayData.rsi > 60) {
                    cash += positions[tk] * dayData.price;
                    delete positions[tk];
                    tradesCount++;
                }
            }
            
            // Re-evaluate equity after sells
            currentEquity = cash;
            for (let tk in positions) {
                if (marketData[tk][date]) {
                    currentEquity += positions[tk] * marketData[tk][date].price;
                }
            }
            
            // 2. Buy Phase (RSI < 40)
            let tradeSize = currentEquity / maxSlots;
            let candidates = [];
            
            for (let tk of tickers) {
                if (!positions[tk] && marketData[tk] && marketData[tk][date]) {
                    if (marketData[tk][date].rsi < 40) {
                        candidates.push({ 
                            ticker: tk, 
                            rsi: marketData[tk][date].rsi, 
                            price: marketData[tk][date].price 
                        });
                    }
                }
            }
            
            // Sort by lowest RSI (buy the most bleeding stock first)
            candidates.sort((a, b) => a.rsi - b.rsi);
            
            for (let cand of candidates) {
                if (Object.keys(positions).length < maxSlots && cash >= tradeSize * 0.99) {
                    let amountToInvest = Math.min(cash, tradeSize);
                    positions[cand.ticker] = amountToInvest / cand.price;
                    cash -= amountToInvest;
                }
            }
        }
        
        // Final evaluation on the last day
        let finalDate = sortedDates[sortedDates.length - 1];
        let finalEquity = cash;
        for (let tk in positions) {
            if (marketData[tk][finalDate]) {
                finalEquity += positions[tk] * marketData[tk][finalDate].price;
            }
        }
        
        console.log(`\n--- ${name} ---`);
        console.log(`Final Balance: $${finalEquity.toFixed(2)}`);
        console.log(`Net Profit: ${((finalEquity - 200)/200 * 100).toFixed(2)}%`);
        console.log(`Total Trades Executed: ${tradesCount}`);
    }
    
    runStrategy("1. The Sniper (1x $200 Bullet)", 1);
    runStrategy("2. Two-Bullet (2x $100 Bullets)", 2);
    runStrategy("3. Equal Weight (5x $40 Bullets)", 5);
}
run();
