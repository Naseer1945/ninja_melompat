import pygame
import sys
import random

# --- Inisialisasi Pygame ---
pygame.init()

# --- Pengaturan Konstanta ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ninja Melompat") 

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
RED = (200, 0, 0) 

# Kecepatan Game
GAME_SPEED = 10
CLOCK = pygame.time.Clock()

# --- Konstanta Aset & Hitbox ---
NINJA_FINAL_SIZE = 100 
HITBOX_WIDTH = 50  
HITBOX_HEIGHT = 70 

# --- Pemuatan Aset (Menggunakan Dua File Terpisah) ---
try:
    # 1. Memuat Frame 1 dan Frame 2 secara terpisah
    frame_1_img = pygame.image.load('aset/ninja_jalan_1.png').convert_alpha()
    frame_2_img = pygame.image.load('aset/ninja_jalan_2.png').convert_alpha()
    
    # 2. Skalakan kedua frame ke ukuran tampilan (100x100)
    frame_1_scaled = pygame.transform.scale(frame_1_img, (NINJA_FINAL_SIZE, NINJA_FINAL_SIZE))
    frame_2_scaled = pygame.transform.scale(frame_2_img, (NINJA_FINAL_SIZE, NINJA_FINAL_SIZE))

    # 3. Kumpulkan ke dalam list animasi
    NINJA_RUN_IMAGES = [frame_1_scaled, frame_2_scaled]
    
    # 4. Memuat Kayu Tajam
    OBSTACLE_IMAGE = pygame.image.load('aset/balok_kayu_tajam.png').convert_alpha()
    OBSTACLE_IMAGE = pygame.transform.scale(OBSTACLE_IMAGE, (80, 120)) 
    
except Exception as e:
    print(f"Error fatal saat memuat aset: {e}")
    print("PASTIKAN Anda memiliki 3 file ini di folder 'aset':")
    print("1. 'ninja_jalan_1.png'")
    print("2. 'ninja_jalan_2.png'")
    print("3. 'balok_kayu_tajam.png'")
    sys.exit()

# Ukuran Dasar
GROUND_HEIGHT = 20
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT

# --- Kelas Ninja ---
class Ninja:
    def __init__(self):
        self.images = NINJA_RUN_IMAGES 
        self.image_index = 0
        self.animation_counter = 0
        self.image = self.images[self.image_index]
        
        # Hitbox yang lebih kecil (50x70)
        self.rect = pygame.Rect(50, 0, HITBOX_WIDTH, HITBOX_HEIGHT)
        self.rect.bottom = GROUND_Y 
        self.rect.x = 50 
        
        self.y_start = self.rect.y 
        self.is_jumping = False
        self.jump_velocity = 18 
        self.gravity = 1

    def update(self):
        # LOGIKA LOMPATAN
        if self.is_jumping:
            self.rect.y -= self.jump_velocity
            self.jump_velocity -= self.gravity
            
            if self.rect.y >= self.y_start:
                self.rect.bottom = GROUND_Y 
                self.is_jumping = False
                self.jump_velocity = 0
        
        # LOGIKA ANIMASI BERJALAN 
        if not self.is_jumping:
            self.animation_counter += 1
            if self.animation_counter >= 8: # Ganti frame setiap 8 tick
                self.animation_counter = 0
                self.image_index = (self.image_index + 1) % len(self.images) 
                self.image = self.images[self.image_index]

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = 18
            self.image = self.images[0] 

    def draw(self, screen):
        # Menggambar gambar 100x100 di atas hitbox 50x70
        image_x = self.rect.x - (NINJA_FINAL_SIZE - self.rect.width) // 2 
        image_y = self.rect.y - (NINJA_FINAL_SIZE - self.rect.height)
        
        screen.blit(self.image, (image_x, image_y))
        
        # # DEBUG: Aktifkan untuk melihat kotak tabrakan merah
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)

# --- Kelas Kayu ---
class KayuTajam:
    def __init__(self):
        self.image = OBSTACLE_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = GROUND_Y - self.rect.height
        self.speed = GAME_SPEED

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# --- Fungsi Utama Game ---
def game_loop():
    player = Ninja()
    obstacles = []
    score = 0
    running = True
    
    SPAWN_OBSTACLE = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_OBSTACLE, random.randint(1500, 3000)) 
    
    # --- Konstanta Waktu ---
    WARNING_TIME_MS = 20000  
    POPUP_DURATION_MS = 3000   
    
    start_time = pygame.time.get_ticks() 
    warning_triggered = False            
    popup_show_time = 0                  

    while running:
        current_time = pygame.time.get_ticks()

        # --- 1. Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
            
            if event.type == SPAWN_OBSTACLE:
                pygame.time.set_timer(SPAWN_OBSTACLE, random.randint(1500, 3000)) 
                obstacles.append(KayuTajam())

        # --- 2. Update Objek ---
        player.update()
        
        for obstacle in obstacles:
            obstacle.update()
            if obstacle.rect.right < 0:
                obstacles.remove(obstacle)
                score += 1

        # --- 3. Deteksi Tabrakan & Logika Peringatan ---
        for obstacle in obstacles:
            if player.rect.colliderect(obstacle.rect):
                print(f"Game Over! Ninja menabrak Kayu Tajam! Skor Akhir: {score}")
                running = False
        
        elapsed_time = current_time - start_time
        if elapsed_time >= WARNING_TIME_MS and not warning_triggered:
            warning_triggered = True
            popup_show_time = current_time 

        # --- 4. Drawing (Menggambar) ---
        SCREEN.fill(WHITE) 
        pygame.draw.rect(SCREEN, GREEN, (0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT))

        player.draw(SCREEN)

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            
        # Tampilkan Skor (Font Size 36)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Skor: {score}", True, BLACK)
        SCREEN.blit(text, (SCREEN_WIDTH - 150, 10))
        
        # --- Drawing Pop-up Peringatan (Tengah Atas) ---
        if warning_triggered and (current_time - popup_show_time) < POPUP_DURATION_MS:
            warning_font = pygame.font.Font(None, 36) 
            warning_text = "ANDA BERMAIN TERLALU LAMA!" 
            text_surface = warning_font.render(warning_text, True, RED)
            
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 10 + text_surface.get_height() // 2))
            
            SCREEN.blit(text_surface, text_rect)
        # -----------------------------------------------------------------

        # Update Tampilan
        pygame.display.flip()

        # Atur FPS
        CLOCK.tick(60)

# --- Mulai Game ---
if __name__ == "__main__":
    game_loop()