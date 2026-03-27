const axios = require('axios');
const API_KEY = '2430b417f4d4a39161a9164953d80c62ff4d5cf19734e73a9dba9094ac474949';

async function listVoices() {
    try {
        const response = await axios.get('https://api.elevenlabs.io/v1/voices', {
            headers: { 'xi-api-key': API_KEY }
        });
        
        console.log("Available Voices:");
        response.data.voices.slice(0, 5).forEach(v => {
            console.log(`- ${v.name} (ID: ${v.voice_id})`);
        });
    } catch (e) {
        console.error(e.message);
    }
}
listVoices();
