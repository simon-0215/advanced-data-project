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

## Project Structure

- `data/` - source data (`Prices.csv`)
- `notebook/` - Jupyter analysis notebook (`eda.ipynb`)
- `outputs/` - generated outputs (`returns.csv`, `metrics.csv`, `corr.csv`, `figs/`)
- `report/` - reports (`EDA_report.md`, `assignment1Q1.md`)
