import yahooFinance from 'yahoo-finance2';
const yf = yahooFinance; // default export handles it in v2, but if failing, we use the constructor if needed. Wait, in v2.11+ it is just import yahooFinance from 'yahoo-finance2' and use yahooFinance.historical.
// Let's use the older format or fetch directly.
