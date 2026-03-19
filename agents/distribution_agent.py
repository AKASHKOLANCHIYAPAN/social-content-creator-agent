import sqlite3
import os
import asyncio
import telegram
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def init_db():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            tweet TEXT,
            characters INTEGER,
            status TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Agent 3: Database ready")


def log_to_db(topic, tweet, status):
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO posts (topic, tweet, characters, status, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (topic, tweet, len(tweet), status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    print(f"Agent 3: Logged to database → status: {status}")


async def send_to_telegram(topic, tweet, image_path):
    bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    message = f"""
🤖 Auto-generated post

📌 Topic: {topic}

{tweet}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """

    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as img:
            await bot.send_photo(
                chat_id=chat_id,
                photo=img,
                caption=message
            )
        print("Agent 3: Sent image + text to Telegram!")
    else:
        await bot.send_message(chat_id=chat_id, text=message)
        print("Agent 3: Sent text only to Telegram!")


def run_distribution_agent(topic, tweet, image_path=None):
    print("Agent 3: Starting distribution...")

    init_db()

    try:
        asyncio.run(send_to_telegram(topic, tweet, image_path))
        status = "success"
    except Exception as e:
        print(f"Agent 3: Failed → {e}")
        status = "failed"

    log_to_db(topic, tweet, status)
    print(f"Agent 3: Done! Status → {status}")
    return status


if __name__ == "__main__":
    sample_topic = "ChatGPT"
    sample_tweet = "AI is transforming how we work. #ChatGPT #AI #FutureOfWork"
    status = run_distribution_agent(sample_topic, sample_tweet, "image.jpg")
    print("\n--- Final Output ---")
    print(f"Status : {status}")