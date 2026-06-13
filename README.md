# Applied Statistics Assignment

Pythonでデータ分析を学びながら、応用統計学の課題3を進めるための作業フォルダです。

## 目的

- `hl_qol.csv` を使って論文の Table 2、Table 3、Table 4 に近い分析を行う
- Pythonでデータ確認、集計、統計検定、回帰分析を学ぶ
- 完成物を丸ごと作るより、処理の意味を理解することを優先する

## フォルダ構成

```text
assignment/
├─ data/
│  ├─ raw/
│  │  ├─ hl_qol.csv
│  │  └─ hl_qol.dta
│  └─ dictionary/
│     └─ variable_table.xlsx
├─ reference/
│  ├─ assignment/
│  │  ├─ 応用統計学_最終レポート課題.pdf
│  │  └─ Assignment 1 questions 3.docx
│  └─ original_tables/
│     ├─ table2_original.png
│     ├─ table3_original.png
│     └─ table4_original.png
├─ scripts/
├─ notebooks/
└─ outputs/
```

## 主なファイル

- `data/raw/hl_qol.csv`
  - Python分析で主に使うローデータ
- `data/raw/hl_qol.dta`
  - Stata形式の元データ
- `data/dictionary/variable_table.xlsx`
  - 変数名とカテゴリの説明
- `reference/original_tables/`
  - 論文の Table 2、Table 3、Table 4 の確認用画像

## 最初にやること

まずはデータの中身を確認します。

```python
import pandas as pd

df = pd.read_csv("data/raw/hl_qol.csv")

print(df.shape)
print(df.columns)
print(df.head())
print(df.isna().sum())
```

## Gitについて

このフォルダはローカルでGit管理します。
GitHubに上げる前提ではありません。

```powershell
git init
git status
```

必要になったら、自分の学習区切りごとにコミットします。
