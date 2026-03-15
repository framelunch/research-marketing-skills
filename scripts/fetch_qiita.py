#!/usr/bin/env python3
"""
fetch_qiita.py - Fetch app/game marketing-related articles from Qiita via Qiita API v2.

Usage:
    python scripts/fetch_qiita.py --year 2026 --output /tmp/qiita_raw.json
    python scripts/fetch_qiita.py --year 2026 --min-likes 5 --output /tmp/qiita_raw.json
    python scripts/fetch_qiita.py --year 2026 --queries "個人開発,アプリ" --output /tmp/qiita_raw.json

Qiita API v2 is public and allows up to 60 requests/hour without authentication.
With a Qiita access token (QIITA_TOKEN env var), the limit increases to 1000 requests/hour.
"""

import argparse
import json
import os
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone


# Query terms for app/game marketing on Qiita (Japanese community)
MARKETING_QUERIES = [
    # Individual dev / launch
    "個人開発 リリース",
    "個人開発 マーケティング",
    "個人開発 収益",
    "アプリ リリース 個人開発",
    "個人開発 ユーザー獲得",
    "個人開発 宣伝",
    # App Store / Google Play
    "App Store 審査",
    "アプリ マーケティング",
    "ASO アプリ最適化",
    "iOS アプリ リリース",
    "Androidアプリ リリース",
    # Game dev
    "ゲーム 個人開発 リリース",
    "インディーゲーム マーケティング",
    # Promotion channels
    "アプリ 宣伝 SNS",
    "ProductHunt 個人開発",
    "個人開発 note Qiita 宣伝",
]

QIITA_API_BASE = "https://qiita.com/api/v2/items"


def fetch_qiita_articles(query: str, year: int, min_likes: int = 3,
                          per_page: int = 20, token: str | None = None) -> list[dict]:
    """Fetch Qiita articles matching a query within the given year."""
    # Qiita API supports created:>=YYYY-01-01 in query strings
    full_query = f"{query} created:>={year}-01-01 created:<={year}-12-31"
    params = urllib.parse.urlencode({
        "query": full_query,
        "per_page": per_page,
        "page": 1,
    })
    url = f"{QIITA_API_BASE}?{params}"

    headers = {"User-Agent": "AppGameMarketingResearch/1.0 (educational research tool)"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            articles = json.loads(response.read().decode("utf-8"))
            return [a for a in articles if a.get("likes_count", 0) >= min_likes]
    except Exception as e:
        print(f"  Warning: Qiita query '{query}' failed: {e}")
        return []


def normalize_article(article: dict, query: str) -> dict:
    """Normalize a Qiita API article to a standard structure."""
    tags = [t["name"] for t in article.get("tags", [])]
    return {
        "id": article.get("id", ""),
        "title": article.get("title", ""),
        "url": article.get("url", ""),
        "author": article.get("user", {}).get("id", ""),
        "likes_count": article.get("likes_count", 0),
        "comments_count": article.get("comments_count", 0),
        "page_views_count": article.get("page_views_count"),  # may be None (private stat)
        "tags": tags,
        "created_at": article.get("created_at", ""),
        "matched_query": query,
        "engagement_score": article.get("likes_count", 0) + article.get("comments_count", 0) * 3,
    }


def classify_article(article: dict) -> str:
    """Classify article as 'success', 'pain_point', or 'general'."""
    title = article["title"].lower()
    text = title + " " + " ".join(article["tags"]).lower()

    success_kw = [
        "リリースした", "公開した", "収益", "ダウンロード", "ユーザー獲得",
        "万ダウンロード", "万円", "ヒットした", "バズった", "振り返り", "まとめ",
        "成功", "伸びた",
    ]
    pain_kw = [
        "ダウンロードされない", "ユーザーが来ない", "宣伝できない", "集客できない",
        "誰にも使われない", "埋もれた", "どうすれば", "悩み", "失敗",
    ]

    if any(kw in text for kw in success_kw):
        return "success"
    if any(kw in text for kw in pain_kw):
        return "pain_point"
    return "general"


def main():
    parser = argparse.ArgumentParser(description="Fetch app/game marketing-related Qiita articles")
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="Target year for filtering articles (default: current year)")
    parser.add_argument("--min-likes", type=int, default=3,
                        help="Minimum likes threshold (default: 3)")
    parser.add_argument("--output", type=str, default="/tmp/qiita_raw.json",
                        help="Output JSON file path")
    parser.add_argument("--queries", type=str, default=None,
                        help="Comma-separated query list (default: built-in marketing list)")
    args = parser.parse_args()

    queries = args.queries.split(",") if args.queries else MARKETING_QUERIES
    target_year = args.year
    token = os.environ.get("QIITA_TOKEN")

    if token:
        print("Using Qiita API token (higher rate limit).")
    else:
        print("No QIITA_TOKEN found — using public API (60 req/hour limit).")

    print(f"Fetching Qiita articles for year {target_year} using {len(queries)} queries...")

    seen_ids = set()
    all_articles = []
    success_articles = []
    pain_articles = []

    for query in queries:
        print(f"  Searching: '{query}'...")
        articles = fetch_qiita_articles(query, target_year,
                                        min_likes=args.min_likes, token=token)
        for raw in articles:
            article = normalize_article(raw, query)
            if article["id"] not in seen_ids:
                seen_ids.add(article["id"])
                category = classify_article(article)
                article["category"] = category
                all_articles.append(article)
                if category == "success":
                    success_articles.append(article)
                elif category == "pain_point":
                    pain_articles.append(article)

        time.sleep(1.0)  # stay well within 60 req/hour

    all_articles.sort(key=lambda x: x["engagement_score"], reverse=True)
    success_articles.sort(key=lambda x: x["engagement_score"], reverse=True)
    pain_articles.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "target_year": target_year,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_articles": len(all_articles),
        "success_articles_count": len(success_articles),
        "pain_point_articles_count": len(pain_articles),
        "queries_used": queries,
        "top_success_stories": success_articles[:20],
        "top_pain_points": pain_articles[:20],
        "all_articles": all_articles[:80],
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Found {len(all_articles)} unique Qiita articles: "
          f"{len(success_articles)} success stories, {len(pain_articles)} pain points.")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()
