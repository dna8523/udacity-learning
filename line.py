from decimal import Decimal, getcontext
from math import *
from vector import Vector

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0'] * self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = 0
        self.constant_term = constant_term

        self.basepoint = self.set_basepoint()

    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = [0] * self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c / initial_coefficient
            self.basepoint = Vector(basepoint_coords)
            return self.basepoint

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i == initial_index)) + 'x_{}'.format(i + 1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    def is_parallel_line(self, line):
        n1 = Vector(self.normal_vector)
        n2 = Vector(line.normal_vector)
        return n1.is_parallel(n2)

    def __eq__(self, line):
        if not self.is_parallel_line(line):
            return False
        x0 = self.basepoint
        y0 = line.basepoint
        basepoint_difference = x0.subtract(y0)
        n = Vector(self.normal_vector)
        return basepoint_difference.is_orthognal(n)

    def intersection(self, line):
        if self.is_parallel_line(line):
            return 'None'
        a = self.normal_vector[0]
        b = self.normal_vector[1]
        c = line.normal_vector[0]
        d = line.normal_vector[1]
        k1 = self.constant_term
        k2 = line.constant_term
        x = (d * k1 - b * k2) / (a * d - b * c)
        y = (a * k2 - c * k1) / (a * d - b * c)
        return Vector([x, y])

    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


l1 = Line([1.182, 5.562], 6.744)
l2 = Line([1.773, 8.343], 9.525)
v = l1.basepoint.subtract(l2.basepoint)
n1 = Vector(l1.normal_vector)
n2 = Vector(l2.normal_vector)
print l1 == l2, l1.intersection(l2), l1.is_parallel_line(l2)
