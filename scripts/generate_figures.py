"""Generate EDA figures and save to outputs/figs/"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "Prices.csv"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGS_DIR = OUTPUTS_DIR / "figs"
FIGS_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("husl")

TRADING_DAYS = 252
REP_TICKERS = ["AAPL", "AMZN", "NVDA", "JNJ", "XOM", "META"]
WINDOW = 21

# Load data
df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)
price_cols = [c for c in df.columns if c != "Date"]
prices = df[price_cols].ffill().bfill()
df_clean = df.copy()
df_clean[price_cols] = prices
df_clean = df_clean.dropna(how="any").reset_index(drop=True)

# Returns
ret_only = df_clean[price_cols].pct_change().dropna(how="all")
ret_dates = df_clean["Date"].iloc[1:].reset_index(drop=True)

# Metrics
def annualized_return(r):
    prod_gross = (1 + r).prod()
    T = r.dropna().count()
    return prod_gross ** (TRADING_DAYS / T) - 1 if T > 0 else np.nan

def annualized_vol(r):
    return r.std() * np.sqrt(TRADING_DAYS)

def sharpe_ratio(r, rf=0):
    ann_ret = annualized_return(r)
    ann_vol = annualized_vol(r)
    return (ann_ret - rf) / ann_vol if ann_vol > 0 else np.nan

def max_drawdown(r):
    cum = (1 + r).cumprod()
    rolling_max = cum.cummax()
    dd = (cum - rolling_max) / rolling_max
    return dd.min()

metrics = pd.DataFrame({
    "annualized_return": ret_only.apply(annualized_return),
    "annualized_volatility": ret_only.apply(annualized_vol),
    "sharpe_ratio": ret_only.apply(sharpe_ratio),
    "max_drawdown": ret_only.apply(max_drawdown),
})
corr = ret_only.corr()
cum = (1 + ret_only).cumprod()
drawdown = (cum - cum.cummax()) / cum.cummax()
roll_vol = ret_only.rolling(WINDOW).std() * np.sqrt(TRADING_DAYS) * 100

# 1. Price curves
fig, ax = plt.subplots(figsize=(12, 5))
for t in REP_TICKERS:
    if t in df_clean.columns:
        ax.plot(df_clean["Date"], df_clean[t], label=t, alpha=0.8)
ax.set_title("Adjusted Close Prices — Representative Tickers")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend(loc="upper left", ncol=2)
ax.set_xlim(df_clean["Date"].min(), df_clean["Date"].max())
plt.tight_layout()
plt.savefig(FIGS_DIR / "price_sample.png", dpi=150, bbox_inches="tight")
plt.close()

# 2. Return distributions
fig, axes = plt.subplots(2, 5, figsize=(14, 6))
axes = axes.flatten()
for i, t in enumerate(price_cols):
    ret_only[t].dropna().hist(bins=50, ax=axes[i], density=True, alpha=0.6, edgecolor="white")
    ret_only[t].dropna().plot(kind="kde", ax=axes[i], color="darkblue", lw=2)
    axes[i].set_title(t)
    axes[i].set_xlabel("Daily return")
for j in range(i + 1, len(axes)):
    axes[j].axis("off")
fig.suptitle("Return Distributions by Ticker", fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(FIGS_DIR / "return_hist.png", dpi=150, bbox_inches="tight")
plt.close()

# 3. Rolling volatility
fig, ax = plt.subplots(figsize=(12, 4))
for t in REP_TICKERS:
    if t in roll_vol.columns:
        ax.plot(ret_dates, roll_vol[t], label=t, alpha=0.7)
ax.set_title(f"Rolling Annualized Volatility ({WINDOW}-day window)")
ax.set_xlabel("Date")
ax.set_ylabel("Volatility (%)")
ax.legend(loc="upper right", ncol=2)
plt.tight_layout()
plt.savefig(FIGS_DIR / "rolling_vol.png", dpi=150, bbox_inches="tight")
plt.close()

# 4. Drawdown
fig, ax = plt.subplots(figsize=(12, 4))
for t in REP_TICKERS:
    if t in drawdown.columns:
        ax.fill_between(ret_dates, 0, drawdown[t], alpha=0.4, label=t)
ax.set_title("Drawdowns Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Drawdown")
ax.legend(loc="lower left", ncol=2)
ax.set_ylim(-1, 0.1)
plt.tight_layout()
plt.savefig(FIGS_DIR / "drawdown.png", dpi=150, bbox_inches="tight")
plt.close()

# 5. Correlation heatmap
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, vmin=-1, vmax=1, ax=ax)
ax.set_title("Return Correlation Heatmap")
plt.tight_layout()
plt.savefig(FIGS_DIR / "corr_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()

# 6a. Top/bottom return
fig, ax = plt.subplots(figsize=(8, 5))
m = metrics.sort_values("annualized_return", ascending=False)
colors = ["green" if v >= 0 else "red" for v in m["annualized_return"]]
m["annualized_return"].plot(kind="barh", ax=ax, color=colors)
ax.axvline(0, color="black", lw=0.5)
ax.set_title("Annualized Return by Ticker (Top / Bottom)")
ax.set_xlabel("Annualized Return")
plt.tight_layout()
plt.savefig(FIGS_DIR / "top_bottom_return.png", dpi=150, bbox_inches="tight")
plt.close()

# 6b. Sharpe ratio
fig, ax = plt.subplots(figsize=(8, 5))
m = metrics.sort_values("sharpe_ratio", ascending=False)
m["sharpe_ratio"].plot(kind="barh", ax=ax, color="steelblue")
ax.axvline(0, color="black", lw=0.5)
ax.set_title("Sharpe Ratio by Ticker")
ax.set_xlabel("Sharpe Ratio (rf=0)")
plt.tight_layout()
plt.savefig(FIGS_DIR / "sharpe_ratio.png", dpi=150, bbox_inches="tight")
plt.close()

# 6c. Vol and drawdown
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
metrics.sort_values("annualized_volatility")["annualized_volatility"].plot(kind="barh", ax=axes[0], color="coral")
axes[0].set_title("Annualized Volatility")
axes[0].set_xlabel("Volatility")
metrics.sort_values("max_drawdown")["max_drawdown"].plot(kind="barh", ax=axes[1], color="purple")
axes[1].set_title("Maximum Drawdown")
axes[1].set_xlabel("Max Drawdown")
plt.tight_layout()
plt.savefig(FIGS_DIR / "top_bottom_metrics.png", dpi=150, bbox_inches="tight")
plt.close()

# 7. Cumulative returns
fig, ax = plt.subplots(figsize=(12, 5))
for t in REP_TICKERS:
    if t in cum.columns:
        ax.plot(ret_dates, cum[t], label=t, alpha=0.8)
ax.set_title("Cumulative Returns (Normalized to 1)")
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Return")
ax.legend(loc="upper left", ncol=2)
ax.axhline(1, color="gray", ls="--", lw=1)
plt.tight_layout()
plt.savefig(FIGS_DIR / "cum_returns.png", dpi=150, bbox_inches="tight")
plt.close()

# 8. AAPL daily returns
fig, ax = plt.subplots(figsize=(12, 3))
ax.bar(ret_dates, ret_only["AAPL"] * 100, width=1, alpha=0.6)
ax.axhline(0, color="black", lw=0.5)
ax.set_title("AAPL Daily Returns (%)")
ax.set_xlabel("Date")
ax.set_ylabel("Return (%)")
plt.tight_layout()
plt.savefig(FIGS_DIR / "return_ts_aapl.png", dpi=150, bbox_inches="tight")
plt.close()

# 9. Box plot
fig, ax = plt.subplots(figsize=(10, 5))
ret_only[price_cols].boxplot(ax=ax)
ax.set_title("Return Distribution by Ticker (Box Plot)")
ax.set_ylabel("Daily Return")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(FIGS_DIR / "return_boxplot.png", dpi=150, bbox_inches="tight")
plt.close()

# 10. Risk-return scatter
fig, ax = plt.subplots(figsize=(8, 6))
for t in metrics.index:
    ax.scatter(metrics.loc[t, "annualized_volatility"] * 100,
               metrics.loc[t, "annualized_return"] * 100, s=100, label=t)
    ax.annotate(t, (metrics.loc[t, "annualized_volatility"] * 100,
                metrics.loc[t, "annualized_return"] * 100),
                fontsize=9, alpha=0.8)
ax.set_xlabel("Annualized Volatility (%)")
ax.set_ylabel("Annualized Return (%)")
ax.set_title("Risk-Return Trade-off by Ticker")
ax.axhline(0, color="gray", ls="--", lw=0.5)
ax.axvline(0, color="gray", ls="--", lw=0.5)
plt.tight_layout()
plt.savefig(FIGS_DIR / "risk_return_scatter.png", dpi=150, bbox_inches="tight")
plt.close()

print("Generated 12 figures in", FIGS_DIR)
