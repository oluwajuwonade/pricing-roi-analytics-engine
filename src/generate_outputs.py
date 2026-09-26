from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from economics import break_even_units, roi

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
DATA.mkdir(exist_ok=True)
OUTPUTS.mkdir(exist_ok=True)

SCENARIOS = {
    "Downside": {"price": 95.0, "volume": 8500, "variable_cost": 54.0, "fixed_cost": 240000, "investment": 500000},
    "Base": {"price": 110.0, "volume": 10000, "variable_cost": 48.0, "fixed_cost": 240000, "investment": 500000},
    "Upside": {"price": 125.0, "volume": 11500, "variable_cost": 45.0, "fixed_cost": 240000, "investment": 500000},
}


def calculate_scenario(name: str, values: dict[str, float]) -> dict[str, float | str]:
    revenue = values["price"] * values["volume"]
    variable_total = values["variable_cost"] * values["volume"]
    contribution = revenue - variable_total
    operating_profit = contribution - values["fixed_cost"]
    return {"scenario": name, **values, "revenue": revenue, "variable_total": variable_total, "contribution": contribution, "contribution_margin": contribution / revenue, "operating_profit": operating_profit, "break_even_units": break_even_units(values["fixed_cost"], values["price"], values["variable_cost"]), "roi": roi(operating_profit, values["investment"])}


def main() -> None:
    assumptions = pd.DataFrame([{ "scenario": name, **values } for name, values in SCENARIOS.items()])
    assumptions.to_csv(DATA / "assumptions.csv", index=False)
    scenario_df = pd.DataFrame([calculate_scenario(name, values) for name, values in SCENARIOS.items()])
    scenario_df.to_csv(OUTPUTS / "scenario_economics.csv", index=False)

    prices = np.arange(80, 141, 5)
    volumes = np.arange(6000, 14001, 1000)
    rows = []
    for price in prices:
        for volume in volumes:
            variable_cost = SCENARIOS["Base"]["variable_cost"]
            contribution = (price - variable_cost) * volume
            profit = contribution - SCENARIOS["Base"]["fixed_cost"]
            rows.append({"price": price, "volume": volume, "operating_profit": profit, "contribution_margin": (price - variable_cost) / price})
    sensitivity = pd.DataFrame(rows)
    sensitivity.to_csv(OUTPUTS / "price_volume_sensitivity.csv", index=False)

    plt.style.use("seaborn-v0_8-whitegrid")
    colors = {"Downside": "#C2413B", "Base": "#2563EB", "Upside": "#15803D"}
    fig, ax = plt.subplots(figsize=(9, 5.2))
    for scenario in SCENARIOS:
        row = scenario_df[scenario_df["scenario"] == scenario].iloc[0]
        ax.bar(scenario, row["roi"] * 100, color=colors[scenario], width=0.6)
        ax.text(scenario, row["roi"] * 100 + 2, f"{row['roi']:.1%}", ha="center", weight="bold")
    ax.axhline(0, color="#334155", linewidth=0.8)
    ax.set_title("Illustrative ROI by Commercial Scenario", loc="left", weight="bold")
    ax.set_ylabel("ROI (%)"); ax.set_xlabel("")
    fig.tight_layout(); fig.savefig(OUTPUTS / "scenario_roi.png", dpi=180); plt.close(fig)

    pivot = sensitivity.pivot(index="volume", columns="price", values="operating_profit") / 1000
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    im = ax.imshow(pivot.values, aspect="auto", cmap="RdYlGn", vmin=-300, vmax=700)
    ax.set_title("Operating Profit Sensitivity: Price × Volume", loc="left", weight="bold")
    ax.set_xlabel("Price ($)"); ax.set_ylabel("Annual units")
    ax.set_xticks(range(len(pivot.columns))); ax.set_xticklabels([f"${x:.0f}" for x in pivot.columns], rotation=45, ha="right")
    ax.set_yticks(range(len(pivot.index))); ax.set_yticklabels([f"{x:,.0f}" for x in pivot.index])
    fig.colorbar(im, ax=ax, label="Operating profit ($000)")
    fig.tight_layout(); fig.savefig(OUTPUTS / "price_volume_heatmap.png", dpi=180); plt.close(fig)

    base = scenario_df[scenario_df["scenario"] == "Base"].iloc[0]
    components = ["Revenue", "Variable cost", "Fixed cost", "Operating profit"]
    values = [base["revenue"], -base["variable_total"], -base["fixed_cost"], base["operating_profit"]]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    bars = ax.bar(components, np.array(values) / 1000, color=["#0F766E", "#F59E0B", "#94A3B8", "#2563EB"])
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (18 if value >= 0 else -35), f"${value/1000:,.0f}k", ha="center", va="bottom" if value >= 0 else "top", fontsize=9)
    ax.axhline(0, color="#334155", linewidth=0.8)
    ax.set_title("Base Case Unit-Economics Bridge", loc="left", weight="bold")
    ax.set_ylabel("Annual value ($000)")
    fig.tight_layout(); fig.savefig(OUTPUTS / "base_case_bridge.png", dpi=180); plt.close(fig)

    best = scenario_df.loc[scenario_df["roi"].idxmax()]
    base_row = scenario_df[scenario_df["scenario"] == "Base"].iloc[0]
    (OUTPUTS / "executive_summary.md").write_text(f"""# Executive Summary — Illustrative Pricing & ROI Analysis\n\n**Scope:** Pricing and unit-economics scenarios for a fictional product using documented assumptions; no real company or market data is represented.\n\n## Headline results\n\n- Base-case price / volume: **${base_row.price:.0f} / {base_row.volume:,.0f} units**.\n- Base-case break-even: **{base_row.break_even_units:,.0f} units**.\n- Base-case operating profit: **${base_row.operating_profit:,.0f}** and ROI of **{base_row.roi:.1%}**.\n- Highest modeled ROI: **{best.scenario} at {best.roi:.1%}**.\n\n## Decision readout\n\nThe base case clears break-even by **{base_row.volume - base_row.break_even_units:,.0f} units**. The price-volume matrix shows that volume scale is a material lever, but price increases improve contribution margin only when demand is assumed to hold. Pricing decisions should therefore pair the margin view with demand evidence.\n\n## Controls\n\n- Break-even returns `None` when contribution per unit is non-positive.\n- ROI returns `None` when investment is zero.\n- Scenario outputs use the same revenue, contribution, break-even, and ROI calculation path.\n\n## Limitations\n\nThis is an illustrative portfolio artifact built from synthetic assumptions. It does not estimate a demand curve, customer willingness to pay, taxes, financing, churn, retention, or competitive response.\n""")


if __name__ == "__main__":
    main()
