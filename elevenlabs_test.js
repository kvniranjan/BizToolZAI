const axios = require('axios');

const API_KEY = '2430b417f4d4a39161a9164953d80c62ff4d5cf19734e73a9dba9094ac474949';

async function testElevenLabs() {
    try {
        const response = await axios.get('https://api.elevenlabs.io/v1/user', {
            headers: {
                'xi-api-key': API_KEY
            }
        });
        
        console.log("✅ ElevenLabs API Key is Valid!");
        console.log(`Subscription Tier: ${response.data.subscription.tier}`);
        console.log(`Character Count Remaining: ${response.data.subscription.character_limit - response.data.subscription.character_count}`);
    } catch (error) {
        console.error("❌ ElevenLabs API Key Test Failed:", error.response ? error.response.data : error.message);
    }
}

testElevenLabs();
