import pygame
import sys
import random

# --- Inisialisasi & Konstanta ---
pygame.init()
SCREEN = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Ninja Melompat") 
CLOCK = pygame.time.Clock()
FONT = pygame.font.Font(None, 36) # Buat satu kali di sini

# Warna & Pengaturan
WHITE, BLACK, RED, GREEN = (255, 255, 255), (0, 0, 0), (200, 0, 0), (0, 150, 0)
GAME_SPEED = 10
GROUND_Y = 380

# --- Pemuatan Aset ---
def load_img(path, size):
    return pygame.transform.scale(pygame.image.load(f'aset/{path}').convert_alpha(), size)

NINJA_FRAMES = [load_img('ninja_jalan_1.png', (100, 100)), load_img('ninja_jalan_2.png', (100, 100))]
OBSTACLE_IMG = load_img('balok_kayu_tajam.png', (80, 120))

class Ninja:
    def __init__(self):
        self.image_index = 0
        self.anim_timer = 0
        self.rect = pygame.Rect(50, GROUND_Y - 70, 50, 70) # Hitbox langsung
        self.jump_vel = 0
        self.is_jumping = False

    def update(self):
        # Gravitasi & Lompat
        if self.is_jumping:
            self.rect.y -= self.jump_vel
            self.jump_vel -= 1
            if self.rect.bottom >= GROUND_Y:
                self.rect.bottom = GROUND_Y
                self.is_jumping = False
        else:
            # Animasi lari
            self.anim_timer += 1
            if self.anim_timer >= 8:
                self.anim_timer = 0
                self.image_index = (self.image_index + 1) % 2

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_vel = 18

    def draw(self, screen):
        # Gambar karakter di tengah hitbox
        screen.blit(NINJA_FRAMES[self.image_index], (self.rect.x - 25, self.rect.y - 30))

class Kayu:
    def __init__(self):
        self.rect = OBSTACLE_IMG.get_rect(midbottom=(850, GROUND_Y))

    def update(self):
        self.rect.x -= GAME_SPEED

def game_loop():
    player = Ninja()
    obstacles = []
    score = 0
    start_time = pygame.time.get_ticks()
    
    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_UP]: player.jump()
            if event.type == pygame.USEREVENT + 1: obstacles.append(Kayu())

        # Update
        player.update()
        for obs in obstacles[:]:
            obs.update()
            if obs.rect.right < 0: obstacles.remove(obs); score += 1
            if player.rect.colliderect(obs.rect): return # Game Over

        # Draw
        SCREEN.fill(WHITE)
        pygame.draw.rect(SCREEN, GREEN, (0, GROUND_Y, 800, 20))
        player.draw(SCREEN)
        for obs in obstacles: SCREEN.blit(OBSTACLE_IMG, obs.rect)
        
        # Skor & Peringatan
        SCREEN.blit(FONT.render(f"Skor: {score}", True, BLACK), (650, 10))
        
        curr_time = pygame.time.get_ticks()
        if 20000 < (curr_time - start_time) < 23000:
            warn = FONT.render("ANDA BERMAIN TERLALU LAMA!", True, RED)
            SCREEN.blit(warn, (400 - warn.get_width()//2, 20))

        pygame.display.flip()
        CLOCK.tick(60)

if __name__ == "__main__":
    game_loop()
