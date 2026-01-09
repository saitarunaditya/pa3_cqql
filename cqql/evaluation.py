# cqql/evaluation.py
# -------------------------------------------------
# CQQL Evaluation
#
# Assumption for this implementation:
#   - We evaluate only after normalization removed ordinal overlaps.
#   - Then standard fuzzy semantics apply:
#       NOT: 1 - x
#       AND: x * y
#       OR : x + y - x*y
#
# Atom scoring:
#   - DB attributes: forced to {0,1}
#   - text/prox attributes: in [0,1]
# -------------------------------------------------

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Callable

from cqql.ast import Formula, Atom, Not, And, Or


@dataclass(frozen=True)
class EvalConfig:
    # atom name -> attribute name
    get_attr: Callable[[str], str]
    # attribute name -> type in {"db","text","prox"}
    attr_type: Dict[str, str]


def clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def force_db_value(x: float) -> float:
    # robust: treat anything >= 0.5 as True
    return 1.0 if x >= 0.5 else 0.0


def atom_value(atom_name: str, scores: Dict[str, float], cfg: EvalConfig) -> float:
    """
    Fetch value for atom from object score map, then apply DB/text/prox policy.
    If atom not found: default 0 (safe).
    """
    raw = float(scores.get(atom_name, 0.0))
    raw = clamp01(raw)

    attr = cfg.get_attr(atom_name)
    t = cfg.attr_type.get(attr, "prox")  # default to prox-like if unknown

    if t == "db":
        return force_db_value(raw)
    return raw


def evaluate(f: Formula, scores: Dict[str, float], cfg: EvalConfig) -> float:
    """
    Evaluate CQQL formula on a single object.
    Returns a score in [0,1].
    """
    if isinstance(f, Atom):
        if f.name == "TRUE":
            return 1.0
        if f.name == "FALSE":
            return 0.0
        return atom_value(f.name, scores, cfg)

    if isinstance(f, Not):
        return 1.0 - evaluate(f.sub, scores, cfg)

    if isinstance(f, And):
        a = evaluate(f.left, scores, cfg)
        b = evaluate(f.right, scores, cfg)
        return a * b

    if isinstance(f, Or):
        a = evaluate(f.left, scores, cfg)
        b = evaluate(f.right, scores, cfg)
        return a + b - (a * b)

    raise TypeError(f"Unsupported formula node for evaluation: {type(f)}")
