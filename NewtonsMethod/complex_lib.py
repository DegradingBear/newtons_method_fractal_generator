################################################################################
####                                                                        ####
####                        COMPLEX NUMBER LIBRARY                          ####
####                                                                        ####
################################################################################
from __future__ import annotations

class Complex():
    def __init__(self, real, imaginary):
        self._real = real
        self._im = imaginary

    def get_real(self):
        return self._real

    def get_im(self):
        return self._im

    def __repr__(self):
        return f"{round(self._real,3)} + {round(self._im,3)}i"

    def __str__(self):
        return self.__repr__()

    def __mul__(self, other)->Complex:
        real = self._real * other.get_real() - (self._im * other.get_im())
        im = self._real * other.get_im() + self._im * other.get_real()

        return Complex(real, im)

    def __add__(self, other)->Complex:
        real = self._real + other.get_real()
        im = self._im + other.get_im()

        return Complex(real, im)

    def __neg__(self)->Complex:
        return Complex(-self._real, -self._im)

    def __sub__(self, other)->Complex:
        return self + (-other)

    def copy(self)->Complex:
        """
        returns a complex number with the same real and imaginary components
        """
        return Complex(self._real, self._im)

    def __truediv__(self, other)->Complex:
        """self/other"""
        a = self._real #self is a+bi
        b = self._im
        c = other.get_real() #other is c + di
        d = other.get_im()
        divisor = (c**2 + d**2)
        real = (a*c + b*d)/divisor
        im = (b*c - a*d)/divisor

        return Complex(real, im)

    def mag(self)->float:
        return (self._real ** 2 + self._im ** 2)**0.5

    def dist(self, other)->float:
        """
        returns the "distance" from self to other
        """
        return ((self._real - other.get_real())**2 + (self._im-other.get_im()) ** 2)**0.5


class complex_polynomial():
    def __init__(self, coefficients: list[Complex]):
        """
        coefficients are the coefficients of the polynomial in increasing powers
        ie: [1+0i, 2+0i, 3+0i] will produce polynomial of (3+0i)z^2 + (2+0i)z + 1+0i
        """
        self._terms = []
        for power, coefficient in coefficients:
            self._terms.append(
                complex_term(coefficient, power)
            )

        self._derivative = None

    def eval(self, z: Complex)->Complex:
        value = Complex(0,0)
        for val in [term.eval(z) for term in self._terms]:
            value += val
        return value

    def __repr__(self)->str:
        return " + ".join(
            [
                str(term) for term in self._terms
            ]
        )

    def __str__(self)->str:
        return self.__repr__()

    def differentiate(self)->complex_polynomial:
        """
        returns the derivative polynomial of this polynomial
        """
        #ignore the first term as this was a constant that goes away when derive
        derivative_terms = [term.differentiate() for term in self._terms][1:]
        coefficients = [(term.get_pow(),term.get_coefficient()) for term in derivative_terms]

        return complex_polynomial(coefficients)

    def newtons_method(self, guess: Complex)->Complex:
        #only want to calculate derivative once if needed
        if not self._derivative:
            self._derivative = self.differentiate()

        #x_(n+1) = x_n - p(x_n)/p'(x_n)
        return guess - (self.eval(guess)/self._derivative.eval(guess))


class complex_term():
    def __init__(self, coeff: Complex, power: int):
        self._coeff = coeff
        self._pow = power

    def eval(self, z: Complex)->Complex:
        """
        evaluates the value of this term at the given z value
        """

        if self._pow == 0:
            return self._coeff

        value = z.copy()
        for i in range(self._pow-1):
            value *= z

        value *= self._coeff
        return value

    def __repr__(self)->str:
        return f"({str(roundself._coeff)})z^{self._pow}"

    def __str__(self)->str:
        return self.__repr__()

    def differentiate(self)->complex_term:
        """
        returns the derivative of this term
        """
        coefficient = self._coeff * Complex(self._pow, 0)
        power = self._pow - 1
        if power < 0: #this was just a constant
            return None

        return complex_term(coefficient, power)

    def get_coefficient(self)->Complex:
        return self._coeff.copy()
    def get_pow(self)->int:
        return self._pow


if __name__ == "__main__":
    f = complex_polynomial(
        [
            Complex(1,0),
            Complex(0,4),
            Complex(1,9)
        ] #y = x^2
    )
    guess = Complex(3,12)
    for i in range(30):
        guess = f.newtons_method(guess)
        print(f"{guess} | {f.eval(guess)}")