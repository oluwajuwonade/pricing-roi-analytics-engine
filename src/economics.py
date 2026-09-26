from __future__ import annotations

def break_even_units(fixed_cost: float, price: float, variable_cost: float) -> float | None:
    contribution = price - variable_cost
    if contribution <= 0:
        return None
    return fixed_cost / contribution

def roi(gain: float, investment: float) -> float | None:
    if investment == 0:
        return None
    return (gain - investment) / investment
