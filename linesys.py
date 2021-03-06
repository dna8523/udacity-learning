from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def swap_rows(self, row1, row2):
        t = self.planes[row1]
        self.planes[row1] = self.planes[row2]
        self.planes[row2] = t

    def multiply_coefficient_and_row(self, coefficient, row):
        t, c = self.planes[row].normal_vector, self.planes[row].constant_term
        for i in range(len(t)):
            self.planes[row].normal_vector[i] = coefficient * t[i]
        self.planes[row].constant_term = coefficient * c

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        t, c = self.planes[row_to_add].normal_vector, self.planes[row_to_add].constant_term
        t1, c1 = self.planes[row_to_be_added_to].normal_vector, self.planes[row_to_be_added_to].constant_term
        for i in range(len(t)):
            t1[i] += t[i] * coefficient
        c1 += c * coefficient
        self.planes[row_to_be_added_to] = Plane(t1, c1)

    def compute_triangular_form(self):
        system = deepcopy(self)
        if len(self) > self.dimension:
            for i in range(self.dimension, len(self)):
                system[i] = Plane()
        indices = system.indices_of_first_nonzero_terms_in_each_row()
        for i, c in enumerate(indices):
            top_index = system.topmost_index(i)
            if c != i:
                if top_index != -1:
                    system.swap_rows(i, top_index)
                else:
                    if c < i and c != -1:
                        for t in range(i - c):
                            if system[system.topmost_index(c + t)].normal_vector[c + t] != 0:
                                row_to_multiply = system.topmost_index(c + t)
                                coefficient = system[i].normal_vector[c + t] / \
                                    system[row_to_multiply].normal_vector[c +
                                                                          t] * (-1)
                                system.add_multiple_times_row_to_row(
                                    coefficient, row_to_multiply, i)
        return system

    def compute_rref(self):
        r = self.compute_triangular_form()
        indices = r.indices_of_first_nonzero_terms_in_each_row()
        for row in range(len(r)):
            for col in range(r.dimension):
                if col != indices[row] and col < len(r) and r[col].normal_vector[col] != 0:
                    coefficient = float(r[row].normal_vector[col]) / \
                        r[col].normal_vector[col] * (-1)
                    r.add_multiple_times_row_to_row(coefficient, col, row)
                if col == indices[row] and r[row].normal_vector[col] != 1:
                    r.multiply_coefficient_and_row(
                        1. / r[row].normal_vector[col], row)
        return r

    def output(self):
        r = self.compute_rref()
        indices = self.indices_of_first_nonzero_terms_in_each_row()
        
        return r

    def topmost_index(self, idex):
        indices = self.indices_of_first_nonzero_terms_in_each_row()
        result = -1
        for i, c in enumerate(indices):
            if c == idex:
                result = i
                break
        return result

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i, p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices

    def __len__(self):
        return len(self.planes)

    def __getitem__(self, i):
        return self.planes[i]

    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i + 1, p)
                for i, p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


p1 = Plane([0.786, 0.786, 0.588], -0.714)
p2 = Plane([-0.138, -0.138, 0.244], 0.319)
s = LinearSystem([p1, p2])
print s.output()

p1 = Plane([8.631, 5.112, -1.816], -5.113)
p2 = Plane([4.315, 11.132, -5.27], -6.775)
p3 = Plane([-2.158, 3.01, -1.727], -0.831)
s = LinearSystem([p1, p2])
print s.output()

p1 = Plane([0.935, 1.76, -9.365], -9.955)
p2 = Plane([0.187, 0.352, -1.873], -1.991)
p3 = Plane([0.374, 0.704, -3.746], -3.982)
p4 = Plane([-0.561, -1.056, 5.619], 5.973)
s = LinearSystem([p1, p2, p3, p4])
print s.output()
