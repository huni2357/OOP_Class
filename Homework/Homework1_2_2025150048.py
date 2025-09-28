class PhysicalObject:
    def __init__(self, name, mass, x0=0.0, v0=0.0):
        self.name, self.mass, self.x, self.v = name, float(mass), float(x0), float(v0)
        
    def compute_force(self):
        raise NotImplementedError

    def update(self, dt):
        F = self.compute_force()
        a = F / self.mass
        self.v += a * dt         
        self.x += self.v * dt    

    def describe(self):
        return f"{self.name}: x={self.x:.6f} m, v={self.v:.6f} m/s"

class FallingObject(PhysicalObject):

    def __init__(self, name, mass, g=9.81, x0=0.0, v0=0.0):
        super().__init__(name, mass, x0, v0); self.g = float(g)

    def compute_force(self):
        return -self.mass * self.g   

class FreeObject(PhysicalObject):
    
    def compute_force(self):
        return 0.0

class SpringMass(PhysicalObject):

    def __init__(self, name, mass, k, x0=0.0, v0=0.0):
        super().__init__(name, mass, x0, v0); self.k = float(k)

    def compute_force(self):
        return -self.k * self.x


if __name__ == "__main__":

    glider = FreeObject(name="Glider", mass=1.0, x0=0.0, v0=0.0)
    ball =   FallingObject(name="Ball", mass=1.0, g=9.81, x0=0.0, v0=0.0)
    osc =    SpringMass(name="Oscillator", mass=1.0, k=10.0, x0=0.1, v0=0.0)

    # Simulate each for 3 seconds with dt=0.01 and print final states
    T = 3.0
    dt = 0.01
    steps = int(T / dt)

    for obj in (glider, ball, osc):
        for _ in range(steps):
            obj.update(dt)

    print(glider.describe())
    print(ball.describe())
    print(osc.describe())
