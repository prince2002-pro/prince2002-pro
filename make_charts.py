"""Builds the chart images used in README.md from data/sales.csv (synthetic data).
Run from the repo root: python scripts/make_charts.py   (needs pandas, matplotlib)
"""
import json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
NAVY, TEAL, AMBER, SLATE, MUTED, LINE = "#10222f", "#0f766e", "#c2790a", "#1d3f5c", "#5b6b78", "#d9e1e7"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#c9d4da", "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
df = pd.read_csv(ROOT / "data" / "sales.csv", parse_dates=["month"])
df["year"] = df.month.dt.year
K = lambda v, _=None: f"{v/1e3:,.0f}K"
M = lambda v: f"KES {v/1e6:.1f}M"
title = lambda ax, t: ax.set_title(t, loc="left", fontsize=14, fontweight="bold", color=NAVY, pad=14)

# 1. Revenue and profit trend
m = df.groupby("month")[["revenue", "profit"]].sum()
fig, ax = plt.subplots(figsize=(11, 4.8))
ax.fill_between(m.index, m.revenue, color=TEAL, alpha=.12)
ax.plot(m.index, m.revenue, color=TEAL, lw=2.6, label="Revenue")
ax.plot(m.index, m.profit, color=AMBER, lw=2.6, label="Profit")
ax.plot(m.index, m.revenue.rolling(3).mean(), color=SLATE, lw=1.4, ls="--", label="Revenue, 3-month average")
pk = m.revenue.idxmax()
ax.annotate(f"Peak: {pk:%b %Y}\nKES {m.revenue.max()/1e3:,.0f}K", (pk, m.revenue.max()), xytext=(-95, -8), textcoords="offset points",
            fontsize=10, color=NAVY, arrowprops=dict(arrowstyle="->", color=MUTED))
ax.yaxis.set_major_formatter(K); ax.set_ylim(0); ax.grid(axis="y", color=LINE, lw=.8); ax.legend(frameon=False, loc="upper left", ncol=3)
title(ax, "Monthly revenue and profit (KES, synthetic data)"); fig.tight_layout(); fig.savefig(OUT / "revenue-profit-trend.png", dpi=130); plt.close(fig)

# 2. Regional performance, 2024 vs 2025
r = df.pivot_table(index="region", columns="year", values="revenue", aggfunc="sum").sort_values(2025, ascending=False)
fig, ax = plt.subplots(figsize=(11, 4.8)); w = .38; xs = range(len(r))
ax.bar([x - w/2 for x in xs], r[2024], w, color="#8aa5b8", label="2024"); ax.bar([x + w/2 for x in xs], r[2025], w, color=TEAL, label="2025")
for x, (a, b) in enumerate(zip(r[2024], r[2025])):
    ax.text(x + w/2, b, f"+{(b/a-1)*100:.0f}%", ha="center", va="bottom", fontsize=11, fontweight="bold", color=TEAL)
ax.set_xticks(list(xs)); ax.set_xticklabels(r.index, fontsize=11); ax.yaxis.set_major_formatter(lambda v, _: f"{v/1e6:.1f}M")
ax.grid(axis="y", color=LINE, lw=.8); ax.set_axisbelow(True); ax.legend(frameon=False); ax.set_ylim(0, r.values.max() * 1.15)
title(ax, "Revenue by region, 2024 vs 2025 (KES), with year-on-year growth"); fig.tight_layout(); fig.savefig(OUT / "regional-performance.png", dpi=130); plt.close(fig)

# 3. Product category performance
c = df.groupby("category")[["revenue", "profit"]].sum(); c["margin"] = c.profit / c.revenue * 100; c = c.sort_values("revenue", ascending=False)
cols = [TEAL, SLATE, AMBER]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1, 1.1]})
a1.pie(c.revenue, labels=c.index, autopct="%1.0f%%", colors=cols, startangle=90, wedgeprops=dict(width=.42, edgecolor="white"), textprops={"fontsize": 11})
a1.set_title("Revenue share", loc="left", fontsize=13, fontweight="bold", color=NAVY)
b = a2.barh(c.index[::-1], c.margin[::-1], color=cols[::-1], height=.55)
for rect, v in zip(b, c.margin[::-1]): a2.text(v + .6, rect.get_y() + rect.get_height()/2, f"{v:.1f}%", va="center", fontsize=11, fontweight="bold", color=NAVY)
a2.set_xlim(0, c.margin.max() * 1.2); a2.set_title("Profit margin", loc="left", fontsize=13, fontweight="bold", color=NAVY)
a2.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%"); a2.grid(axis="x", color=LINE, lw=.8); a2.set_axisbelow(True)
fig.suptitle("Product category performance", x=.02, ha="left", fontsize=14, fontweight="bold", color=NAVY); fig.tight_layout(rect=(0, 0, 1, .93))
fig.savefig(OUT / "product-performance.png", dpi=130); plt.close(fig)

