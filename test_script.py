import os, google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")
prompt = """
Write a 60-second YouTube Shorts script for 'The Broke Economist' about the 'Buy, Borrow, Die' billionaire tax loophole.
The voiceover is an insider who is exposing the rigged system. 
CRITICAL: The tone MUST have a dark, cynical, and highly humorous touch. Think 'The Big Short' meets 'WallStreetBets'. 
No generic intros. Just hard-hitting, funny truth.
Include visual cues in brackets [like this].
"""
print(model.generate_content(prompt).text)
