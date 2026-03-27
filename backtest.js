const https = require('https');
async function run() {
    const tickers = ['SPY'];
    const period1 = Math.floor(Date.now() / 1000) - (2 * 365 * 24 * 60 * 60);
    const period2 = Math.floor(Date.now() / 1000);
    const { RSI } = require('technicalindicators');

    for (let ticker of tickers) {
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?period1=${period1}&period2=${period2}&interval=1d`;
        const res = await new Promise((resolve, reject) => {
            https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (resp) => {
                let data = '';
                resp.on('data', chunk => data += chunk);
                resp.on('end', () => resolve(JSON.parse(data)));
            }).on('error', reject);
        });
        
        if (!res.chart || !res.chart.result) {
            console.log("Failed to fetch data for", ticker);
            continue;
        }

        const timestamps = res.chart.result[0].timestamp;
        const closes = res.chart.result[0].indicators.quote[0].close;
        
        // Filter out nulls
        const validData = [];
        for (let i = 0; i < closes.length; i++) {
            if (closes[i] !== null) {
                validData.push({ time: timestamps[i], price: closes[i] });
            }
        }
        
        const prices = validData.map(d => d.price);
        const inputRSI = { values: prices, period: 14 };
        const rsiArray = RSI.calculate(inputRSI);
        
        let capital = 200.0;
        let position = 0.0;
        let trades = 0;
        
        let buyDate = null;
        let holdingPeriods = [];
        
        for (let i = 0; i < rsiArray.length; i++) {
            let rsi = rsiArray[i];
            let price = prices[i + 14]; 
            let date = new Date(validData[i + 14].time * 1000);
            
            if (rsi < 40 && capital > 0) {
                position = capital / price;
                capital = 0.0;
                buyDate = date;
                trades++;
            } else if (rsi > 60 && position > 0) {
                capital = position * price;
                position = 0.0;
                let daysHeld = (date - buyDate) / (1000 * 60 * 60 * 24);
                holdingPeriods.push(daysHeld);
                buyDate = null;
                trades++;
            }
        }
        
        let avgHold = holdingPeriods.length > 0 ? holdingPeriods.reduce((a,b)=>a+b)/holdingPeriods.length : 0;
        let maxHold = holdingPeriods.length > 0 ? Math.max(...holdingPeriods) : 0;
        let minHold = holdingPeriods.length > 0 ? Math.min(...holdingPeriods) : 0;
        
        console.log(`\n--- ${ticker} REAL DATA BACKTEST ---`);
        console.log(`Average Holding Period: ${avgHold.toFixed(1)} days`);
        console.log(`Longest Trade Held: ${maxHold.toFixed(0)} days`);
        console.log(`Shortest Trade Held: ${minHold.toFixed(0)} days`);
        console.log(`Total Completed Trades (Buy/Sell Pairs): ${holdingPeriods.length}`);
    }
}
run();
