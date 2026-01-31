from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Callable
from cqql.ast import Formula, Atom, Not, And, Or


@dataclass(frozen=True)
class EvalConfig:
    get_attr: Callable[[str], str]
    attr_type: Dict[str, str]


def clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def force_db_value(x: float) -> float:
    return 1.0 if x >= 0.5 else 0.0


def atom_value(atom_name: str, scores: Dict[str, float], cfg: EvalConfig) -> float:
    raw = float(scores.get(atom_name, 0.0))
    raw = clamp01(raw)

    attr = cfg.get_attr(atom_name)
    t = cfg.attr_type.get(attr, "prox")

    if t == "db":
        return force_db_value(raw)
    return raw


def evaluate(f: Formula, scores: Dict[str, float], cfg: EvalConfig) -> float:

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
