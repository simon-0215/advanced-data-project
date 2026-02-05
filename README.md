# advanced-data-project

## Data

### Source
- **Dataset:** S&P 500 Stock Prices (Portfolio Optimization, 2015–2025)
- **Platform:** Kaggle
- **Dataset page:** https://www.kaggle.com/datasets/hiteshyadavx/s-and-p-500-stock-prices
- **File used:** `Prices.csv`
- **Download date:** 2026-02-04

### Format
- `Prices.csv` is a wide-format table:
  - Rows = trading days
  - `Date` column = trading date
  - Other columns = stock tickers (e.g., AAPL, AMZN, GOOGL)
  - Values = adjusted close prices

### Notes
- Missing values may exist due to non-trading days or incomplete ticker history.
- All metrics and backtests in this project assume:
  - no transaction costs
  - no slippage
  - long-only constraints (weights >= 0)

## 项目结构

- `data/` — 原始数据 (Prices.csv)
- `notebook/` — Jupyter 分析 notebook (eda.ipynb)
- `outputs/` — 结果输出 (returns.csv, metrics.csv, corr.csv, figs/)
- `report/` — 中文 EDA 报告 (EDA报告.md)
