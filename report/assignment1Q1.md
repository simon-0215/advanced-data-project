# Problem 1: Exploratory Analysis for the Final Project

**Course:GR5291** 
**Assignment:** HW1 Problem 1 — Exploratory Analysis (15 pts)  
**Project:** S&P 500 Stock Portfolio Analysis  

---

## 1.i Project Teammates

| Name | UNI |
|------|-----|
| Mingyang Xu | mx2315 |
| ian | cw3736 |
| Zhiyuan Lu | zl3622 |
| Yandi Zhang | yz5124 |
| Daile Yang | dy2540 |


*Please replace the placeholders above with your team members’ names and UNIs.*

---

## 1.ii Description of Collected Data

### Data Source
We collected **S&P 500 stock price data** from Kaggle (2015–2025) for portfolio optimization. The dataset contains adjusted close prices for 10 representative tickers across technology, consumer goods, healthcare, finance, and energy sectors.

| Attribute | Description |
|-----------|-------------|
| **Dataset** | S&P 500 Stock Prices (Portfolio Optimization, 2015–2025) |
| **Platform** | Kaggle |
| **Link** | [Kaggle Dataset](https://www.kaggle.com/datasets/hiteshyadavx/s-and-p-500-stock-prices) |
| **File** | `Prices.csv` |
| **Format** | Wide table: rows = trading days, columns = Date + stock tickers |
| **Values** | Adjusted close prices (USD) |
| **Date range** | 2015-01-02 to 2025-12-30 |
| **Sample size** | 2,765 trading days |
| **Tickers** | AAPL, AMZN, GOOGL, JNJ, JPM, META, MSFT, NVDA, PG, XOM |

### Data Structure
The data is stored in wide format: each row represents a trading day, and each column (except `Date`) represents one stock’s adjusted close price. We used simple daily returns \( r_t = (P_t - P_{t-1}) / P_{t-1} \) for all analyses. Missing values were handled via forward-fill. All metrics assume no transaction costs, no slippage, and long-only positions.

---

## 1.iii Descriptive Statistics

### Summary by Ticker

| Ticker | Annualized Return | Annualized Volatility | Sharpe Ratio (rf=0) | Max Drawdown |
|--------|-------------------|------------------------|---------------------|--------------|
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

### Aggregate Statistics (across tickers)

| Metric | Mean | Std | Min | Max |
|--------|------|-----|-----|-----|
| Annualized Return | 23.11% | 21.22% | 6.95% | 72.21% |
| Annualized Volatility | 29.40% | 8.84% | 18.20% | 48.70% |
| Sharpe Ratio | 0.74 | 0.39 | 0.25 | 1.48 |
| Max Drawdown | -47.65% | 17.79% | -76.74% | -24.50% |

### Daily Returns (2,764 observations per ticker)

| Statistic | Value |
|-----------|-------|
| Mean daily return (avg across tickers) | ~0.0009 (0.09%) |
| Typical daily volatility (annualized) | ~25–35% |
| No. of trading days | 2,764 |

---

## 1.iv Graphics

### Plot 1: Price Trajectories (Representative Tickers)

Shows adjusted close prices over time for six representative stocks across sectors.

![Price curves](https://raw.githubusercontent.com/simon-0215/advanced-data-project/main/outputs/A1figs/price_sample.png)

---

### Plot 2: Correlation Heatmap — *Three Dimensions in One Plot*

This figure visualizes **three dimensions** in a single graphic:
- **Dimension 1 (rows):** Stock A
- **Dimension 2 (columns):** Stock B  
- **Dimension 3 (color):** Correlation coefficient between their daily returns

Color intensity indicates strength and direction of correlation (red = stronger positive, blue = negative).

![Correlation heatmap](https://raw.githubusercontent.com/simon-0215/advanced-data-project/main/outputs/A1figs/corr_heatmap.png)

---

### Plot 3: Risk–Return Trade-off (Scatter)

Annualized volatility (x-axis) vs. annualized return (y-axis) for each stock. Points farther up and left are more attractive (higher return, lower risk).

![Risk-return scatter](https://raw.githubusercontent.com/simon-0215/advanced-data-project/main/outputs/A1figs/risk_return_scatter.png)

---

### Plot 4: Rolling Volatility Over Time

21-day rolling annualized volatility for six representative tickers. Captures time-varying risk, including periods such as COVID-19 in 2020.

![Rolling volatility](https://raw.githubusercontent.com/simon-0215/advanced-data-project/main/outputs/A1figs/rolling_vol.png)

---

### Plot 5: Drawdowns Over Time

Drawdown (peak-to-trough decline) for six tickers over the sample period. Useful for assessing worst-case losses and recovery periods.

![Drawdowns](https://raw.githubusercontent.com/simon-0215/advanced-data-project/main/outputs/A1figs/drawdown.png)

---

## 1.v Comments on Descriptive Statistics and Graphics

### Descriptive Statistics

- **Return dispersion:** NVDA stands out with ~72% annualized return; defensive names (JNJ, PG, XOM) stay in the 7–10% range. Tech and growth stocks generally outperform.
- **Risk profiles:** NVDA and META have the highest volatility; JNJ and PG have the lowest. Sharpe ratios range from 0.25 (XOM) to 1.48 (NVDA).
- **Drawdowns:** META shows the deepest max drawdown (-76.74%); PG the shallowest (-24.50%). Larger drawdowns tend to occur in higher-volatility tech names.

### Graphics

1. **Price trajectories** — NVDA and other tech names show strong long-term appreciation; XOM and JNJ are more stable and range-bound. This aligns with growth vs. value / defensive styles.

2. **Correlation heatmap** — Tech stocks (AAPL, AMZN, GOOGL, MSFT, NVDA, META) are highly correlated with each other (0.48–0.68). JNJ and PG are less correlated with tech, supporting diversification. JPM and XOM are moderately correlated (~0.54), consistent with financial and energy sectors moving together in certain regimes.

3. **Risk–return scatter** — NVDA is high risk and high return; MSFT and GOOGL offer relatively better risk-adjusted returns. JNJ and PG sit in the low-risk, low-return region. This suggests that a portfolio combining high-Sharpe tech with defensive names could improve risk-adjusted performance.

4. **Rolling volatility** — Volatility spikes during 2020 (COVID-19) and other stress periods, then reverts. NVDA and META exhibit the largest swings; JNJ and PG are more stable. This supports using time-varying or regime-dependent models for portfolio allocation.

5. **Drawdowns** — Major drawdown episodes align with known market events (e.g., COVID, rate hikes). META’s drawdown is particularly deep; PG and JNJ recover faster. Drawdown analysis is useful for sizing positions and setting risk limits.

### Overall

The data and graphics support the following: (1) tech stocks dominate returns but with higher risk; (2) defensive names (JNJ, PG) provide diversification benefits; (3) correlations and risk are time-varying; (4) a combination of high-Sharpe tech and low-correlation defensive assets is a natural direction for portfolio construction.

---

*Report generated from the advanced-data-project EDA pipeline. Code and data: [GitHub](https://github.com/simon-0215/advanced-data-project).*
