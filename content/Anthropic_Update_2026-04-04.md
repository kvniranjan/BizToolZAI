# Anthropic Just Dropped a 300K Token Output Upgrade. Here's Why Your Spreadsheets Will Thank You.

**By [Your AI Assistant], channeling Joanna Stern**

Imagine asking an AI to analyze an entire year's worth of messy corporate financial reports and getting back... half a report, because the AI literally ran out of breath. Frustrating, right? 

Well, Business Analysts, rejoice. This week, Anthropic rolled out an update that fixes exactly that. They've raised the `max_tokens` cap to a whopping 300,000 on the Message Batches API for Claude Opus 4.6 and Sonnet 4.6. 

### Why Should You Care?
If you're not a developer, "Message Batches API" sounds like tech-jargon alphabet soup. But here's the translation: Claude can now generate *massive* single-turn outputs. We're talking long-form content, giant structured data dumps, and endless spreadsheets without stopping midway to ask, "Should I continue?"

Before this, Claude was great at reading big documents (thanks to its massive context window), but it was artificially limited in how much it could *write back* to you at once. Now, it can spit out comprehensive, end-to-end business intelligence reports or format 50-page unstructured PDFs into perfectly clean CSVs in one go.

### How to Use It Today
If you are using Claude via API (or through an internal company tool powered by it):
1. **Batch Your Work:** Gather those giant quarterly review PDFs or messy datasets.
2. **Add the Magic Word:** Have your dev team include the `output-300k-2026-03-24` beta header in your tool's API requests.
3. **Ask for the World:** Prompt Claude to restructure the entire dataset into structured JSON or CSV. Don't hold back on the length.

It's basically like giving your smartest, fastest intern a bottomless pot of coffee. Go forth and analyze!
