from groq import Groq
import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=1.2,
        top_p=0.9
    )
    return response.choices[0].message.content.strip()


def pick_best_topic(trends_list):
    print("Agent 2: Picking best topic from trends...")
    random.shuffle(trends_list)
    prompt = f"""
    You manage a social media account covering news and current events.
    From this list of trending topics, pick ONE random interesting topic.
    Every time you are called, pick a DIFFERENT topic.
    Return ONLY the topic name, nothing else. No explanation.

    Trending topics: {trends_list}
    """
    topic = ask_groq(prompt)
    print(f"Agent 2: Best topic → {topic}")
    return topic
def load_used_topics():
    if os.path.exists("used_topics.txt"):
        with open("used_topics.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    return []


def save_used_topic(topic):
    with open("used_topics.txt", "a") as f:
        f.write(topic + "\n")


def pick_best_topic(trends_list):
    print("Agent 2: Picking best topic from trends...")

    # load previously used topics
    used_topics = load_used_topics()

    # filter out already used topics
    fresh_topics = [t for t in trends_list if t not in used_topics]

    # if all topics used, reset the file and start fresh
    if not fresh_topics:
        print("Agent 2: All topics used, resetting history...")
        open("used_topics.txt", "w").close()
        fresh_topics = trends_list

    random.shuffle(fresh_topics)

    prompt = f"""
    You manage a social media account covering news and current events.
    From this list of trending topics, pick ONE interesting topic.
    Return ONLY the topic name exactly as written, nothing else.

    Trending topics: {fresh_topics}
    """
    topic = ask_groq(prompt)

    # save this topic so it won't be used again
    save_used_topic(topic)

    print(f"Agent 2: Best topic → {topic}")
    return topic


def generate_tweet(topic):
    print(f"Agent 2: Generating post for '{topic}'...")
    prompt = f"""
    Write an engaging social media post about: {topic}

    Rules:
    - Maximum 250 characters
    - Include 2-3 relevant hashtags at the end
    - Use an engaging hook at the start
    - Informative and professional tone
    - No emojis
    - Return ONLY the post text, nothing else
    """
    tweet = ask_groq(prompt)
    print(f"Agent 2: Generated post → {tweet}")
    return tweet


def quality_check(tweet):
    print("Agent 2: Running quality check...")
    prompt = f"""
    Review this social media post and respond with ONLY "PASS" or "FAIL":

    Post: "{tweet}"

    Check:
    - Is it under 280 characters?
    - Does it have 2-3 hashtags?
    - Is the tone professional?
    - Is it engaging?

    Reply with ONLY the word PASS or FAIL. Nothing else.
    """
    result = ask_groq(prompt).upper()
    print(f"Agent 2: Quality check result → {result}")
    return "PASS" in result


def generate_image(topic):
    print("Agent 2: Generating image...")

    urls = [
        "https://image.pollinations.ai/prompt/modern+technology+news+background+professional+clean?width=1024&height=1024&nologo=true",
        "https://image.pollinations.ai/prompt/abstract+digital+background+blue+professional?width=512&height=512&nologo=true",
    ]

    for attempt, url in enumerate(urls, 1):
        try:
            print(f"Agent 2: Image attempt {attempt}...")
            response = requests.get(url, timeout=90)
            if response.status_code == 200:
                with open("image.jpg", "wb") as f:
                    f.write(response.content)
                print("Agent 2: Image saved as image.jpg")
                return "image.jpg"
            else:
                print(f"Agent 2: Attempt {attempt} failed → {response.status_code}")
        except Exception as e:
            print(f"Agent 2: Attempt {attempt} error → {e}")

    print("Agent 2: All image attempts failed, continuing without image")
    return None


def run_content_agent(trends_list):
    # step 1: pick best topic
    topic = pick_best_topic(trends_list)

    # step 2: generate post with retry loop
    max_attempts = 3
    tweet = None
    for attempt in range(1, max_attempts + 1):
        print(f"Agent 2: Attempt {attempt} of {max_attempts}")
        tweet = generate_tweet(topic)
        if quality_check(tweet):
            print(f"Agent 2: Post approved after {attempt} attempt(s)")
            break
        else:
            print(f"Agent 2: Post failed quality check, regenerating...")

    # step 3: generate image
    image_path = generate_image(topic)

    return topic, tweet, image_path


if __name__ == "__main__":
    from trend_agent import get_trends
    real_trends = get_trends()
    topic, tweet, image_path = run_content_agent(real_trends)
    print("\n--- Final Output ---")
    print(f"Topic      : {topic}")
    print(f"Post       : {tweet}")
    print(f"Length     : {len(tweet)} characters")
    print(f"Image path : {image_path}")