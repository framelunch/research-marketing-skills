# research-marketing-skills

This directory contains a marketing strategy research skill for apps and games.

## Available Skill

**app-game-marketing-strategy** (`SKILL.md`)

Use this skill whenever working on marketing, user acquisition, launch strategy, or growth
for any app, game, or digital product in this directory. The skill:

1. Asks the user (in Japanese) what product they want to market
2. Runs Reddit and HN research scripts to gather real community data
3. Generates a comprehensive marketing strategy report with 5 scored categories
4. Saves the report to `reports/{year}/{date}/{time}.md`

## Directory Structure

```
research-marketing-skills/
├── CLAUDE.md          ← this file (local skill registration)
├── SKILL.md           ← marketing strategy skill
├── scripts/
│   ├── fetch_reddit.py   ← fetches from marketing subreddits
│   ├── fetch_hn.py       ← fetches from Hacker News
│   └── fetch_qiita.py    ← fetches from Qiita (Japan market)
├── references/
│   ├── marketing-subreddits.md  ← subreddit guide
│   ├── hn-search-guide.md       ← HN search strategy
│   ├── qiita-search-guide.md    ← Qiita search strategy & Japan channels
│   ├── report-template.md       ← full report template
│   └── japanese-era.md          ← era conversion reference
└── reports/
    └── {year}/{date}/{time}.md   ← generated reports
```

## Script Usage

```bash
# Reddit research
python scripts/fetch_reddit.py --year 2026 --output /tmp/reddit_raw.json

# HN research
python scripts/fetch_hn.py --year 2026 --output /tmp/hn_raw.json

# Qiita research (Japan market)
python scripts/fetch_qiita.py --year 2026 --output /tmp/qiita_raw.json
# Optional: set QIITA_TOKEN env var to increase rate limit from 60 to 1000 req/hour
```

## Notes
- This skill is local to this directory only
- Reports use Western calendar year format (e.g., 2026, 2025)
- All scripts require no API keys — they use public APIs only
- Qiita script optionally accepts `QIITA_TOKEN` env var for higher rate limits
