import pygame
import random
import math

class body:
    mass = 0.0
    radius = 0.0
    position = (0.0, 0.0)
    velocity = [0.0, 0.0]
    colour = (0, 0, 0)
    ignored = False

    def __init__(self, mass, radius, position, velocity, colour):
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.colour = colour

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.position[0]), int(self.position[1])), int(self.radius))

    def update(self, dt, x_size, y_size):
        self.position = (self.position[0] + self.velocity[0] * dt, self.position[1] + self.velocity[1] * dt)
        # Screen wrapping logic
        if self.position[0] > x_size:
            self.position = (0, self.position[1])
        elif self.position[0] < 0:
            self.position = (x_size, self.position[1])

        if self.position[1] > y_size:
            self.position = (self.position[0], 0)
        elif self.position[1] < 0:
            self.position = (self.position[0], y_size)

def attract(b1, b2, G, bodies, x_size, y_size):
    if b1.mass == 0:
        b1.ignored = True
        b1.colour = (0, 0, 0)
        b1.radius = 0
        b1.velocity = [0, 0]
        return None
    if b2.mass == 0:
        b2.ignored = True
        b2.colour = (0, 0, 0)
        b2.radius = 0
        b2.velocity = [0, 0]
        return None
    # Calculate dx, dy with screen wrapping
    dx = b2.position[0] - b1.position[0]
    dy = b2.position[1] - b1.position[1]

    # Wrap around x axis
    if abs(dx) > x_size / 2:
        if dx > 0:
            dx -= x_size
        else:
            dx += x_size

    # Wrap around y axis
    if abs(dy) > y_size / 2:
        if dy > 0:
            dy -= y_size
        else:
            dy += y_size
    distance = (dx**2 + dy**2)**0.5
    if distance < b1.radius + b2.radius and not b1.mass == 0 and not b2.mass == 0:
        b1.velocity[0] = (b1.velocity[0] * b1.mass + b2.velocity[0] * b2.mass) / (b1.mass + b2.mass)
        b1.velocity[1] = (b1.velocity[1] * b1.mass + b2.velocity[1] * b2.mass) / (b1.mass + b2.mass)
        b1.position = ((b1.position[0] * b1.mass + b2.position[0] * b2.mass) / (b1.mass + b2.mass),
                       (b1.position[1] * b1.mass + b2.position[1] * b2.mass) / (b1.mass + b2.mass))
        print(f"Collided {b1.mass} and {b2.mass} at distance {distance}")
        b1.radius = (b1.radius**3 + b2.radius**3)**(1/3)
        b1.colour = ((b1.colour[0] * b1.mass + b2.colour[0] * b2.mass) // (b1.mass + b2.mass), 
                    (b1.colour[1] * b1.mass + b2.colour[1] * b2.mass) // (b1.mass + b2.mass),
                    (b1.colour[2] * b1.mass + b2.colour[2] * b2.mass) // (b1.mass + b2.mass))
        b1.mass += b2.mass
        # Throw off debris on collision
        num_debris = random.randint(3, 6)
        lesser_mass = min(b1.mass, b2.mass)
        if not (lesser_mass == 0 or (b1.mass / b2.mass > 10 or b2.mass / b1.mass > 10)):
            for _ in range(num_debris):
                debris_mass = lesser_mass * random.uniform(0.025, 0.05)
                debris_radius = max(2, debris_mass / 100)
                angle = random.uniform(0, 2 * math.pi)
                closing_speed = (abs(b1.velocity[0]) + abs(b1.velocity[1]) + abs(b2.velocity[0]) + abs(b2.velocity[1]))
                speed = random.uniform(closing_speed / 2, 2 * closing_speed)
                debris_velocity = [
                    b1.velocity[0] + speed * math.cos(angle),
                    b1.velocity[1] + speed * math.sin(angle)
                ]
                debris_position = (
                    b1.position[0] + (b1.radius + debris_radius) * math.cos(angle),
                    b1.position[1] + (b1.radius + debris_radius) * math.sin(angle)
                )
                debris_colour = (
                    min(255, max(0, (b1.colour[0] + b2.colour[0]) // 2 + random.randint(-30, 30))),
                    min(255, max(0, (b1.colour[1] + b2.colour[1]) // 2 + random.randint(-30, 30))),
                    min(255, max(0, (b1.colour[2] + b2.colour[2]) // 2 + random.randint(-30, 30)))
                )
                bodies.append(body(debris_mass, debris_radius, debris_position, debris_velocity, debris_colour))
        b1.mass += b2.mass
        b2.mass = 0
        b2.radius = 0
        b2.velocity = [0, 0]
        b2.ignored = True
        return (0, 0)
    else:
        if not b1.ignored and not b2.ignored and not b1.mass == 0 and not b2.mass == 0:
            force = G * b1.mass * b2.mass / distance**2
            #print(f"Attracting {b1.mass} and {b2.mass} with force {force} at distance {distance}")
            b1.velocity[0] += (force * dx / distance / b1.mass)
            b1.velocity[1] += (force * dy / distance / b1.mass)
            b2.velocity[0] += (-force * dx / distance / b2.mass)
            b2.velocity[1] += (-force * dy / distance / b2.mass)
        return None

def run_sim(num_bodies, dt, min_radius, max_radius, min_mass, max_mass, min_velocity, max_velocity, G):
    pygame.init()
    x_size, y_size = pygame.display.get_desktop_sizes()[0]
    screen = pygame.display.set_mode((x_size, y_size))
    #x_size = int(x_size * 0.4)
    #y_size = int(y_size * 0.4) 
    pygame.display.set_caption("Gravitational Simulation")
    bodies = []
    for i in range(num_bodies):
        mass = random.uniform(min_mass, max_mass)
        radius = (mass/max_mass) * (max_radius - min_radius) + min_radius
        position = (random.randint(0, x_size), random.randint(0, y_size))
        velocity = [random.uniform(min_velocity, max_velocity), random.uniform(min_velocity, max_velocity)]
        colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        bodies.append(body(mass, radius, position, velocity, colour))

    clock = pygame.time.Clock() # Create a clock object
    ignoredIndices = [] # List to keep track of bodies that have been ignored after collision
    #for i in range(num_steps):
    while len(bodies) - len(ignoredIndices) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    dt *= 1.2
                if event.key == pygame.K_LEFT:
                    dt *= 0.8
                if event.key == pygame.K_PLUS:
                    G *= 1.2
                if event.key == pygame.K_MINUS:
                    G *= 0.8
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down_time = pygame.time.get_ticks()
                mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up_time = pygame.time.get_ticks()
                press_duration = (mouse_up_time - mouse_down_time) / 1000.0  # seconds
                final_mouse_pos = pygame.mouse.get_pos()
                # Calculate the distance from the initial mouse position to the final position
                distance = math.sqrt((final_mouse_pos[0] - mouse_pos[0])**2 + (final_mouse_pos[1] - mouse_pos[1])**2)
                speed = distance / press_duration if press_duration > 0 else 0
                velocity = [0.0, 0.0]
                angle = math.atan2(final_mouse_pos[1] - mouse_pos[1], final_mouse_pos[0] - mouse_pos[0])
                if speed > 0:
                    velocity = [speed * math.cos(angle), speed * math.sin(angle)]
                # Scale mass and radius with press duration, clamp to reasonable values
                mass = min(2000, max(100, 300 + press_duration * 1000))
                radius = min(50, max(5, 10 + press_duration * 10))
                colour = (255, 255, 255)
                bodies.append(body(mass, radius, final_mouse_pos, velocity, colour))

        screen.fill((0, 0, 0))

        for b in bodies:
            b.update(dt, x_size, y_size)
            b.draw(screen)

        for j in range(len(bodies)):
            for k in range(len(bodies)):
                if j != k and k not in ignoredIndices and j not in ignoredIndices:
                    ret = attract(bodies[j], bodies[k], G, bodies, x_size, y_size)
                    if ret is not None:
                        ignoredIndices.append(k)

        pygame.display.flip()
        clock.tick(60) # Limit the frame rate to 60 FPS

G = 5 # Gravitational constant
num_bodies = 10
dt = 0.01
#num_steps = 10000
min_radius = 5
max_radius = 50
min_mass = 100
max_mass = 2000
min_velocity = -500
max_velocity = 500
run_sim(num_bodies, dt, min_radius, max_radius, min_mass, max_mass, min_velocity, max_velocity, G)
pygame.quit()
