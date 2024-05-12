from mpmath import polyroots


class poly:

    @staticmethod
    def x():
        return poly(0.0, 1.0)

    @staticmethod
    def zero():
        return poly(0.0)

    def __init__(self, *args):
        if len(args) == 0:
            self.coef = [0.0, ]
        elif type(args[0]) is list:
            args = list(args[0])
        elif type(args[0]) is poly:
            args = list(args[0].coef)
        if all(isinstance(c, float) for c in args):
            self.coef = list(args)
        else:
            self.coef = []
            for c in args:
                if type(c) is float:
                    self.coef.append(c)
                elif type(c) is int:
                    self.coef.append(float(c))
                else:
                    raise Exception()

    def __getitem__(self, i):
        if i < len(self.coef):
            return self.coef[i]
        return 0

    def __setitem__(self, i, v):
        # TODO: type checking
        if i < len(self.coef):
            self.coef[i] = v
        elif i > len(self.coef):
            self[i - 1] = 0
            self[i] = v
        else:
            self.coef.append(v)

    def __str__(self):
        return str(self.coef)

    def __len__(self):
        self.trim()
        return len(self.coef)

    def trim(self):
        if self.coef[-1] == 0.0 and len(self.coef) > 1:
            self.coef.pop()
            self.trim()

    def __add__(self, p2):
        pr = poly()
        for i in range(max(len(self), len(p2))):
            pr[i] = self[i] + p2[i]
        pr.trim()
        return pr

    def __sub__(self, p2):
        pr = poly()
        for i in range(max(len(self), len(p2))):
            pr[i] = self[i] - p2[i]
        pr.trim()
        return pr

    def __mul__(self, p2):
        if type(p2) is int:
            return self * poly(p2)
        pr = poly()
        for i in range(len(self)):
            for j in range(len(p2)):
                pr[i + j] += self[i] * p2[j]
        pr.trim()
        return pr

    def __eq__(self, p2):
        if type(p2) is int or type(p2) is float:
            return self[0] == p2 and len(self) == 1
        elif type(p2) is poly:
            for i in range(max(len(self), len(p2))):
                if self[i] != p2[i]:
                    return False
            return True
        else:
            raise Exception("Cannot compare type poly with type {}.".format(type(p2)))

    def eval(self, x):
        n = len(self.coef) - 1
        b = self.coef[n]
        for i in range(0, n):
            b = self.coef[n - i - 1] + b * x
        return b

    def differentiate(self):
        diff = poly()
        for n in range(1, len(self)):
            diff[n-1] = n*self[n]
        return diff

    def roots(self):
        coef = list(self.coef)
        coef.reverse()
        zeros = polyroots(coef)
        return [complex(r) for r in zeros]

    def is_zero(self):
        self.trim()
        return len(self) == 1 and self[0] == 0


