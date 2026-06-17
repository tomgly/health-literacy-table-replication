# Health Literacy Table Replication

応用統計学の課題3で、health literacy と QOL のデータを使って論文の表を再現するための作業フォルダです。

## 目的

- `hl_qol.csv` を使って論文の Table 2、Table 3、Table 4 に近い分析を行う
- データ確認、集計、統計検定、回帰分析の流れをPythonで理解する
- 完成物を丸ごと作るより、処理の意味を説明できるようにする

## 主なファイル

### スクリプト

- `scripts/01_load_data.py`
  - データの形、列名、欠損、主要変数を確認する
- `scripts/02_table2_gender.py`
  - Table 2 の Gender 部分だけを確認する
- `scripts/03_table2_blocks.py`
  - Table 2 のカテゴリ別集計を作る
- `scripts/04_table3_gender.py`
  - Table 3 の Gender 部分だけを確認する
- `scripts/05_table3_blocks.py`
  - Table 3 のカテゴリ別QOL集計を作る

### ノート

- `notebooks/table2_execution_note.md`
  - Table 2 の実行メモ
- `notebooks/table3_execution_note.md`
  - Table 3 の実行メモ

### 出力

- `outputs/table2_preview.csv`
  - Table 2 の確認用CSV
- `outputs/table2_preview.xlsx`
  - Table 2 の確認用Excel
- `outputs/table3_preview.csv`
  - Table 3 の確認用CSV
- `outputs/table3_preview.xlsx`
  - Table 3 の確認用Excel

## ローカルで用意するファイル

- `data/raw/hl_qol.csv`
  - 分析で使うローデータ
- `data/raw/hl_qol.dta`
  - Stata形式の元データ
- `data/dictionary/variable_table.xlsx`
  - 変数名とカテゴリの説明
- `reference/original_tables/`
  - 論文の Table 2、Table 3、Table 4 の画像

## セットアップ

このプロジェクトでは `uv` を使います。

```powershell
uv sync
```

依存関係は `pyproject.toml` と `uv.lock` で管理します。

## データ確認

まずは元データの形を確認します。

```powershell
uv run python scripts/01_load_data.py
```

## Table 2 の実行

Table 2 は次のコマンドで作ります。

```powershell
uv run python scripts/03_table2_blocks.py
```

出力先は以下です。

- `outputs/table2_preview.csv`
- `outputs/table2_preview.xlsx`

処理内容は `notebooks/table2_execution_note.md` にまとめています。

## Table 3 の実行

Table 3 は次のコマンドで作ります。

```powershell
uv run python scripts/05_table3_blocks.py
```

出力先は以下です。

- `outputs/table3_preview.csv`
- `outputs/table3_preview.xlsx`

処理内容は `notebooks/table3_execution_note.md` にまとめています。

## 次にやること

次は Table 4 に進みます。

Table 4 では、health literacy の3群を使って以下を確認します。

- `pcs` と `mcs` の平均と95%信頼区間
- `adequate` を基準カテゴリにした crude regression
- 論文脚注に沿った adjusted regression

最初は crude model から進めます。

## メモ

このプロジェクトは学習用です。
論文の表と完全一致させることより、どの変数を使って何を計算しているかを理解することを優先します。

Table 2 と Table 3 では、論文掲載値と完全には一致しない場合があります。
特に Table 2 は、課題文にも再集計値が論文表と完全一致しない可能性があると記載されています。

## 元論文

- DOI: `10.1371/journal.pone.0151079`
- 論文リンク: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0151079
