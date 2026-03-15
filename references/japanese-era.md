# Japanese Era (元号) Reference

Use this table to convert Western calendar years to Japanese era (元号) format when naming report directories.

## Era Conversion Table

| Western Year | Japanese Era | 表記 |
|-------------|--------------|------|
| 2019 | Reiwa 1 | 令和元年 |
| 2020 | Reiwa 2 | 令和2年 |
| 2021 | Reiwa 3 | 令和3年 |
| 2022 | Reiwa 4 | 令和4年 |
| 2023 | Reiwa 5 | 令和5年 |
| 2024 | Reiwa 6 | 令和6年 |
| 2025 | Reiwa 7 | 令和7年 |
| 2026 | Reiwa 8 | 令和8年 |
| 2027 | Reiwa 9 | 令和9年 |
| 2028 | Reiwa 10 | 令和10年 |
| 2029 | Reiwa 11 | 令和11年 |
| 2030 | Reiwa 12 | 令和12年 |

## Formula

```
Reiwa year = Western year - 2018
```

Example: 2026 - 2018 = **8** → 令和8年

## Usage in Reports

Report directories use the format:
```
reports/令和{N}/{yyyy-mm-dd}/{HHMMSS}.md
```

Examples:
- 2025 report → `reports/令和7/2025-06-01/093000.md`
- 2026 report → `reports/令和8/2026-03-15/120000.md`

## Note

The Reiwa era started on **May 1, 2019**. For dates before May 1, 2019, the Heisei (平成) era was in use, but this skill focuses on 2019 onward where Reiwa applies cleanly to full calendar years.
