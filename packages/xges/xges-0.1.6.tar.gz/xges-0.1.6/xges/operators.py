def _set(s):
    return "{}" if len(s) == 0 else str(s)


class Insert:
    def __init__(self, x, y, T, score, effective_parents):
        self.x = x
        self.y = y
        self.T = T
        self.score = score
        self.effective_parents = effective_parents

    def __lt__(self, other):
        return self.score < other.score

    def __str__(self):
        return (
            f"Insert: "
            f"{self.x} → {self.y}, "
            f"T = {_set(self.T)}, "
            f"score = {self.score}, "
            f"effective_parents = {_set(self.effective_parents)}"
        )

    def __repr__(self):
        return str(self)


class Delete:
    def __init__(self, x, y, C, score, effective_parents, directed):
        self.x = x
        self.y = y
        self.C = C
        self.score = score
        self.effective_parents = effective_parents
        self.directed = directed

    def __lt__(self, other):
        return self.score < other.score

    def __str__(self):
        return (
            f"Delete: "
            f"{self.x} {'→' if self.directed else '-'} {self.y}, "
            f"C = {_set(self.C)}, "
            f"score = {self.score}, "
            f"effective_parents = {_set(self.effective_parents)}"
        )

    def __repr__(self):
        return str(self)


class Reverse:
    def __init__(self, insert, score, parents_x):
        self.insert = insert
        self.score = score
        self.parents_x = parents_x

    def __lt__(self, other):
        return self.score < other.score

    def __str__(self):
        return (
            f"Reverse: "
            f"{self.insert.x} ← {self.insert.y}, "
            f"T = {_set(self.insert.T)}, "
            f"score = {self.score}, "
            f"effective_parents = {_set(self.insert.effective_parents)}"
        )

    def __repr__(self):
        return str(self)
