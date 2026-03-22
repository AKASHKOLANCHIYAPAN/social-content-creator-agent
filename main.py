from agents.trend_agent import get_trends
from agents.content_agent import run_content_agent
from agents.distribution_agent import run_distribution_agent
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


def run_pipeline():
    print("=" * 50)
    print(f"Pipeline started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    platform = os.getenv("POST_PLATFORM", "both")
    print(f"Platform mode → {platform}")
    print("=" * 50)

    # step 1: agent 1 fetches trends
    trends = get_trends()
    if not trends:
        print("Pipeline: No trends found, stopping.")
        return

    # step 2: agent 2 generates content
    topic, tweet, image_path = run_content_agent(trends)
    if not tweet:
        print("Pipeline: No tweet generated, stopping.")
        return

    # step 3: agent 3 distributes based on platform
    status = run_distribution_agent(topic, tweet, image_path, platform)

    print("=" * 50)
    print(f"Pipeline finished! Status → {status}")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()