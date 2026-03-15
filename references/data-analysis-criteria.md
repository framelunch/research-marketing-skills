# Data Analysis Criteria

How to evaluate and filter raw data from Reddit, HN, and Qiita into actionable insights.

## Engagement Thresholds

| Source | Signal | Threshold for significance |
|--------|--------|---------------------------|
| Reddit | post score + comments | Top 10% within the fetched set |
| HN | `engagement_score` = points + 2× comments | >100 points = strong signal |
| Qiita | `engagement_score` = likes + 3× comments | 50+ likes = significant |

## What to Extract per Source

**Reddit (`/tmp/reddit_raw.json`):**
- `top_success_stories`: What worked for similar products? Look for repeating patterns across multiple posts.
- `top_pain_points`: What are developers struggling with? These are landmines to avoid.
- Classify posts as `success`, `pain_point`, or `general` based on their framing.

**HN (`/tmp/hn_raw.json`):**
- Sort by `engagement_score`.
- Show HN posts reveal what the tech-savvy early adopter community responds to.
- Prioritize posts with concrete data: revenue numbers, download benchmarks, channel effectiveness.

**Qiita (`/tmp/qiita_raw.json`):**
- `top_success_stories`: Japanese developer launch reports with concrete data (downloads, revenue).
- `top_pain_points`: Japan-specific discoverability and promotion struggles.
- Look for Japan-specific channels mentioned: X `#個人開発`, note, はてなブックマーク, AppBank, etc.
- Note: Qiita audience is developers — adjust for mainstream Japanese users accordingly.

## Relevance Filtering

Raw data is broad; filter for what applies to the user's specific product. A marketing insight
for a PC strategy game does not automatically apply to a productivity iOS app. Always ground
your analysis in the user's specific **category**, **platform**, and **target audience**.

When data is thin for a niche, say so explicitly rather than extrapolating too far.

## Global vs. Japan Distinction

Always separate insights into two tracks:
1. **Global/English-language strategies** — sourced from Reddit + HN
2. **Japan-specific strategies** — sourced from Qiita

Present both tracks clearly in the report. Do not blend them without noting the source.

## Source Reliability & Limitations

| Source | Bias / Limitation |
|--------|--------------------|
| Reddit | Public API returns top ~1000 posts; older years (3+ years back) may have gaps |
| HN | English-centric; Japanese market insights will be limited; skews technical |
| Qiita | Japan/developer-centric; supplement with Reddit/HN for global strategies; 60 req/hour unauthenticated |
| All | All three sources skew toward technically sophisticated audiences — adjust if targeting mainstream/casual users |

If any script fails due to network issues, note this in the report and proceed with partial data.
If rate-limited on Qiita, suggest setting `QIITA_TOKEN` env var or reducing `--limit`.
