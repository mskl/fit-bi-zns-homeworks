class TrapMF:
    """ Trapezoidal membership function """

    def __init__(self, a, b, c, d):
        """ Initialise the __/‾‾\__ function with 4 points: __a/b‾‾c\d__ """
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __getitem__(self, x) -> float:
        """ Get the function value f(x) """
        # avoid division by 0 by moving the boundaries
        if self.a == self.b:
            self.a -= 1
        if self.d == self.c:
            self.d += 1

        rise = (x - self.a) / (self.b - self.a)
        fall = (self.d - x) / (self.d - self.c)
        return max(min(rise, 1, fall), 0)
