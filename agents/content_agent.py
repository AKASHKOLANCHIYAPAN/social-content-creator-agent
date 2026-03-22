from groq import Groq
import os
import requests
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime
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

    used_topics = load_used_topics()
    fresh_topics = [t for t in trends_list if t not in used_topics]

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


def generate_image():
    print("Agent 2: Fetching base image from Picsum...")

    try:
        url = "https://picsum.photos/1024/1024"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open("image.jpg", "wb") as f:
                f.write(response.content)
            print("Agent 2: Base image saved as image.jpg")
            return "image.jpg"
        else:
            print(f"Agent 2: Picsum failed → {response.status_code}")
            return None
    except Exception as e:
        print(f"Agent 2: Image fetch error → {e}")
        return None


def add_text_to_image(image_path, topic):
    print("Agent 2: Adding headline and date to image...")

    try:
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        overlay_height = int(height * 0.40)
        draw.rectangle(
            [(0, height - overlay_height), (width, height)],
            fill=(0, 0, 0, 190)
        )

        try:
            font_headline = ImageFont.truetype("arial.ttf", 32)
            font_date = ImageFont.truetype("arial.ttf", 22)
        except:
            font_headline = ImageFont.load_default()
            font_date = ImageFont.load_default()

        wrapped = textwrap.wrap(topic, width=38)
        y = height - overlay_height + 25
        for line in wrapped[:3]:
            draw.text((30, y), line, font=font_headline, fill=(255, 255, 255, 255))
            y += 42

        now = datetime.now().strftime("%d %B %Y  |  %H:%M")
        draw.text((30, height - 45), now, font=font_date, fill=(180, 180, 180, 255))

        combined = Image.alpha_composite(img, overlay).convert("RGB")

        os.makedirs("posts", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"posts/post_{timestamp}.jpg"
        combined.save(output_path, "JPEG", quality=95)
        print(f"Agent 2: Image saved as {output_path}")
        return output_path

    except Exception as e:
        print(f"Agent 2: Text overlay failed → {e}")
        return image_path


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

    # step 3: fetch image from picsum
    image_path = generate_image()

    # step 4: add headline + date on image
    if image_path:
        image_path = add_text_to_image(image_path, topic)

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