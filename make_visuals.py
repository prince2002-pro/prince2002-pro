"""Generates the animated SVGs and the fraud-detection demo chart used in README.md.
Run from the repo root: python scripts/make_visuals.py   (needs numpy, matplotlib, scikit-learn)
"""
import random
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)
FONT = "font-family:'Segoe UI',Helvetica,Arial,sans-serif"
TEAL, AMBER = "#0f766e", "#f0a93b"

# ---------- Animated banner ----------
random.seed(7)
heights = [60, 78, 70, 95, 88, 112, 104, 130, 124, 150, 146, 172]
bars, pts = [], []
for i, h in enumerate(heights):
    x = 660 + i * 42
    bars.append(f'<rect class="bar" style="animation-delay:{i*.12:.2f}s" x="{x}" y="{290-h}" width="26" height="{h}" rx="4" fill="#12template" opacity=".35"/>'.replace("#12template", "#2dd4bf"))
    pts.append((x + 13, 290 - h - 18 - random.randint(0, 14)))
path = "M" + " L".join(f"{x},{y}" for x, y in pts)
banner = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 320" width="1200" height="320" role="img" aria-label="Prince Muhindo Visanguliryo, Data Scientist and Analyst">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a1620"/><stop offset="1" stop-color="#0f4c47"/></linearGradient>
<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="#2dd4bf"/><stop offset="1" stop-color="{AMBER}"/></linearGradient></defs>
<style>
.n{{{FONT};font-weight:700;font-size:48px;fill:#fff}}.t{{{FONT};font-size:24px;fill:#9fe3da}}.s{{{FONT};font-size:16px;fill:#b8c7d2}}
.fade{{opacity:0;animation:f 1s ease-out forwards}}@keyframes f{{to{{opacity:1}}}}
.bar{{transform-box:fill-box;transform-origin:bottom;animation:r 1s ease-out backwards}}@keyframes r{{from{{transform:scaleY(0)}}}}
.ln{{fill:none;stroke:url(#ln);stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:900;stroke-dashoffset:900;animation:d 2.6s .6s ease-out forwards}}@keyframes d{{to{{stroke-dashoffset:0}}}}
.dot{{fill:{AMBER};opacity:0;animation:f .5s 3s forwards}}
@media (prefers-reduced-motion:reduce){{.fade,.dot{{animation:none;opacity:1}}.bar{{animation:none}}.ln{{animation:none;stroke-dashoffset:0}}}}
</style>
<rect width="1200" height="320" fill="url(#bg)"/>
<g stroke="#ffffff" stroke-opacity=".06">{"".join(f'<line x1="0" x2="1200" y1="{y}" y2="{y}"/>' for y in range(50,320,60))}</g>
{"".join(bars)}
<path class="ln" d="{path}"/><circle class="dot" cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="7"/>
<text class="n fade" x="60" y="130">Prince Muhindo</text><text class="n fade" x="60" y="188" style="animation-delay:.2s">Visanguliryo</text>
<text class="t fade" x="60" y="232" style="animation-delay:.5s">Data Scientist and Analyst</text>
<text class="s fade" x="60" y="266" style="animation-delay:.8s">Dashboards  |  Python and SQL  |  MEAL and indicator monitoring  |  FR / EN / SW</text>
</svg>'''
(OUT / "banner.svg").write_text(banner, encoding="utf-8")

# ---------- Animated impact stats (figures from the CV) ----------
stats = [("70%", "less manual reporting time", "Power BI dashboard"), ("6+ hrs", "saved every week", "Automated Python reports"),
         ("20,000+", "rows cleaned and standardised", "Pandas and Tableau"), ("3", "working languages", "French, English, Swahili")]
cards = ""
for i, (big, lab, sub) in enumerate(stats):
    x = 30 + i * 290
    cards += f'''<g class="c" style="animation-delay:{i*.25}s"><rect x="{x}" y="10" width="270" height="130" rx="12" fill="#f4f8f9" stroke="#d3dfe4"/>
<rect x="{x}" y="10" width="6" height="130" rx="3" fill="{TEAL}"/>
<text x="{x+28}" y="68" style="{FONT};font-weight:700;font-size:40px;fill:#10222f">{big}</text>
<text x="{x+28}" y="96" style="{FONT};font-size:15px;fill:#10222f">{lab}</text>
<text x="{x+28}" y="120" style="{FONT};font-size:13px;fill:#5b6b78">{sub}</text></g>'''
(OUT / "stats.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 150" width="1200" height="150" role="img" aria-label="Impact highlights">
<style>.c{{opacity:0;transform:translateY(12px);animation:u .7s ease-out forwards}}@keyframes u{{to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion:reduce){{.c{{animation:none;opacity:1;transform:none}}}}</style>{cards}</svg>''', encoding="utf-8")

# ---------- Toolkit map ----------
cols = {"Languages": ["Python", "SQL", "R", "JavaScript"], "Data and BI": ["Power BI", "Tableau", "Metabase", "Excel and VBA"],
        "Databases": ["PostgreSQL", "MongoDB", "MS Access", "Database design and QA"],
        "Data collection": ["Kobo Toolbox", "XLSForm", "APIs", "Data validation"], "Python stack": ["Pandas", "NumPy", "Plotly", "Anomaly detection"]}
colors = [TEAL, "#1d3f5c", "#8a5a06", "#0b4f4a", "#34566f"]
g = ""
for i, (title, items) in enumerate(cols.items()):
    x = 20 + i * 232
    g += f'<text x="{x}" y="34" style="{FONT};font-weight:700;font-size:17px;fill:#10222f">{title}</text><rect x="{x}" y="44" width="40" height="4" rx="2" fill="{colors[i]}"/>'
    for j, it in enumerate(items):
        y = 64 + j * 46
        g += f'<g class="p" style="animation-delay:{(i*4+j)*.06:.2f}s"><rect x="{x}" y="{y}" width="212" height="36" rx="18" fill="{colors[i]}" fill-opacity=".1" stroke="{colors[i]}" stroke-opacity=".5"/><text x="{x+106}" y="{y+23}" text-anchor="middle" style="{FONT};font-size:14px;fill:#10222f">{it}</text></g>'
(OUT / "toolkit.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 260" width="1200" height="260" role="img" aria-label="Toolkit">
<style>.p{{opacity:0;animation:f .5s ease-out forwards}}@keyframes f{{to{{opacity:1}}}}@media (prefers-reduced-motion:reduce){{.p{{animation:none;opacity:1}}}}</style>{g}</svg>''', encoding="utf-8")

# ---------- Fraud detection demo (synthetic data, Isolation Forest) ----------
rng = np.random.default_rng(1)
normal = np.c_[rng.normal(3.6, 0.7, 2500), rng.normal(5.0, 1.2, 2500)]
fraud = np.c_[rng.normal(6.4, 0.8, 45), rng.normal(0.6, 0.6, 45)]
X = np.vstack([normal, fraud]); y = np.r_[np.zeros(len(normal)), np.ones(len(fraud))]
pred = IsolationForest(contamination=0.02, random_state=1).fit_predict(X) == -1
tp = int((pred & (y == 1)).sum())
fig, ax = plt.subplots(figsize=(9, 5.2))
ax.scatter(*X[~pred].T, s=9, c="#0f766e", alpha=.35, label="Normal")
ax.scatter(*X[pred].T, s=26, c="#c2790a", edgecolors="#10222f", linewidths=.4, label=f"Flagged ({pred.sum()})")
ax.set_xlabel("Transaction amount (log scale)"); ax.set_ylabel("Hours since previous transaction")
ax.set_title(f"Isolation Forest on synthetic card transactions: {tp} of {len(fraud)} seeded anomalies caught", loc="left", fontsize=11.5, fontweight="bold", color="#10222f")
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.legend(frameon=False); fig.tight_layout(); fig.savefig(OUT / "fraud-demo.png", dpi=130); plt.close(fig)
print("flagged", pred.sum(), "caught", tp, "of", len(fraud))
