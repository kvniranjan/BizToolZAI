# 🏭 Operations Dashboard

## 📊 Tracking
- **Master Log:** [affiliate_log.csv](./affiliate_log.csv) (Logs all tools found, status, and verdict)
- **Content Approval:** [content_approval.csv](./content_approval.csv) (Approve/Reject daily posts before 10 PM)
- **Email List:** [email_subscribers.csv](./email_subscribers.csv) (Simple subscriber tracking)
- **Content Queue:** [content/](./content/) (Drafted tweets, posts, and scripts)

## 🤖 Automated Workflows (Cron Jobs)

### 1. 🌅 Product Hunt Morning Scan (08:00 UTC)
- **Goal:** Catch new AI launches early.
- **Action:** Scans top launches -> Checks for affiliate program -> Drafts "Early Adopter Alert".
- **Output:** Entry in `affiliate_log.csv`, Message to User.

### 2. ☀️ Reddit Opportunity Scout (14:00 UTC)
- **Goal:** Find high-intent leads.
- **Action:** Searches Reddit for "looking for ai tool" -> Drafts helpful replies.
- **Output:** Drafts in `content/social_replies_{date}.md`.

### 3. 🌙 Nightly Deep Research (19:00 UTC)
- **Goal:** Find trending tools & draft content.
- **Action:** Identifies tool -> Writes Review + Social Content -> Logs to `content_approval.csv`.
- **Output:** Draft in `content/`, Row in Approval CSV.

### 4. 🚀 Blog Auto-Publisher (22:00 UTC)
- **Goal:** Publish approved content to `biztoolzai.com`.
- **Action:** Checks `content_approval.csv` -> If NOT "Reject" -> Converts to HTML -> Pushes to GitHub.
- **Output:** Live site update.

## 📝 Manual Tasks
- "Check recent logs"
- "Approve today's post"
- "Run a specific search now"
