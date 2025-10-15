import pygame, random, math, sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("❤️ Particle Heart Animation")

BACKGROUND = (255, 255, 255)  
PARTICLE_COLOR = (255, 70, 100)
SPARKLE_COLOR = (255, 200, 200)
FLOAT_HEART_COLOR = (255, 120, 150)
TEXT_COLOR = (255, 50, 50)

class Particle:
    def __init__(self, x, y):
        self.x = x + random.uniform(-4, 4)
        self.y = y + random.uniform(-4, 4)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-2, -0.5)
        self.life = random.randint(40, 70)
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05  
        self.life -= 1

    def draw(self, surface):
        alpha = max(0, min(255, int(255 * (self.life / 70))))
        color = (*PARTICLE_COLOR, alpha)
        surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (self.size, self.size), self.size)
        surface.blit(surf, (self.x - self.size, self.y - self.size))

class Sparkle:
    def __init__(self, x, y):
        self.x = x + random.uniform(-2, 2)
        self.y = y + random.uniform(-2, 2)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.life = random.randint(15, 30)
        self.size = random.randint(1, 3)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        alpha = max(0, min(255, int(255 * (self.life / 30))))
        color = (*SPARKLE_COLOR, alpha)
        surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (self.size, self.size), self.size)
        surface.blit(surf, (self.x - self.size, self.y - self.size))

class FloatingHeart:
    def __init__(self, x, y):
        self.x = x + random.uniform(-10, 10)
        self.y = y + random.uniform(-10, 10)
        self.vx = random.uniform(-0.3, 0.3)
        self.vy = random.uniform(-1, -0.3)
        self.life = random.randint(50, 100)
        self.size = random.randint(5, 10)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        alpha = max(0, min(255, int(255 * (self.life / 100))))
        surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.polygon(surf, (*FLOAT_HEART_COLOR, alpha), [
            (self.size, self.size),
            (self.size*2, self.size),
            (self.size*2, self.size*2),
            (self.size, self.size*2)
        ])
        surface.blit(surf, (self.x - self.size, self.y - self.size))

def heart_points(scale=10):
    points = []
    for t in range(0, 360, 3):
        angle = math.radians(t)
        x = 16 * math.sin(angle)**3
        y = -(13 * math.cos(angle) - 5 * math.cos(2*angle) - 2 * math.cos(3*angle) - math.cos(4*angle))
        points.append((WIDTH//2 + x * scale, HEIGHT//2 + y * scale))
    return points

points = heart_points()
particles = []
sparkles = []
floating_hearts = []

merge_phase = 0.0
phase_speed = 0.02  
show_text = False
font = pygame.font.SysFont('Arial', 64, bold=True)

running = True
start_time = pygame.time.get_ticks()
while running:
    t = pygame.time.get_ticks() - start_time
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if merge_phase < 1.0:
        merge_phase += phase_speed
        for _ in range(5):
            px, py = random.choice(points)
            spawn_y = (1 - merge_phase) * 300 + py
            particles.append(Particle(px, spawn_y))
    else:
     
        for _ in range(3):
            px, py = random.choice(points)
            sparkles.append(Sparkle(px, py))
        
        if random.random() < 0.05:  
            px, py = random.choice(points)
            floating_hearts.append(FloatingHeart(px, py))
        show_text = True

    for p in particles[:]:
        p.update()
        if p.life <= 0:
            particles.remove(p)
        else:
            p.draw(screen)

    for s in sparkles[:]:
        s.update()
        if s.life <= 0:
            sparkles.remove(s)
        else:
            s.draw(screen)

    for fh in floating_hearts[:]:
        fh.update()
        if fh.life <= 0:
            floating_hearts.remove(fh)
        else:
            fh.draw(screen)

    if merge_phase >= 1.0:
        pulse_scale = 1.0 + 0.15 * math.sin(pygame.time.get_ticks() * 0.01)
        for x, y in points:
            pygame.draw.circle(screen, PARTICLE_COLOR, (int(WIDTH//2 + (x - WIDTH//2) * pulse_scale),
                                                        int(HEIGHT//2 + (y - HEIGHT//2) * pulse_scale)), 2)

    if show_text:
        alpha = min(255, int((t - 2000) / 2))
        text_surf = font.render("LOVE", True, TEXT_COLOR)
        text_surf.set_alpha(alpha)
        rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 180))
        screen.blit(text_surf, rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
