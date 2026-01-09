# cqql/weighting.py
# -------------------------------------------------
# Expand CQQL weighted operators into plain Boolean formulas:
#   WAND(theta1,theta2, φ1, φ2) -> (φ1 OR !theta1) AND (φ2 OR !theta2)
#   WOR(theta1,theta2, φ1, φ2)  -> (φ1 AND theta1) OR (φ2 AND theta2)
# -------------------------------------------------

from cqql.ast import (
    Formula, Atom, Not, And, Or, WeightedAnd, WeightedOr
)


def expand_weights(f: Formula) -> Formula:
    """
    Recursively eliminate WeightedAnd / WeightedOr nodes by replacing them
    with the corresponding plain Boolean formula.
    """
    # Atom
    if isinstance(f, Atom):
        return f

    # Not
    if isinstance(f, Not):
        return Not(expand_weights(f.sub))

    # And / Or
    if isinstance(f, And):
        return And(expand_weights(f.left), expand_weights(f.right))

    if isinstance(f, Or):
        return Or(expand_weights(f.left), expand_weights(f.right))

    # Weighted AND
    if isinstance(f, WeightedAnd):
        left = expand_weights(f.left)
        right = expand_weights(f.right)
        theta1 = Atom(f.theta1)
        theta2 = Atom(f.theta2)
        # (φ1 ∨ ¬θ1) ∧ (φ2 ∨ ¬θ2)
        return And(
            Or(left, Not(theta1)),
            Or(right, Not(theta2))
        )

    # Weighted OR
    if isinstance(f, WeightedOr):
        left = expand_weights(f.left)
        right = expand_weights(f.right)
        theta1 = Atom(f.theta1)
        theta2 = Atom(f.theta2)
        # (φ1 ∧ θ1) ∨ (φ2 ∧ θ2)
        return Or(
            And(left, theta1),
            And(right, theta2)
        )

    raise TypeError(f"Unknown Formula node type: {type(f)}")
