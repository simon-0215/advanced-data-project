# S&P 500 Stock Price Exploratory Data Analysis Report

**Project:** advanced-data-project  
**Report date:** 2026-02-04  
**Data range:** 2015-01-02 to 2025-12-30  

---

## 1. Introduction

This report presents an exploratory data analysis (EDA) of 10 representative S&P 500 stocks.  
The goal is to understand price trends, return distribution, risk characteristics, and cross-asset correlation as a foundation for portfolio optimization and risk management.

### Data Source

| Item | Details |
|------|---------|
| Dataset | S&P 500 Stock Prices (Portfolio Optimization, 2015–2025) |
| Platform | Kaggle |
| Dataset page | [Kaggle Dataset](https://www.kaggle.com/datasets/hiteshyadavx/s-and-p-500-stock-prices) |
| File used | `Prices.csv` |
| Download date | 2026-02-04 |

### Data Format

- Wide format table: rows are trading days, columns are `Date` + tickers
- Values are adjusted close prices
- Tickers: AAPL, AMZN, GOOGL, JNJ, JPM, META, MSFT, NVDA, PG, XOM

### Analysis Assumptions

- No transaction costs
- No slippage
- Long-only constraints (weights >= 0)
- Risk-free rate is set to 0 for Sharpe ratio

---

## 2. Data Processing

1. Parse `Date` as datetime and sort by date  
2. Check missing values by ticker  
3. Apply forward-fill as the missing-value policy  
4. Compute simple returns and log returns  
5. Use simple returns for downstream metrics and visualizations

### Metrics Computed (per ticker)

- Annualized return
- Annualized volatility
- Sharpe ratio (rf = 0)
- Maximum drawdown

---

## 3. Visualization Notes

All figures are saved under `outputs/figs/`.

1. **price_sample.png**: representative price curves  
2. **return_hist.png**: return distributions by ticker  
3. **rolling_vol.png**: rolling annualized volatility  
4. **drawdown.png**: drawdown over time  
5. **corr_heatmap.png**: return correlation heatmap  
6. **top_bottom_return.png**: annualized return ranking  
7. **sharpe_ratio.png**: Sharpe ranking  
8. **top_bottom_metrics.png**: volatility and max drawdown ranking  
9. **cum_returns.png**: cumulative return trajectories  
10. **return_ts_aapl.png**: daily AAPL return series  
11. **return_boxplot.png**: return boxplots by ticker  
12. **risk_return_scatter.png**: risk-return tradeoff

---

## 4. Key Results

### Per-Ticker Summary

| Ticker | Annualized Return | Annualized Volatility | Sharpe | Max Drawdown |
|------|------:|------:|------:|------:|
| NVDA | 72.21% | 48.70% | 1.48 | -66.34% |
| MSFT | 25.64% | 26.89% | 0.95 | -37.15% |
| GOOGL | 25.37% | 28.85% | 0.88 | -44.32% |
| AAPL | 24.71% | 28.85% | 0.86 | -38.52% |
| AMZN | 28.06% | 32.93% | 0.85 | -56.15% |
| META | 21.61% | 37.54% | 0.58 | -76.74% |
| JPM | 19.29% | 27.15% | 0.71 | -43.63% |
| JNJ | 9.44% | 18.20% | 0.52 | -27.37% |
| PG | 7.30% | 18.52% | 0.39 | -24.50% |
| XOM | 6.95% | 27.42% | 0.25 | -61.34% |

### Findings

- NVDA has the strongest return and highest Sharpe, but also high risk and deep drawdowns.
- MSFT shows strong risk-adjusted performance with a relatively balanced profile.
- JNJ and PG are more defensive (lower volatility and shallower drawdowns) but lower return.
- Correlation is generally higher among tech names than between tech and defensive stocks.

---

## 5. Conclusions and Next Steps

### Conclusions

- Data quality is good; missing-value handling has limited impact in this sample.
- Growth/tech names provide higher returns but also higher volatility and drawdown risk.
- Defensive names improve stability but reduce expected return.

### Output Files

- `outputs/returns.csv`
- `outputs/metrics.csv`
- `outputs/corr.csv`
- `outputs/figs/*.png`

### Advanced Next Steps

1. Mean-variance optimization and efficient frontier backtesting  
2. Risk parity / Hierarchical Risk Parity (HRP) comparison  
3. Factor decomposition plus volatility regime detection (e.g., HMM)

---

*Generated from the project EDA workflow. For implementation details, see `notebook/eda.ipynb`.*
