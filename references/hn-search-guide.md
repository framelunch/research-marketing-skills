# Hacker News Search Guide for App/Game Marketing Research

## Overview
HN Algolia API (https://hn.algolia.com/api/v1/search) provides free, no-auth access to HN posts.
The fetch_hn.py script uses this to find marketing-relevant discussions.

## Key Query Categories

### Launch Stories (Show HN)
- `"Show HN game"` — direct game launches to HN community
- `"Show HN app"` — app launches, often include honest engagement numbers
- `"indie game launch"` — retrospectives and stories
- `"app launch strategy"` — planning discussions with community feedback

### Success & Growth
- `"indie game revenue"` — revenue sharing posts (highly valuable benchmarks)
- `"game success story"` — what worked, what didn't
- `"app growth hacking"` — growth tactics that worked
- `"user acquisition app"` — specific UA channel discussions

### Strategy & Tactics
- `"app store optimization"` — ASO techniques from practitioners
- `"game monetization"` — F2P, premium, subscription comparisons
- `"mobile game marketing"` — platform-specific mobile strategies
- `"freemium game strategy"` — conversion optimization
- `"app retention strategy"` — churn reduction

### Pain Points & Lessons
- `"game discoverability"` — the central challenge for indie games
- `"indie developer marketing"` — "we're not marketers" perspective
- `"subscription app pricing"` — pricing experimentation stories

## Interpreting Results

### Engagement Score Formula
`engagement_score = points + (num_comments × 2)`

Higher comment counts relative to points = community debate or strong opinions
High points + low comments = broad agreement or informational post

### Quality Signals for Marketing Research
- **points > 100**: Widely resonant with HN audience (tech-savvy early adopters)
- **num_comments > 50**: Active discussion = likely contains actionable disagreement or nuance
- **Show HN with points > 50**: Rare success; worth studying what they did right
- **Launched + revenue figures**: Primary data source for benchmarking

## Limitations
- HN audience skews heavily technical and English-speaking
- Successful "Show HN" posts ≠ mainstream app/game success (different demographics)
- Japanese market specifics won't appear often — supplement with local research
- Year filtering uses timestamps; posts near year boundaries may differ slightly
