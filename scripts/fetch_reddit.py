#!/usr/bin/env python3
"""
fetch_reddit.py - Fetch posts from app/game marketing subreddits using Reddit's public JSON API.

Usage:
    python scripts/fetch_reddit.py --year 2026 --output /tmp/reddit_raw.json
    python scripts/fetch_reddit.py --year 2026 --limit 50 --output /tmp/reddit_raw.json
    python scripts/fetch_reddit.py --year 2026 --subreddits gamedev,IndieDev --output /tmp/reddit_raw.json

No authentication required (uses Reddit's public JSON API).
"""

import argparse
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone


MARKETING_SUBREDDITS = [
    # App launch & business
    "SideProject",
    "AppBusiness",
    "startups",
    "entrepreneur",
    "growthhacking",
    # Lifestyle & productivity apps (key for non-game apps)
    "productivity",
    "selfimprovement",
    "DecidingToBeBetter",
    "getdisciplined",
    "Journaling",
    "bulletjournal",
    # Mobile dev
    "iOSProgramming",
    "androiddev",
    # Game dev (for general marketing pattern reference)
    "gamedev",
    "IndieDev",
]

# Keywords that signal marketing success stories — require concrete outcome words
# to avoid false positives like "looking for feedback" being counted as success
SUCCESS_SIGNAL_KEYWORDS = [
    "just launched", "just shipped", "just released", "just hit",
    "we reached", "i launched", "i released", "i shipped",
    "first month", "first week", "revenue", "downloads", "installs",
    "post-mortem", "case study", "lessons learned",
    "hit 1k", "hit 10k", "hit 100k", "passed 1000", "passed 10k",
    "made $", "earned $", "generated $",
]

# Keywords that signal marketing pain points — must clearly indicate struggle,
# not just any question (avoid short words like "help" that cause false positives)
PAIN_SIGNAL_KEYWORDS = [
    "how to promote", "how to market", "how to get users", "how to get downloads",
    "no downloads", "zero downloads", "nobody downloads", "nobody installs",
    "no traction", "no users", "can't get users", "can't find users",
    "launch failed", "flopped", "struggling to", "nobody cares about my",
    "discoverability", "invisible on", "buried in",
]

HEADERS = {
    "User-Agent": "AppGameMarketingResearch/1.0 (educational research tool)",
}


def fetch_subreddit_posts(subreddit: str, limit: int = 25, sort: str = "top",
                          target_year: int | None = None) -> list[dict]:
    """Fetch posts from a subreddit using Reddit's public JSON API.

    When target_year is the current year or previous year, uses t=year (past 12 months).
    For older years, uses t=all with client-side filtering — note Reddit's public API
    returns up to ~1000 top posts, so older year coverage may be incomplete.
    """
    current_year = datetime.now(timezone.utc).year
    time_filter = "year" if target_year is None or target_year >= current_year - 1 else "all"
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}&t={time_filter}"
    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            posts = data.get("data", {}).get("children", [])
            return [p["data"] for p in posts]
    except Exception as e:
        print(f"  Warning: Failed to fetch r/{subreddit}: {e}")
        return []


def classify_post(post: dict) -> str:
    """Classify post as 'success', 'pain_point', or 'general'."""
    title = post.get("title", "").lower()
    flair = (post.get("link_flair_text") or "").lower()
    text = title + " " + flair

    if any(kw in text for kw in SUCCESS_SIGNAL_KEYWORDS):
        return "success"
    if any(kw in text for kw in PAIN_SIGNAL_KEYWORDS):
        return "pain_point"
    return "general"


def filter_by_year(post: dict, year: int) -> bool:
    """Filter posts created in the given year."""
    created = post.get("created_utc", 0)
    post_year = datetime.fromtimestamp(created, tz=timezone.utc).year
    return post_year == year


def score_post(post: dict) -> int:
    """Engagement score combining upvotes and comment count."""
    return post.get("score", 0) + post.get("num_comments", 0) * 3


def main():
    parser = argparse.ArgumentParser(description="Fetch app/game marketing subreddit posts")
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="Target year for filtering posts (default: current year)")
    parser.add_argument("--limit", type=int, default=25,
                        help="Max posts to fetch per subreddit (default: 25)")
    parser.add_argument("--output", type=str, default="/tmp/reddit_raw.json",
                        help="Output JSON file path")
    parser.add_argument("--subreddits", type=str, default=None,
                        help="Comma-separated subreddit list (default: built-in marketing list)")
    args = parser.parse_args()

    subreddits = args.subreddits.split(",") if args.subreddits else MARKETING_SUBREDDITS
    target_year = args.year

    print(f"Fetching posts from {len(subreddits)} subreddits for year {target_year}...")

    all_posts = []
    success_posts = []
    pain_posts = []

    for sub in subreddits:
        print(f"  Fetching r/{sub}...")
        posts = fetch_subreddit_posts(sub, limit=args.limit, sort="top", target_year=target_year)

        for post in posts:
            if not filter_by_year(post, target_year):
                continue

            category = classify_post(post)
            entry = {
                "subreddit": sub,
                "title": post.get("title", ""),
                "selftext": post.get("selftext", "")[:600],
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "flair": post.get("link_flair_text", ""),
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "created_utc": post.get("created_utc", 0),
                "engagement_score": score_post(post),
                "category": category,
            }
            all_posts.append(entry)
            if category == "success":
                success_posts.append(entry)
            elif category == "pain_point":
                pain_posts.append(entry)

        time.sleep(1)  # be polite to Reddit's API

    all_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    success_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    pain_posts.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "target_year": target_year,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_posts": len(all_posts),
        "success_posts_count": len(success_posts),
        "pain_point_posts_count": len(pain_posts),
        "subreddits_searched": subreddits,
        "top_success_stories": success_posts[:30],
        "top_pain_points": pain_posts[:30],
        "all_posts": all_posts[:100],
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Fetched {len(all_posts)} posts: "
          f"{len(success_posts)} success stories, {len(pain_posts)} pain points.")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()
