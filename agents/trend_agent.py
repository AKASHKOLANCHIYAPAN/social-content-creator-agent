import feedparser

def get_trends(max_topics=10):
    print("Agent 1: Fetching real trending topics...")

    try:
        url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(url)

        if not feed.entries:
            raise Exception("No entries found in feed")

        trends_list = []
        for entry in feed.entries[:max_topics]:
            title = entry.title
            if " - " in title:
                title = title.split(" - ")[0].strip()
            trends_list.append(title)

        print(f"Agent 1: Found {len(trends_list)} real trending topics")
        print(f"Agent 1: Topics -> {trends_list}")
        return trends_list

    except Exception as e:
        print(f"Agent 1: Error fetching trends -> {e}")
        fallback = ["AI", "ChatGPT", "iPhone 17", "Python", "Tech news"]
        print(f"Agent 1: Using fallback topics -> {fallback}")
        return fallback

if __name__ == "__main__":
    topics = get_trends()
    print("\nFinal output:", topics)
