---
name: app-game-marketing-strategy
description: >
  Marketing strategy research skill for apps and games. Researches success stories and
  pain points from Reddit marketing communities and Hacker News, then synthesizes a
  complete marketing strategy report covering target audience, pricing, sales channels,
  promotion methods, and small-scale suitability — each rated on a 5-point scale.

  Use this skill whenever the user wants to market, promote, launch, or grow an app,
  game, mobile game, indie game, web service, or any software product. Also trigger
  when the user asks about user acquisition, app store visibility, game discoverability,
  pricing strategy for digital products, or how to reach their first users. Even if
  they don't say "marketing" explicitly — if they're asking how to get people to use
  their product, use this skill.
---

# App & Game Marketing Strategy Skill

You help developers understand how to market their apps and games effectively, drawing on
real community data from Reddit and Hacker News. Your output is a concrete, actionable
strategy grounded in what has actually worked (and failed) for similar products.

## Step 1: Confirm the Product (Ask in Japanese)

Before doing any research, ask the user in Japanese to confirm what they want to market.
Gather enough context to make the research targeted and useful.

Ask these questions in Japanese in a single message:

```
マーケティング調査を始める前に、いくつか確認させてください。

1. **商品名・サービス名**はなんですか？
2. **カテゴリ**を教えてください（例：モバイルゲーム、PCゲーム、iOSアプリ、Webサービスなど）
3. **プラットフォーム**はどこを予定していますか？（App Store / Google Play / Steam / Web など）
4. **ターゲットユーザー**のイメージはありますか？（例：10代のゲーマー、社会人向け生産性アプリなど）
5. **価格モデル**の候補はありますか？（無料・有料・フリーミアム・サブスクリプションなど）
6. **調査対象年度**はいつにしますか？（指定がなければ現在の年を使用します）

分かる範囲で教えていただければ大丈夫です。
```

Wait for the user's response before proceeding.

## Step 2: Determine Target Year

Once the user responds, determine:
- **target_year**: from user input, or use the current year (e.g., 2026)

Set the report output path:
```
reports/{target_year}/{yyyy-mm-dd}/{HHMMSS}.md
```
Where `{yyyy-mm-dd}` is today's date and `{HHMMSS}` is the current time when you start writing the report.

Create the directory before writing: `mkdir -p reports/{target_year}/{yyyy-mm-dd}/`

## Step 3: Run Data Collection

Run all three scripts in parallel (or sequentially if needed). Use the target_year from Step 2.

### Reddit Research
```bash
python scripts/fetch_reddit.py \
  --year {target_year} \
  --limit 30 \
  --output /tmp/reddit_raw.json
```

This fetches from marketing subreddits (r/gamedev, r/IndieDev, r/SideProject, r/startups, etc.)
and classifies posts as `success`, `pain_point`, or `general`.

For context on which subreddits are searched and what signals to look for, read:
`references/marketing-subreddits.md`

### Hacker News Research
```bash
python scripts/fetch_hn.py \
  --year {target_year} \
  --min-points 5 \
  --output /tmp/hn_raw.json
```

This searches HN for app/game marketing discussions (Show HN launches, revenue posts,
strategy discussions) using 20 targeted queries.

For context on queries and how to interpret HN data, read:
`references/hn-search-guide.md`

### Qiita Research (Japan market)
```bash
python scripts/fetch_qiita.py \
  --year {target_year} \
  --min-likes 3 \
  --output /tmp/qiita_raw.json
```

This searches Qiita for Japanese individual developer articles about app/game launches,
monetization, and promotion strategies. Uses 16 targeted Japanese queries.
No authentication required (60 req/hour limit applies).

For context on queries and how to interpret Qiita data, read:
`references/qiita-search-guide.md`

## Step 4: Analyze the Data

Read all three output files and extract insights relevant to the user's specific product.

**From Reddit (`/tmp/reddit_raw.json`):**
- `top_success_stories`: What worked for similar products? Look for patterns.
- `top_pain_points`: What are developers struggling with? These are your landmines to avoid.
- Cross-reference with the product category and platform the user gave you.

**From HN (`/tmp/hn_raw.json`):**
- Sort by `engagement_score` (points + 2× comments)
- Posts with >100 points are significant signals
- Show HN posts reveal what the HN community (tech-savvy early adopters) responds to
- Look for revenue numbers, download benchmarks, channel effectiveness data

**From Qiita (`/tmp/qiita_raw.json`):**
- `top_success_stories`: Japanese developer launch reports with concrete data (downloads, revenue)
- `top_pain_points`: Japan-specific discoverability and promotion struggles
- Sort by `engagement_score` (likes + 3× comments); articles with 50+ likes are significant
- Look for Japan-specific channels mentioned: X `#個人開発`, note, はてなブックマーク, AppBank等
- Note: Qiita audience is developers — adjust for mainstream Japanese users accordingly

