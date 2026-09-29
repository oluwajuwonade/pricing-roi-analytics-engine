# Pricing, Unit Economics & ROI Decision Engine

> **Decision problem:** How do price, volume, cost, and customer economics change contribution, break-even, and ROI?

A decision-support engine linking pricing assumptions, unit economics, break-even analysis, ROI scenarios, and sensitivity analysis.

## Executive summary

Pricing decisions become clearer when revenue, variable cost, fixed cost, volume, contribution margin, and ROI are evaluated together.

## Decision workflow

`Price + Volume + Costs → Revenue → Contribution → Break-even → ROI → Sensitivity → Commercial decision`

## Analytical questions

1. What happens to contribution when price changes?
2. What volume is required to break even?
3. How sensitive is ROI to price, cost, and volume?
4. Which assumptions drive the largest commercial differences?

## Deliverables

- Unit-economics calculator
- Break-even engine
- Price/volume sensitivity matrix
- ROI scenarios
- Margin bridge
- Decision memo template

## Sample outputs

Run:

```bash
python src/generate_outputs.py
```

The generated outputs include:

- Scenario economics
- ROI comparison
- Base-case unit economics bridge
- Price/volume sensitivity
- Executive summary

## Data disclosure

Inputs are synthetic assumptions for a fictional product. They are **not empirical demand estimates** and should not be treated as market forecasts.

## Important limitations

- Inputs are synthetic assumptions for a fictional product.
- The model does not estimate demand elasticity or observed customer response.
- ROI and break-even outputs are scenario results conditional on the stated assumptions, not forecasts.
- Real decisions require validated costs, pricing constraints, demand evidence, and context-specific assumptions.

## Technical stack

Python · pandas · NumPy · Plotly · financial modelling concepts

## Portfolio role

**Tier 1 — Flagship Commercial Decision Analytics**

The project demonstrates practical business reasoning around pricing, unit economics, break-even, ROI, and sensitivity analysis.

## Related projects

- [Financial Planning & Scenario Modelling](https://github.com/oluwajuwonade/financial-modelling-starter-system)
- [AI-Powered Retail Sales Diagnostic](https://github.com/oluwajuwonade/AI-Powered-Retail-Sales-Diagnostic)
- [Business Metrics & KPI Engine](https://github.com/oluwajuwonade/business-kpi-calculator)

## Author

**Oluwajuwon Adediji**  
Data & Quantitative Analyst | Commercial & Decision Analytics
