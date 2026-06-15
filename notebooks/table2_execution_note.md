# Table 2 の作り方メモ

## 使っているファイル

- 入力データ: `data/raw/hl_qol.csv`
- 実行コード: `scripts/03_table2_blocks.py`
- 実行すると作られるファイル:
  - `outputs/table2_preview.csv`
  - `outputs/table2_preview.xlsx`

## 全体の流れ

1. `hl_qol.csv` を読み込む
2. `hltcatnew` が欠損している行を除外する
3. `hltcatnew` が `inadequate` の人を `inadequate_hl` として扱う
4. Table 2 に出す各変数ごとにカテゴリ別の集計をする
5. カテゴリ別に以下を計算する
   - 全体の人数 `N`
   - 全体に占める割合 `%`
   - inadequate health literacy の割合
   - 95%信頼区間
   - カイ二乗検定の p値
6. 変数ごとの結果を縦に結合する
7. CSV と Excel に保存する

## Rで再現するときの対応

Pythonでやっていることは、Rではだいたい次の処理に対応します。

| Python側の処理 | Rでの考え方 |
| --- | --- |
| `pd.read_csv()` | `read.csv()` または `readr::read_csv()` |
| `dropna(subset = "hltcatnew")` | `filter(!is.na(hltcatnew))` |
| `hltcatnew == "inadequate"` | `inadequate_hl = hltcatnew == "inadequate"` |
| `value_counts()` | `count()` |
| `groupby()` | `group_by()` |
| `pd.crosstab()` | `table()` |
| `chi2_contingency()` | `chisq.test()` |
| `proportion_confint(..., method = "wilson")` | Wilson法で割合の95%信頼区間を計算 |

## 集計している変数

Table 2 では、以下の変数を順番に集計しています。

- `Gender`
- `agegroup3`
- `ms2g`
- `RA06ur`
- `Stateno`
- `educatn4g`
- `workst3g`
- `econ3g`
- `irsd_quint`
- `ischprocedure`
- `yearsIHD3g`
- `CVDcomorb3g`
- `CVDriskf3g`

## 注意点

`N` と `%` は元データ全体をもとに計算しています。
一方で inadequate health literacy の割合、95%信頼区間、p値は `hltcatnew` が欠損していないデータをもとに計算しています。

そのため、論文の Table 2 と完全一致しない可能性があります。