**Synthesize for this specific product:**
The raw data is broad; your job is to filter it for relevance. A marketing insight for a PC
strategy game doesn't automatically apply to a productivity iOS app. Stay grounded in what
the data says about the user's specific category, platform, and audience.

**Global vs. Japan distinction:**
Separate insights into (1) global/English-language strategies (Reddit + HN) and
(2) Japan-specific strategies (Qiita). The report must present both tracks clearly.

## Step 5: Generate the Report

Read the full template from `references/report-template.md` before writing.

The report structure has 6 sections:
1. Product Overview
2. Market Research Summary (Reddit + HN + Qiita findings)
3. Marketing Strategy Recommendations (5 scored sections, each with Japan-specific sub-section)
4. Action Plan
5. Key Risks & Mitigations
6. Data Sources

### The 5 Scored Sections (core output)

Each section uses a 5-point scale with a clear rationale. Be honest — if the market data
suggests a challenging environment, say so at 2/5 rather than inflating to 4/5.

| Section | What to Evaluate |
|---------|-----------------|
| **Target Audience** | How clearly defined and reachable is the audience? Demand signals? |
| **Pricing Strategy** | What does the market bear? What do similar products charge? |
| **Sales Channels** | What distribution paths are realistically available and competitive? |
| **Promotion Methods** | What organic/paid channels are viable given team size and budget? |
| **Small-Scale Suitability** | How feasible is this for a solo dev or small team? |

For each section:
- Give a star rating (★★★★☆ format) and numeric score (N/5)
- Provide a concrete table of options/benchmarks from the research data
- Explain what the score means for this specific product
- Include the scale definition so the user understands what each level means

**Section 3.4 (Promotion Methods) MUST include two parallel tracks:**
- **グローバル向け (Global):** Channels from Reddit/HN data (English-language)
- **日本向け (Japan):** Channels from Qiita data (X `#個人開発`, note, はてブ, AppBank, etc.)

Both tracks should have their own recommended promotion sequence (pre-launch / launch / post-launch).

### Writing Style
- Concrete and specific, not generic ("post on social media" is useless; "post weekly dev
  progress on r/IndieDev, targeting Tuesday/Wednesday for best visibility" is useful)
- Back every major recommendation with something from the research data
- Acknowledge uncertainty honestly — if the data is thin for a niche, say so
- Action-oriented: end with a clear minimum viable marketing plan

## Step 6: Save the Report

Save to the path determined in Step 2:
```
reports/{japanese_era}/{yyyy-mm-dd}/{HHMMSS}.md
```

After saving, tell the user in Japanese:
```
調査が完了しました。レポートを以下に保存しました：

`reports/{target_year}/{yyyy-mm-dd}/{HHMMSS}.md`

レポートの内容を要約します：
[brief summary in Japanese of key findings and the 5 scores]
```

Then display the full report content so the user can read it immediately.

## Step 7: Review for Improvements and Bugs

After completing the report, review the skill itself for issues. Check the following:

**Scripts (`scripts/`):**
- Did any script fail or return 0 results unexpectedly? If so, note the cause.
- Are there discrepancies between the script's output JSON keys and what this SKILL.md describes?
- Did rate limiting occur? If so, suggest adding `QIITA_TOKEN` or reducing `--limit`.

**SKILL.md (this file):**
- Are there any contradictions between steps (e.g., output paths, key names)?
- Are all referenced files in `references/` actually present on disk?

**`references/report-template.md`:**
- Does the template reflect all three data sources (Reddit, HN, Qiita)?

**`CLAUDE.md`:**
- Is the directory structure diagram consistent with the actual files and paths used?

If any issues are found, fix them immediately (edit files, create missing files, etc.) and tell the user in Japanese what was fixed:

```
スキルの改善点・バグを確認しました：

- [問題1]: [対応内容]
- [問題2]: [対応内容]
（問題がなければ「改善点・バグは見つかりませんでした」と報告）
```

If there are no issues, still report that explicitly so the user knows the review was done.

## Reference Files

| File | When to Read |
|------|-------------|
| `references/marketing-subreddits.md` | Understanding subreddit categories and what to look for |
| `references/hn-search-guide.md` | Interpreting HN data and query strategy |
| `references/qiita-search-guide.md` | Interpreting Qiita data and Japan-specific channels |
| `references/report-template.md` | Full report template — read before generating report |
| `references/japanese-era.md` | Era conversion table for report directory naming (令和N = year - 2018) |

## Notes on Data Quality

- Reddit's public API returns top ~1000 posts; older years (3+ years back) may have gaps
- HN data is English-centric; Japanese market insights will be limited
- Both Reddit and HN skew toward technically sophisticated audiences — adjust recommendations
  accordingly if the target audience is mainstream/casual
- Qiita data is Japan/developer-centric; supplement with Reddit/HN for global strategies
- Qiita unauthenticated API allows 60 req/hour — if rate-limited, set `QIITA_TOKEN` env var
- If any script fails due to network issues, note this in the report and proceed with partial data
