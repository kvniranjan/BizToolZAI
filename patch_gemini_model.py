file_path = '/root/.openclaw/workspace/be_pipeline_v2.py'
with open(file_path, 'r') as f:
    content = f.read()

content = content.replace("model = genai.GenerativeModel('gemini-1.5-flash')", "model = genai.GenerativeModel('gemini-2.5-flash')")

with open(file_path, 'w') as f:
    f.write(content)
print("Patched Gemini model version")
