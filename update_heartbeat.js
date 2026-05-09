const fs = require('fs');
const path = '/root/.openclaw/workspace/memory/heartbeat-state.json';
let state = { lastChecks: {} };
if (fs.existsSync(path)) {
  state = JSON.parse(fs.readFileSync(path, 'utf8'));
}
state.lastChecks.youtube = Math.floor(Date.now() / 1000);
fs.writeFileSync(path, JSON.stringify(state, null, 2));
