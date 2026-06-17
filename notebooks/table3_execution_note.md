# Table 3 の作り方メモ

## 使っているファイル

- 入力データ: `data/raw/hl_qol.csv`
- 実行コード: `scripts/05_table3_blocks.py`
- 実行すると作られるファイル:
  - `outputs/table3_preview.csv`
  - `outputs/table3_preview.xlsx`

## 全体の流れ

1. `hl_qol.csv` を読み込む
2. Table 3 に出す各変数ごとにカテゴリ別の集計をする
3. カテゴリ別に以下を計算する
   - physical component score `pcs` の平均
   - `pcs` の95%信頼区間
   - mental component score `mcs` の平均
   - `mcs` の95%信頼区間
   - `pcs` の p値
   - `mcs` の p値
4. 変数ごとの結果を縦に結合する
5. CSV と Excel に保存する

## Rで再現するときの対応

Pythonでやっていることは、Rではだいたい次の処理に対応します。

| Python側の処理 | Rでの考え方 |
| --- | --- |
| `pd.read_csv()` | `read.csv()` または `readr::read_csv()` |
| `groupby()` 相当のカテゴリ別処理 | `group_by()` |
| `series.mean()` | `mean()` |
| `sem()` | 平均の標準誤差を計算 |
| `t.ppf()` | t分布にもとづく95%信頼区間を計算 |
| `ttest_ind()` | `t.test()` |
| `f_oneway()` | `aov()` または `oneway.test()` |

## 集計している変数

Table 3 では、以下の変数を順番に集計しています。

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

`pcs` と `mcs` はどちらも欠損がないため、基本的には元データ全体をもとに平均と95%信頼区間を計算しています。

2カテゴリの変数では t検定を使い、3カテゴリ以上の変数では一元配置ANOVAを使って p値を計算しています。

論文の Table 3 では一部の順序カテゴリに trend test が使われているため、現在のPythonコードで計算した p値は論文掲載値と完全には一致しない可能性があります。
