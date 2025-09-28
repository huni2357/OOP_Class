
#inclass exercise_1

class Vector:
    def __init__(self, x, y):
        self.x, self.y = x,y

    def __add__(self,other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self,other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self,other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False
        
    def __str__(self):
        return f"({self.x}, {self.y})"


v1 = Vector(1,2)
v2 = Vector(3,4)

print(v1 + v2)
print(v1 - v2)
print(v1 == v2)

#in class exercise_2

class Temperature:
    unit = "Celsius"
    
    def __init__(self,value):
        self.value = value

    def display(self):
        print(f"{self.value},{self.unit}")

    @classmethod
    def change_unit(cls,new_unit):
        cls.unit = new_unit

    @staticmethod
    def to_fahrenheit(celsius):
        return (celsius * 9/5) + 32

    
t = Temperature(30)
t.display()

Temperature.change_unit('Kelvin')
t.display()

print(Temperature.to_fahrenheit(30))
