const axios = require('axios');

const API_KEY = 'AIzaSyDtm_wNCZD77H5PsKs6Y_eG1jck9-FOc1k';

async function testGemini() {
    try {
        const response = await axios.post(
            `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`,
            {
                contents: [{ parts: [{ text: "Write a 1 sentence pitch for a YouTube channel about unsolved mysteries." }] }]
            },
            {
                headers: { 'Content-Type': 'application/json' }
            }
        );
        
        console.log("✅ Gemini API Key is Valid!");
        console.log("Response:", response.data.candidates[0].content.parts[0].text.trim());
    } catch (error) {
        console.error("❌ Gemini API Key Test Failed:", error.response ? error.response.data : error.message);
    }
}

testGemini();
