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
        indices = system.indices_of_first_nonzero_terms_in_each_row()
        for i,c in enumerate(indices) :
            top_index = system.topmost_index(i)
            if c != i:
                if top_index != -1:
                    system.swap_rows(i,top_index)
                   
    def topmost_index(self,idex):
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


p1 = Plane([1, 1, 1], 1)
p2 = Plane([0, 1, 1], 2)
s = LinearSystem([p1, p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2):
    print 'test case 1 failed'

p1 = Plane([1, 1, 1], 1)
p2 = Plane([1, 1, 1], 2)
s = LinearSystem([p1, p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == Plane(constant_term=1)):
    print 'test case 2 failed'

p1 = Plane([1, 1, 1], 1)
p2 = Plane([0, 1, 0], 2)
p3 = Plane([1, 1, -1], 3)
p4 = Plane([1, 0, -2], 2)
s = LinearSystem([p1, p2, p3, p4])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2 and
        t[2] == Plane([0, 0, -2], 2)
        t[3] == Plane()):
    print 'test case 3 failed'

p1 = Plane([0, 1, 1], 1)
p2 = Plane([1, -1, 1], 2)
p3 = Plane([1, 2, -5], 3)
s = LinearSystem([p1, p2, p3])
t = s.compute_triangular_form()
if not (t[0] == Plane([1, -1, 1]), 2 and
        t[1] == Plane([0, 1, 1], 1) and
        t[2] == Plane([0, 0, -9], -2):
    print 'test case 4 failed'
