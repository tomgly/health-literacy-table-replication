# Health Literacy Table Replication

応用統計学の課題3で、health literacy と QOL のデータを使って論文の表を再現するための作業フォルダです。

## 目的

- `hl_qol.csv` を使って論文の Table 2、Table 3、Table 4 に近い分析を行う
- データ確認、集計、統計検定、回帰分析の流れを理解する
- 完成物を丸ごと作るより、処理の意味を説明できるようにする

## 主なファイル

### スクリプト

- `scripts/01_load_data.py`
  - データの形、列名、欠損、主要変数を確認するスクリプト
- `scripts/02_table2_gender.py`
  - Table 2 の Gender 部分だけを確認するスクリプト
- `scripts/03_table2_blocks.py`
  - Table 2 の集計を作るPythonスクリプト
- `scripts/04_table3_gender.py`
  - Table 3 の Gender 部分を確認するスクリプト

### ノート

- `notebooks/table2_execution_note.md`
  - Table 2 の実行メモ

### 出力

- `outputs/table2_preview.csv`
  - Table 2 の確認用CSV
- `outputs/table2_preview.xlsx`
  - Table 2 の確認用Excel

## ローカルで用意するファイル

- `data/raw/hl_qol.csv`
  - 分析で使うローデータ
- `data/dictionary/variable_table.xlsx`
  - 変数名とカテゴリの説明

## Table 2 の実行

Table 2 は次のコマンドで作ります。

```powershell
python scripts/03_table2_blocks.py
```

出力先は以下です。

- `outputs/table2_preview.csv`
- `outputs/table2_preview.xlsx`

処理内容は `notebooks/table2_execution_note.md` に短くまとめています。

## 最初に確認すること

まずは以下を確認します。

- 元データ: `data/raw/hl_qol.csv`
- 変数表: `data/dictionary/variable_table.xlsx`
- 論文の元表: `reference/original_tables/`
- Table 2 の実行メモ: `notebooks/table2_execution_note.md`

## メモ

このプロジェクトは学習用です。
論文の表と完全一致させることより、どの変数を使って何を計算しているかを理解することを優先します。

## 元論文

- DOI: `10.1371/journal.pone.0151079`
- 論文リンク: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0151079
