from cqql.ast import (
    Formula, Atom, Not, And, Or, WeightedAnd, WeightedOr
)


def expand_weights(f: Formula) -> Formula:

    if isinstance(f, Atom):
        return f

    if isinstance(f, Not):
        return Not(expand_weights(f.sub))

    if isinstance(f, And):
        return And(expand_weights(f.left), expand_weights(f.right))

    if isinstance(f, Or):
        return Or(expand_weights(f.left), expand_weights(f.right))

    if isinstance(f, WeightedAnd):
        left = expand_weights(f.left)
        right = expand_weights(f.right)
        theta1 = Atom(f.theta1)
        theta2 = Atom(f.theta2)

        return And(
            Or(left, Not(theta1)),
            Or(right, Not(theta2))
        )

    if isinstance(f, WeightedOr):
        left = expand_weights(f.left)
        right = expand_weights(f.right)
        theta1 = Atom(f.theta1)
        theta2 = Atom(f.theta2)

        return Or(
            And(left, theta1),
            And(right, theta2)
        )

    raise TypeError(f"Unknown Formula node type: {type(f)}")
