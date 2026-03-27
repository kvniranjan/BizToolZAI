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
    const ticker = 'SPY';
    const res = await fetchYahoo(ticker, '1d', '2y');
    
    if (!res.chart || !res.chart.result) {
        console.log("Failed to fetch");
        return;
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
    
    function testStrategy(period, name) {
        const inputRSI = { values: prices, period: period };
        const rsiArray = RSI.calculate(inputRSI);
        
        let capital = 200.0;
        let position = 0.0;
        let trades = 0;
        let buyDate = null;
        let holdingPeriods = [];
        
        for (let i = 0; i < rsiArray.length; i++) {
            let rsi = rsiArray[i];
            let price = prices[i + period]; 
            let date = new Date(validData[i + period].time * 1000);
            
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
        
        let finalPrice = prices[prices.length - 1];
        let finalVal = capital > 0 ? capital : position * finalPrice;
        let bnhVal = (200.0 / prices[period]) * finalPrice;
        let avgHold = holdingPeriods.length > 0 ? holdingPeriods.reduce((a,b)=>a+b)/holdingPeriods.length : 0;
        
        console.log(`\n--- ${name} ---`);
        console.log(`Final Balance: $${finalVal.toFixed(2)} (Buy & Hold: $${bnhVal.toFixed(2)})`);
        console.log(`Total Completed Trades: ${holdingPeriods.length}`);
        console.log(`Average Holding Period: ${avgHold.toFixed(1)} days`);
    }

    testStrategy(14, "14-Day RSI (Slow & Steady)");
    testStrategy(7, "7-Day RSI (Faster Swings)");
    testStrategy(5, "5-Day RSI (Aggressive Swings)");
}
run();
