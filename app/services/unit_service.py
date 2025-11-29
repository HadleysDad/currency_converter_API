from typing import Dict

# simple unit conversion table (length and mass examples). Extend as desired.
LENGTH: Dict[str, float] = {
    "m": 1.0,
    "cm": 0.01,
    "mm": 0.001,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
}

MASS: Dict[str, float] = {
    "kg": 1.0,
    "g": 0.001,
    "mg": 0.000001,
    "lb": 0.45359237,
    "oz": 0.0283495231,
}

def convert_unit(value: float, from_unit: str, to_unit: str) -> float:
    f = from_unit.lower()
    t = to_unit.lower()

    # detect which dimension: length or mass
    if f in LENGTH and t in LENGTH:
        base = LENGTH
    elif f in MASS and t in MASS:
        base = MASS
    else:
        raise ValueError(f"Unsupported or mismatched units: {from_unit} -> {to_unit}")

    # convert to base (meters or kg) then to target
    base_value = value * base[f]
    result = base_value / base[t]
    return result
