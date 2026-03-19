# TA Meeting Reference Pack

Project: `advanced-data-project`  
Scope: EDA + Time Series + ARIMA/ML Residual Extension

---

## 1) 3-Minute Progress Script (ready to read)

Hi TA, we want to give a quick progress update on our stock portfolio project based on S&P 500 price data from 2015 to 2025.

First, we completed the core data pipeline.  
We loaded `Prices.csv`, parsed dates, checked missing values, and computed daily returns.  
Our key output files are:
- `outputs/returns.csv` for daily returns,
- `outputs/metrics.csv` for annualized return/volatility/Sharpe/max drawdown,
- `outputs/corr.csv` for return correlations.

Second, we completed the EDA and core visual analysis.

We focus on three key figures:
1. `outputs/A1figs/price_sample.png` - representative long-term price trajectories
2. `outputs/A1figs/corr_heatmap.png` - cross-asset correlation and diversification structure
3. `outputs/A1figs/risk_return_scatter.png` - risk-return tradeoff

We also use rolling volatility and drawdown plots to explain regime shifts and downside risk.

Third, we completed time-series modeling in `scripts/Timeseries_Garry.ipynb`, including:
- stationarity tests,
- ACF/PACF diagnostics,
- ARIMA forecasting.

Then we added an extension: ARIMA + ML residual modeling using `scripts/residual_features.py`.

We compared:
1) ARIMA only  
2) ML only (RandomForest predicts returns directly)  
3) Hybrid (ARIMA prediction + ML residual prediction)

Current AAPL result under this setup:
- ARIMA only RMSE: **0.01706026**
- ML only RMSE: **0.01813747**
- Hybrid RMSE: **0.01787769**

So far, ARIMA baseline is best. This means residual modeling has not yet outperformed the baseline under current feature/parameter choices.

Next steps:
- richer residual features,
- walk-forward validation,
- and robustness checks across multiple tickers.

---

## 2) Live Demo Order (what to show first)

1. `outputs/metrics.csv` (quick summary table)
2. `outputs/A1figs/price_sample.png`
3. `outputs/A1figs/corr_heatmap.png`
4. `outputs/A1figs/risk_return_scatter.png`
5. `outputs/timeseries_figs/arima_forecast.png`
6. `scripts/Timeseries_Garry.ipynb` section: **ARIMA + ML Residual Extension**

---

## 3) Key Results to Mention

- Highest annualized return and Sharpe: **NVDA** (`72.21%`, Sharpe `1.48`)
- Balanced risk-adjusted profile: **MSFT** (Sharpe `0.95`)
- Deepest drawdown: **META** (`-76.74%`)
- Correlation is relatively high among tech names; lower between tech and defensive names.
- Current predictive comparison on AAPL: **ARIMA > Hybrid > ML-only** by RMSE.

---

## 4) Short Q&A Answers

### Q: Why add ML residual modeling?
To test whether ARIMA residuals still contain learnable structure (nonlinear/state-dependent effects).

### Q: What does it mean if hybrid does not beat ARIMA?
Under current setup, we do not have strong evidence that residual structure is exploitable enough to improve forecast error.

### Q: Why can ARIMA still win?
Daily returns are very noisy; baseline linear structure may be as good as current feature set allows.

### Q: What are next technical improvements?
Feature enrichment (rolling stats/regime flags), walk-forward backtesting, and broader ticker-level evaluation.

---

## 5) Quick File Map

- Data: `data/Prices.csv`
- EDA notebook: `notebook/eda.ipynb`
- Time-series notebook: `scripts/Timeseries_Garry.ipynb`
- Residual modeling utilities: `scripts/residual_features.py`
- EDA outputs: `outputs/returns.csv`, `outputs/metrics.csv`, `outputs/corr.csv`
- Meeting figures: `outputs/A1figs/*.png`, `outputs/timeseries_figs/*.png`
- Reports: `report/assignment1Q1.md`, `report/EDA_report.md`
