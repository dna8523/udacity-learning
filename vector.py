import math


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

    def plus(self, v):
        new_coordinates = [x + y for x,
                           y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def subtract(self, v):
        new_coordinates = [x - y for x,
                           y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def scalar_multiply(self, c):
        new_coordinates = [c * x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        sums = 0
        for x in self.coordinates:
            sums += x**2
        return math.sqrt(sums)

    def normalize(self):
        new_coordinates = []
        for x in self.coordinates:
            new_coordinates.append((1. / self.magnitude()) * x)
        return Vector(new_coordinates)

    def dot_product(self, v):
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    def angle(self, v):
        if self.magnitude() == 0 or v.magnitude() == 0:
            raise ValueError('zero vector detected')
        result = math.acos(self.dot_product(
            v) / (self.magnitude() * v.magnitude()))
        return result, math.degrees(result)

    def project(self, basis):
        u = basis.normalize()
        t = self.dot_product(u)
        return u.scalar_multiply(t)

    def orthognal(self, basis):
        parallel = self.project(basis)
        return v.subtract(parallel)

    def crossproduct(self, v):
        new_coordinates = []
        new_coordinates.append(
            self.coordinates[1] * v.coordinates[2] - self.coordinates[2] * v.coordinates[1])
        new_coordinates.append(
            -(self.coordinates[0] * v.coordinates[2] - self.coordinates[2] * v.coordinates[0]))
        new_coordinates.append(
            self.coordinates[0] * v.coordinates[1] - self.coordinates[1] * v.coordinates[0])
        return Vector(new_coordinates)

    def area_parallel(self, v):
        height = self.orthognal(v)
        return height.magnitude() * v.magnitude(), 'triangle = ', height.magnitude() * v.magnitude() / 2


v = Vector([1.5, 9.547, 3.691])
b = Vector([-6.007, 0.124, 5.772])
print v.area_parallel(b)
