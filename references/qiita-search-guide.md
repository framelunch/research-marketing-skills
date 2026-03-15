# Qiita Search Guide

## Overview

Qiita is Japan's largest technical article platform, used widely by Japanese individual developers
to share app/game launch reports, marketing retrospectives, and monetization strategies.
It is the primary source for **Japan-specific marketing insights** not covered by Reddit or HN.

## API Basics

- **Endpoint:** `https://qiita.com/api/v2/items`
- **Auth:** Not required (60 req/hour unauthenticated; 1000 req/hour with `QIITA_TOKEN`)
- **Date filter:** Use `created:>=YYYY-01-01 created:<=YYYY-12-31` in the query string
- **Docs:** https://qiita.com/api/v2/docs

## Key Queries for App/Game Marketing Research

### Individual Development & Launch
| Query | What it finds |
|-------|--------------|
| `個人開発 リリース` | Release reports from solo developers |
| `個人開発 収益` | Revenue/monetization stories |
| `個人開発 マーケティング` | Marketing strategy articles |
| `個人開発 ユーザー獲得` | User acquisition tactics |
| `個人開発 宣伝` | Promotion methods used |

### Platform-Specific
| Query | What it finds |
|-------|--------------|
| `App Store 審査` | App Store review process tips |
| `ASO アプリ最適化` | App Store Optimization for Japan |
| `iOS アプリ リリース` | iOS launch experiences |
| `Androidアプリ リリース` | Android launch experiences |

### Game Development
| Query | What it finds |
|-------|--------------|
| `ゲーム 個人開発 リリース` | Indie game launch reports |
| `インディーゲーム マーケティング` | Indie game marketing in Japan |

## Interpreting Qiita Data

### Engagement Signals
- **likes_count (LGTM):** Primary quality signal. Articles with 50+ LGTMs are well-regarded.
- **comments_count:** Indicates discussion; multiply by 3 for engagement score.
- **page_views_count:** Only visible to article author — will be `null` in API responses.

### What High-LGTM Articles Reveal
- **Success stories (振り返り, まとめ):** Detailed retrospectives with specific numbers
  (downloads, revenue, channels that worked) — most valuable data points
- **How-to articles:** Specific tactics with step-by-step instructions
- **Failure analyses (失敗談):** What not to do — equally valuable

### Japan-Specific Marketing Channels Mentioned on Qiita
Based on common Qiita articles about individual app/game promotion:

| Channel | Usage Pattern | Best for |
|---------|--------------|---------|
| **X (Twitter)** `#個人開発` | Daily dev logs, screenshots | Building a following pre-launch |
| **note** | Long-form launch reports | SEO, storytelling, non-tech audience |
| **Zenn** | Technical articles (like Qiita) | Developer audience |
| **Qiita itself** | Technical launch reports | Developer community |
| **はてなブックマーク** | Content aggregation | Viral spread to broader audience |
| **Product Hunt** | English-language launch | International tech audience |
| **AppBank / iPhoneアプリまとめ** | App review media | Non-technical Japanese users |
| **4Gamer / ファミ通** | Game review media | Japanese gamers |
| **ニコニコ動画 / YouTube** | Video content | Game demos, tutorials |
| **Discord JP コミュニティ** | Community building | Niche game audiences |

## What to Look For

### Success Story Signals
- `リリースした` / `公開した` — just launched
- `収益` / `万円` — revenue figures
- `万ダウンロード` — download milestones
- `バズった` / `ヒットした` — went viral
- `振り返り` / `まとめ` — retrospectives (usually contain concrete data)

### Pain Point Signals
- `ダウンロードされない` — no downloads
- `ユーザーが来ない` — no users coming
- `誰にも使われない` — nobody using it
- `埋もれた` — buried/invisible in store

## Japan Market Context

- **App Store Japan** is the world's 2nd largest by revenue — high opportunity but competitive
- **X (Twitter) Japan** has unusually high engagement; `#個人開発` tag is very active
- **note** is popular for non-technical launch stories targeting mainstream Japanese users
- **はてなブックマーク** acts as a secondary viral amplifier — articles with 100+ bookmarks
  reach a broad Japanese internet audience
- Japanese users respond well to **dev diaries and authentic behind-the-scenes content**
- Localization quality (Japanese text, date formats, yen pricing) heavily impacts conversion

## Data Quality Notes

- Qiita skews toward developer audiences — mainstream user insights are limited
- Articles are in Japanese — directly useful for Japan market; supplement with Reddit/HN for global
- Older years (3+ years back) may return fewer results as the query API prioritizes recency
- If API rate limit is hit (HTTP 429), wait 60 seconds and retry
