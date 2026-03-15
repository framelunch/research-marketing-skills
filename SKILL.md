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

## Step 2: Determine Target Year and Output Path

Once the user responds, determine:
- **target_year**: from user input, or use the current year (e.g., 2026)

Set the report output path:
```
reports/{target_year}/{yyyy-mm-dd}/{HHMMSS}.md
```
Where `{yyyy-mm-dd}` is today's date and `{HHMMSS}` is the current time when you start writing.

Create the directory before writing: `mkdir -p reports/{target_year}/{yyyy-mm-dd}/`

## Step 3: Run Data Collection

Run all three scripts in parallel. Use the target_year from Step 2.

```bash
python scripts/fetch_reddit.py --year {target_year} --limit 30 --output /tmp/reddit_raw.json
python scripts/fetch_hn.py --year {target_year} --min-points 5 --output /tmp/hn_raw.json
python scripts/fetch_qiita.py --year {target_year} --min-likes 3 --output /tmp/qiita_raw.json
```

For context on the data sources, read:
- `references/marketing-subreddits.md` — subreddit categories and signals
- `references/hn-search-guide.md` — HN query strategy
- `references/qiita-search-guide.md` — Qiita query strategy and Japan channels

## Step 4: Analyze the Data

Read `references/data-analysis-criteria.md` for:
- Engagement thresholds (what counts as a significant signal)
- What to extract from each source
- Relevance filtering guidelines
- Global vs. Japan distinction
- Source reliability and known limitations

## Step 5: Generate the Report

Read `references/report-template.md` for the full report structure.
Read `references/report-scoring-criteria.md` for how to score and write each section.

The report has 6 sections:
1. Product Overview
2. Market Research Summary (Reddit + HN + Qiita findings)
3. Marketing Strategy Recommendations (5 scored sections, each with Japan-specific sub-section)
4. Action Plan
5. Key Risks & Mitigations
6. Data Sources

## Step 6: Save the Report

Save to the path determined in Step 2. Then tell the user in Japanese:

```
調査が完了しました。レポートを以下に保存しました：

`reports/{target_year}/{yyyy-mm-dd}/{HHMMSS}.md`

レポートの内容を要約します：
[brief summary in Japanese of key findings and the 5 scores]
```

Then display the full report content so the user can read it immediately.

## Step 7: Review for Improvements and Bugs

After completing the report, review the skill itself for issues:

**Scripts (`scripts/`):**
- Did any script fail or return 0 results unexpectedly?
- Are there discrepancies between script output JSON keys and what this SKILL.md describes?
- Did rate limiting occur?

**Files:**
- Are there contradictions between steps (output paths, key names)?
- Are all referenced files in `references/` actually present on disk?
- Does `references/report-template.md` reflect all three data sources?
- Is `CLAUDE.md`'s directory diagram consistent with actual files?

If issues are found, fix them immediately and report in Japanese:

```
スキルの改善点・バグを確認しました：

- [問題1]: [対応内容]
- [問題2]: [対応内容]
（問題がなければ「改善点・バグは見つかりませんでした」と報告）
```

## Reference Files

| File | Purpose |
|------|---------|
| `references/marketing-subreddits.md` | Subreddit categories and signals |
| `references/hn-search-guide.md` | HN query strategy |
| `references/qiita-search-guide.md` | Qiita queries and Japan channels |
| `references/data-analysis-criteria.md` | How to evaluate and filter raw data |
| `references/report-template.md` | Full report template |
| `references/report-scoring-criteria.md` | Scoring criteria and writing guidelines |
| `references/japanese-era.md` | Era conversion table (令和N = year - 2018) |
