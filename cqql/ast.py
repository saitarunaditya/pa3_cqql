class Formula:
    """Base class for all CQQL formulas."""

    def atoms(self):
        """Return the set of atomic symbols occurring in the formula."""
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return str(self)



class Atom(Formula):
    def __init__(self, name):
        self.name = name

    def atoms(self):
        return {self.name}

    def __str__(self):
        return self.name



class Not(Formula):
    def __init__(self, sub):
        self.sub = sub

    def atoms(self):
        return self.sub.atoms()

    def __str__(self):
        return f"!({self.sub})"



class And(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def atoms(self):
        return self.left.atoms().union(self.right.atoms())

    def __str__(self):
        return f"({self.left} & {self.right})"



class Or(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def atoms(self):
        return self.left.atoms().union(self.right.atoms())

    def __str__(self):
        return f"({self.left} | {self.right})"



class WeightedAnd(Formula):
    def __init__(self, theta1, theta2, left, right):
        self.theta1 = theta1
        self.theta2 = theta2
        self.left = left
        self.right = right

    def atoms(self):
        return (
            {self.theta1, self.theta2}
            .union(self.left.atoms())
            .union(self.right.atoms())
        )

    def __str__(self):
        return f"WAND({self.theta1},{self.theta2},{self.left},{self.right})"



class WeightedOr(Formula):
    def __init__(self, theta1, theta2, left, right):
        self.theta1 = theta1
        self.theta2 = theta2
        self.left = left
        self.right = right

    def atoms(self):
        return (
            {self.theta1, self.theta2}
            .union(self.left.atoms())
            .union(self.right.atoms())
        )

    def __str__(self):
        return f"WOR({self.theta1},{self.theta2},{self.left},{self.right})"
