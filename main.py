import pygame
import math
import random

class body:
    mass = 0.0
    radius = 0.0
    position = (0.0, 0.0)
    velocity = (0.0, 0.0)
    color = (0, 0, 0)

    def __init__(self, mass, radius, position, velocity, color):
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), int(self.radius))

    def update(self, dt):
        self.position = (self.position[0] + self.velocity[0] * dt, self.position[1] + self.velocity[1] * dt)

def attract(b1, b2):
    G = 6.67430e-11  # Gravitational constant
    dx = b2.position[0] - b1.position[0]
    dy = b2.position[1] - b1.position[1]
    distance = (dx**2 + dy**2)**0.5
    if distance == 0:
        return (0, 0)
    force = G * b1.mass * b2.mass / distance**2
    b1.velocity += (force * dx / distance / b1.mass, force * dy / distance / b1.mass)
    b2.velocity += (-force * dx / distance / b2.mass, -force * dy / distance / b2.mass)

def run_sim(num_bodies, x_size, y_size, dt, num_steps, min_radius, max_radius, min_mass, max_mass, min_velocity, max_velocity):
    pygame.init()
    screen = pygame.display.set_mode((x_size, y_size))
    pygame.display.set_caption("Gravitational Simulation")
    bodies = []
    for i in range(num_bodies):
        mass = random.uniform(min_mass, max_mass)
        radius = random.uniform(min_radius, max_radius)
        position = (random.uniform(0, x_size), random.uniform(0, y_size))
        velocity = (random.uniform(min_velocity, max_velocity), random.uniform(min_velocity, max_velocity))
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        bodies.append(body(mass, radius, position, velocity, color))

    for i in range(num_steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))
        for b in bodies:
            b.update(dt)
            b.draw(screen)

        for j in range(len(bodies)):
            for k in range(j + 1, len(bodies)):
                attract(bodies[j], bodies[k])

        pygame.display.flip()
        pygame.time.delay(int(dt * 1000))

num_bodies = 10
x_size = 1024
y_size = 1024
dt = 0.01
num_steps = 1000
min_radius = 5
max_radius = 20
min_mass = 1e10
max_mass = 1e12
min_velocity = -10
max_velocity = 10
run_sim(num_bodies, x_size, y_size, dt, num_steps, min_radius, max_radius, min_mass, max_mass, min_velocity, max_velocity)
pygame.quit()
