from math import *

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self,v):
        new_coordinates = [x + y for x,y in zip(self.coordinates,v.coordinates)]
        return Vector(new_coordinates)

    def subtract(self,v):
        new_coordinates = [x-y for x,y in zip(self.coordinates,v.coordinates)]
        return Vector(new_coordinates)

    def scalar_multiply(self,c):
        new_coordinates = [c * x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        sums = 0
        for x in self.coordinates:
            sums += x**2
        return sqrt(sums)

    def normalize(self):
        new_coordinates = []
        for x in self.coordinates:
            new_coordinates.append((1. / self.magnitude()) * x)
        return Vector(new_coordinates)

    def dot_product(self,v):
        return sum([x*y for x,y in zip(self.coordinates,v.coordinates)])

    def angle(self,v):
        if self.magnitude() == 0 or v.magnitude() == 0:
            raise ValueError('zero vector detected')
        result = acos(self.dot_product(v)/(self.magnitude()*v.magnitude()))
        return result

    def is_parallel(self,v):
        return self.is_zero() or v.is_zero() or self.angle(v) == pi or self.angle(v) == 0

    def is_zero(self):
        for i in self.coordinates:
            if i != 0:
                return False
        return True