# 4. KPI cards (all figures derived from the data)
rev, pro = df.revenue.sum(), df.profit.sum(); y = df.groupby("year").revenue.sum(); reg = df.groupby("region").revenue.sum().sort_values(ascending=False)
kp = [("TOTAL REVENUE", M(rev), "24 months"), ("TOTAL PROFIT", M(pro), "24 months"), ("PROFIT MARGIN", f"{pro/rev*100:.1f}%", "all categories"),
      ("2025 GROWTH", f"+{(y[2025]/y[2024]-1)*100:.1f}%", "revenue vs 2024"), ("TOP REGION", reg.index[0], f"{reg.iloc[0]/rev*100:.0f}% of revenue"),
      ("PEAK MONTH", f"{pk:%b %Y}", f"KES {m.revenue.max()/1e3:,.0f}K")]
fig, ax = plt.subplots(figsize=(12, 4.4)); ax.set_xlim(0, 12); ax.set_ylim(0, 4.4); ax.axis("off")
for i, (lab, val, sub) in enumerate(kp):
    x, yy = .15 + (i % 3) * 3.95, 2.35 - (i // 3) * 2.15
    ax.add_patch(FancyBboxPatch((x, yy), 3.7, 1.9, boxstyle="round,pad=0.02,rounding_size=0.12", fc="#f4f8f9", ec=LINE))
    ax.add_patch(FancyBboxPatch((x, yy), .09, 1.9, boxstyle="square,pad=0", fc=[TEAL, AMBER][i % 2], ec="none"))
    ax.text(x + .35, yy + 1.45, lab, fontsize=10, color=MUTED, fontweight="bold"); ax.text(x + .35, yy + .75, val, fontsize=26, color=NAVY, fontweight="bold")
    ax.text(x + .35, yy + .25, sub, fontsize=10.5, color=MUTED)
fig.savefig(OUT / "kpi-dashboard.png", dpi=130, bbox_inches="tight"); plt.close(fig)

# 5. Workflow diagram
steps = [("Collect", "Kobo Toolbox\nAPIs, SQL"), ("Clean", "Python\nPandas"), ("Validate", "QA checks\nData governance"), ("Store", "PostgreSQL\nMongoDB"),
         ("Analyse", "Python, R\nExcel"), ("Visualise", "Power BI, Tableau\nMetabase"), ("Decide", "KPI and MEAL\nreporting")]
fig, ax = plt.subplots(figsize=(13, 3.2)); ax.set_xlim(0, 13); ax.set_ylim(0, 3.2); ax.axis("off")
for i, (h, s) in enumerate(steps):
    x = .2 + i * 1.85; col = AMBER if i == len(steps) - 1 else TEAL
    ax.add_patch(FancyBboxPatch((x, 1.35), 1.55, .95, boxstyle="round,pad=0.02,rounding_size=0.14", fc=col, ec="none"))
    ax.text(x + .775, 1.82, h, ha="center", va="center", color="white", fontsize=13, fontweight="bold")
    ax.text(x + .775, .78, s, ha="center", va="center", color=NAVY, fontsize=9.5, linespacing=1.5)
    ax.text(x + .775, 2.55, str(i + 1), ha="center", va="center", color=MUTED, fontsize=10, fontweight="bold")
    if i < len(steps) - 1: ax.add_patch(FancyArrowPatch((x + 1.58, 1.82), (x + 1.82, 1.82), arrowstyle="-|>", mutation_scale=14, color=MUTED, lw=1.6))
fig.savefig(OUT / "data-analytics-workflow.png", dpi=130, bbox_inches="tight"); plt.close(fig)

print(json.dumps({"rev": int(rev), "profit": int(pro), "margin": round(pro/rev*100, 1), "growth": round((y[2025]/y[2024]-1)*100, 1),
  "top": reg.index[0], "top_share": round(reg.iloc[0]/rev*100), "peak": f"{pk:%b %Y}", "regional_growth": {k: round((r.loc[k, 2025]/r.loc[k, 2024]-1)*100) for k in r.index},
  "margins": c.margin.round(1).to_dict(), "shares": (c.revenue/rev*100).round().to_dict()}))
