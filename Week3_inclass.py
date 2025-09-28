#######################
# in-class exercise 1 #
#######################
import math
from abc import ABC, abstractmethod

class Shape3D(ABC):
    
    @abstractmethod
    def volume(self):
        pass

    @abstractmethod
    def surface_area(self):
        pass

    def describe(self):
        return f"This is a 3D shape of type {self.__class__.__name__}."

class Cube(Shape3D):
    def __init__(self,side):
        self.side = side

    def volume(self):
        return self.side**3

    def surface_area(self):
        return (self.side**2)*6

class Sphere(Shape3D):
    def __init__(self,radius):
        self.radius = radius

    def volume(self):
        return self.radius**3*4/3*math.pi

    def surface_area(self):
        return (self.radius**2)*4*math.pi


class Cylinder(Shape3D):
    def __init__(self,radius,height):
        self.radius = radius
        self.height = height

    def volume(self):
        return self.height*(self.radius**2)*math.pi

    def surface_area(self):
        return (self.height + self.radius) * self.radius *math.pi *2

shapes = [
    Cube(2),
    Sphere(3),
    Cylinder(2, 5)
]

for shape in shapes:
    print(shape.describe())
    print("Volume:", shape.volume())
    print("Surface Area:", shape.surface_area())
    print()
#######################
# in-class exercise 2 #
#######################
class A:
    def hello(self):
        print("Hello from A")

class B(A):
    def hello(self):
        print("Hello from B")
        super().hello()
class C(A):
    def hello(self):
        print("Hello from C")
        super().hello()

class D(B, C):
    def hello(self):
        print("Hello from D")
        super().hello()

class E(C):
    def hello(self):
        print("Hello from E")
        super().hello()


class F(B,E):
    def hello(self):
        print("Hello from F")
        super().hello()
 
f = F()
f.hello()
print(F.mro())
# result [<class '__main__.F'>, <class '__main__.B'>, <class '__main__.E'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
# --> F-B-E-C-A-object

# example of conflict error
class X: pass
class Y: pass
class Z(X,Y): pass
class W(Y,X): pass
class P(Z,W): pass
# Z: Z - X - Y - object / W: W - Y - X - object
# P -> 순서가 다름.... 






















        
