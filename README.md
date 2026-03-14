# research-marketing-skills

作成したアプリ・ゲームのマーケティング戦略を、Reddit と Hacker News のリアルなコミュニティデータをもとに調査・提案する Claude Code スキル。

## 概要

このリポジトリには、Claude Code 向けのローカルスキルが含まれています。スキルを使うと Claude が次のことを自動で行います。

1. マーケティングしたい商品について日本語で確認する
2. Reddit（15サブレディット）と Hacker News（22クエリ）からデータを収集する
3. 成功事例・ペインポイントを分析し、商品に合ったマーケティング戦略を立案する
4. 調査結果をレポートファイルに保存する

## ディレクトリ構成

```
research-marketing-skills/
├── CLAUDE.md              # ローカルスキル登録（このディレクトリ内のみで有効）
├── SKILL.md               # スキル定義（Claude Code が参照）
├── scripts/
│   ├── fetch_reddit.py    # Reddit からマーケティング関連投稿を取得
│   └── fetch_hn.py        # Hacker News からマーケティング関連投稿を取得
├── references/
│   ├── marketing-subreddits.md  # 対象サブレディットと読み方の解説
│   ├── hn-search-guide.md       # HN 検索クエリ戦略の解説
│   └── report-template.md       # レポートの出力テンプレート
└── reports/
    └── {西暦}/{yyyy-mm-dd}/{HHMMSS}.md  # 生成されたレポート
```

## 使い方

このディレクトリで Claude Code を開くと、スキルが自動的に有効になります。

```
マーケティング戦略を考えたい
```

のように話しかけると、Claude が日本語で商品内容を確認してから調査を開始します。

### 出力されるレポートの内容

| 項目 | 内容 |
|------|------|
| 市場調査結果 | Reddit・HN から抽出した成功事例とペインポイント |
| ターゲット設定 | 対象ユーザーの明確さ・需要シグナル（5段階評価） |
| 価格設定 | 市場相場・競合ベンチマーク（5段階評価） |
| 販売チャネル | App Store / Steam / Web 等の選択肢（5段階評価） |
| 宣伝方法 | Reddit / HN / SNS 等の具体的な施策（5段階評価） |
| 小規模適正 | ソロ開発者・小チームへの実現可能性（5段階評価） |

レポートは `reports/{西暦}/{yyyy-mm-dd}/{HHMMSS}.md` に保存されます。

### スクリプトの直接実行

```bash
# Reddit データ取得
python scripts/fetch_reddit.py --year 2026 --output /tmp/reddit_raw.json

# Hacker News データ取得
python scripts/fetch_hn.py --year 2026 --output /tmp/hn_raw.json
```

どちらも認証不要のパブリック API を使用しています。

## 調査対象

### Reddit サブレディット

- アプリビジネス: r/SideProject, r/AppBusiness, r/startups, r/growthhacking
- ライフスタイル・生産性: r/Journaling, r/productivity, r/selfimprovement, r/bulletjournal
- モバイル開発: r/iOSProgramming, r/androiddev
- ゲーム開発（参考）: r/gamedev, r/IndieDev

### Hacker News クエリ

日記・習慣・生産性アプリ、アプリローンチ・マーケティング、ゲームマーケティングなど 22 クエリで検索。

## 注意事項

- このスキルは**このディレクトリ内でのみ**有効です（グローバルには登録されていません）
- Reddit API は上位約 1,000 件が上限のため、3年以上前のデータは不完全な場合があります
- HN のデータは英語圏・テック寄りのため、日本市場向けには補足調査を推奨します
