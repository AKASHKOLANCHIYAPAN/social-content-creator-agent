# Social Content Creator Agent

An agentic autonomous system that detects real-time trending topics, generates AI-powered social media content, and distributes it automatically across Telegram and Instagram — zero cost, zero manual effort.

---

## What It Does

This system runs fully autonomously on GitHub's cloud servers. Every 45 minutes it fetches what is trending in the news, writes an engaging social media post using AI, and sends it to Telegram. Every 2 hours it additionally generates a headline-edited image and posts it to Instagram with a detailed caption — all without any human involvement.

---

## Architecture

```
GitHub Actions (scheduler)
        ↓
Agent 1 — Trend Detection Agent
        ↓
Agent 2 — Content Creation Agent
        ↓
Agent 3 — Distribution Agent
        ↓
Telegram (every 45 mins) + Instagram (every 2 hours) + SQLite Log
```

---

## 3 Agents

### Agent 1 — Trend Detection Agent
Fetches the top 10 real-time trending news headlines from Google News RSS feed for India. No API key required. If the feed fails, it falls back to a default topic list automatically.

**Tool used:** `feedparser`

### Agent 2 — Content Creation Agent
Takes the trend list from Agent 1 and runs 4 internal steps:
- Picks the most relevant and fresh topic using Groq AI with topic deduplication
- Writes an engaging social media post under 250 characters with 2-3 hashtags
- Self-reviews the post for quality (agentic loop — retries up to 3 times if it fails)
- Generates a base image using Pollinations.ai with Picsum.photos as fallback
- Overlays the headline text and timestamp directly onto the image using Pillow

**Tools used:** `Groq API (llama-3.1-8b-instant)`, `Pollinations.ai`, `Picsum.photos`, `Pillow`, `used_topics.txt`

### Agent 3 — Distribution Agent
Takes the approved post and edited image from Agent 2 and:
- Sends clean text only to Telegram channel
- Posts the headline-edited image with detailed caption to Instagram
- Logs every run to SQLite database with topic, content, timestamp, and status

**Tools used:** `python-telegram-bot`, `instagrapi`, `SQLite`

---

## Free Tech Stack

| Component | Tool | Cost |
|---|---|---|
| Scheduler | GitHub Actions | Free |
| Trend Detection | Google News RSS + feedparser | Free |
| AI Content Generation | Groq API (llama-3.1-8b-instant) | Free |
| Image Generation | Pollinations.ai + Picsum.photos fallback | Free |
| Image Editing | Pillow | Free |
| Telegram Distribution | python-telegram-bot | Free |
| Instagram Distribution | instagrapi | Free |
| Logging | SQLite | Free |
| Hosting | GitHub Actions Ubuntu Runner | Free |

**Total monthly cost: $0**

---

## Project Structure

```
social-content-creator-agent/
│
├── agents/
│   ├── trend_agent.py           # Agent 1 — fetches real trending topics
│   ├── content_agent.py         # Agent 2 — generates post + edited image
│   └── distribution_agent.py   # Agent 3 — posts to Telegram + Instagram + logs
│
├── .github/
│   └── workflows/
│       └── scheduler.yml        # Two separate cron schedules
│
├── posts/                       # Locally saved edited post images (timestamped)
├── main.py                      # Master pipeline — wires all 3 agents
├── requirements.txt             # All dependencies
└── .gitignore                   # Excludes .env, logs, cache, session, images
```

---

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/AKASHKOLANCHIYAPAN/social-content-creator-agent.git
cd social-content-creator-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```
GROQ_API_KEY="your_groq_api_key"
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
TELEGRAM_CHAT_ID="your_telegram_chat_id"
INSTAGRAM_USERNAME="your_instagram_username"
INSTAGRAM_PASSWORD="your_instagram_password"
```

### 5. Get free API keys

**Groq API** (free, 14400 requests/day)
- Go to console.groq.com
- Sign up and create an API key

**Telegram Bot**
- Open Telegram and message @BotFather
- Type /newbot and follow the steps
- Copy the token you receive
- Message your bot once, then visit:
  `https://api.telegram.org/bot<TOKEN>/getUpdates`
- Copy the chat id from the response

**Instagram**
- Use a personal Instagram account
- Disable two-factor authentication before first run
- A session file is saved automatically after first login — no repeated challenges

### 6. Run locally
```bash
python main.py
```

### 7. Deploy to GitHub Actions
- Push your code to GitHub
- Go to Settings → Secrets and variables → Actions
- Add these 5 secrets:
  - `GROQ_API_KEY`
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`
  - `INSTAGRAM_USERNAME`
  - `INSTAGRAM_PASSWORD`
- Go to Actions tab → Social Media Agent → Run workflow

---

## How the Scheduler Works

The system uses two separate cron jobs in `.github/workflows/scheduler.yml`:

```yaml
on:
  schedule:
    - cron: '*/45 * * * *'
    - cron: '0 5,7,9,11,13,15,17,19,21,23,1,3 * * *'
  workflow_dispatch:
```

The `POST_PLATFORM` environment variable controls which platform posts each cycle:
- `telegram` — sends text only to Telegram
- `instagram` — generates edited image and posts to Instagram
- `both` — posts to both (default when running manually)

---

## How Instagram Image Editing Works

Every Instagram post uses a generated base image with the headline and timestamp overlaid directly using Pillow:

```
Base image fetched (Pollinations.ai or Picsum.photos fallback)
        ↓
Dark overlay added at bottom of image
        ↓
Headline text written on overlay (white, wrapped)
        ↓
Date and time written at bottom (grey)
        ↓
Saved as posts/post_YYYYMMDD_HHMMSS.jpg
        ↓
Posted to Instagram with detailed caption
```

---

## Platform Behavior

| Platform | Content | Schedule |
|---|---|---|
| Telegram | Clean text post only | Every 45 minutes |
| Instagram | Headline-edited image + detailed caption | Every 2 hours (12 posts/day) |

---

## Sample Output

```
Pipeline started at 2026-03-22 10:42:05
Agent 1: Found 10 real trending topics
Agent 2: Best topic → Iran-Israel war LIVE
Agent 2: Post approved after 1 attempt(s)
Agent 2: Base image saved as image.jpg
Agent 2: Headline and date added to image successfully!
Agent 3: Sent text to Telegram!
Agent 3: Instagram login successful!
Agent 3: Posted to Instagram successfully!
Agent 3: Logged to database → status: success
Pipeline finished! Status → success
```

---

## Key Features

- Fully autonomous — no manual effort after setup
- Real-time trend detection from Google News RSS
- AI self-review loop — regenerates content if quality check fails
- Topic deduplication — never repeats the same topic across cycles
- Three-level image fallback — Pollinations → Pollinations 512px → Picsum
- Headline and timestamp baked directly into Instagram images using Pillow
- Instagram session caching — no repeated login challenges
- Graceful fallback — pipeline completes even if individual components fail
- Complete audit trail — every post logged to SQLite with timestamp
- Separate posting schedules per platform
- Zero cost — runs entirely on free tiers

---

## Built With

- Python 3.11
- Groq API
- feedparser
- Pollinations.ai + Picsum.photos
- Pillow
- python-telegram-bot
- instagrapi
- GitHub Actions
- SQLite

---

## Author

Akash Kolanchiyapan
Mini Project — Semester 4
Agentic Autonomous System for Real-Time Content Creation and Distribution over Social Media Platforms