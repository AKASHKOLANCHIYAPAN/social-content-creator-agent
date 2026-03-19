# Social Content Creator Agent

An agentic autonomous system that detects real-time trending topics, generates AI-powered social media content, and distributes it automatically — every 2 hours, zero cost, zero manual effort.

---

## What It Does

This system runs fully autonomously on GitHub's cloud servers. Every 2 hours it wakes up, finds what's trending in the news, writes an engaging social media post using AI, generates a matching image, and sends everything to a Telegram channel — without any human involvement.

---

## Architecture

```
GitHub Actions (scheduler — every 2 hours)
        ↓
Agent 1 — Trend Detection Agent
        ↓
Agent 2 — Content Creation Agent
        ↓
Agent 3 — Distribution Agent
        ↓
Telegram Channel + SQLite Log
```

---

## 3 Agents

### Agent 1 — Trend Detection Agent
Fetches the top 10 real-time trending news headlines from Google News RSS feed for India. No API key required. If the feed fails, it falls back to a default topic list automatically.

**Tool used:** `feedparser`

### Agent 2 — Content Creation Agent
Takes the trend list from Agent 1 and runs 3 internal steps:
- Picks the most relevant and fresh topic using Groq AI
- Writes an engaging social media post under 250 characters with 2-3 hashtags
- Self-reviews the post for quality (agentic loop — retries up to 3 times if it fails)
- Generates a matching image using Pollinations.ai

**Tools used:** `Groq API (llama-3.1-8b-instant)`, `Pollinations.ai`, `used_topics.txt` for deduplication

### Agent 3 — Distribution Agent
Takes the approved post and image from Agent 2 and:
- Sends the post + image to a Telegram channel
- Logs every run to a local SQLite database with topic, post text, character count, status, and timestamp

**Tools used:** `python-telegram-bot`, `SQLite`

---

## Free Tech Stack

| Component | Tool | Cost |
|---|---|---|
| Scheduler | GitHub Actions | Free |
| Trend Detection | Google News RSS + feedparser | Free |
| AI Content Generation | Groq API (llama-3.1-8b-instant) | Free |
| Image Generation | Pollinations.ai | Free |
| Distribution | Telegram Bot | Free |
| Logging | SQLite | Free |
| Hosting | GitHub Actions Ubuntu Runner | Free |

**Total monthly cost: $0**

---

## Project Structure

```
social-content-creator-agent/
│
├── agents/
│   ├── trend_agent.py          # Agent 1 — fetches real trending topics
│   ├── content_agent.py        # Agent 2 — generates post + image
│   └── distribution_agent.py  # Agent 3 — sends to Telegram + logs
│
├── .github/
│   └── workflows/
│       └── scheduler.yml       # GitHub Actions cron schedule
│
├── main.py                     # Master pipeline — wires all 3 agents
├── requirements.txt            # All dependencies
└── .gitignore                  # Excludes .env, logs, cache
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

### 6. Run locally
```bash
python main.py
```

### 7. Deploy to GitHub Actions
- Push your code to GitHub
- Go to Settings → Secrets and variables → Actions
- Add these 3 secrets:
  - `GROQ_API_KEY`
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`
- Go to Actions tab → Social Media Agent → Run workflow

---

## How the Scheduler Works

The system uses a GitHub Actions cron job defined in `.github/workflows/scheduler.yml`:

```yaml
on:
  schedule:
    - cron: '0 */2 * * *'
  workflow_dispatch:
```

This triggers the pipeline every 2 hours automatically on GitHub's servers. `workflow_dispatch` lets you trigger it manually anytime from the Actions tab.

---

## Sample Output

```
Pipeline started at 2026-03-19 13:38:50
Agent 1: Found 10 real trending topics
Agent 2: Best topic → Ugadi 2026
Agent 2: Post approved after 1 attempt(s)
Agent 2: Image saved as image.jpg
Agent 3: Sent image + text to Telegram!
Agent 3: Logged to database → status: success
Pipeline finished! Status → success
```

---

## Key Features

- Fully autonomous — no manual effort after setup
- Real-time trend detection from Google News
- AI self-review loop — regenerates content if quality check fails
- Topic deduplication — never posts the same topic twice in a row
- Graceful fallback — system continues even if one component fails
- Complete audit trail — every post logged to SQLite with timestamp
- Zero cost — runs entirely on free tiers

---

## Built With

- Python 3.11
- Groq API
- feedparser
- Pollinations.ai
- python-telegram-bot
- GitHub Actions

---

## Author

Akash Kolanchiyapan
Mini Project — Semester 4
Agentic Autonomous System for Real-Time Content Creation and Distribution
