import pygame
import random
import time

# تهيئة القيم الأساسية
pygame.init()
pygame.display.set_caption("لعبة تيتريس")

# الألوان
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# متغيرات اللعبة
WIDTH, HEIGHT = 300, 600  # أبعاد نافذة اللعبة
GRID_SIZE = 30  # حجم مربع واحد في الشبكة
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 60  # عدد الإطارات في الثانية

# إنشاء النافذة
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# تعريف أشكال القطع
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]   # L
]

COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

# إنشاء صورة الشعار للبداية
def create_logo():
    logo_surface = pygame.Surface((WIDTH, HEIGHT))
    logo_surface.fill(BLACK)
    
    # رسم شعار تيتريس باستخدام مكعبات ملونة
    blocks = [
        {'color': CYAN, 'positions': [(100, 200), (130, 200), (160, 200), (190, 200)]},  # I
        {'color': YELLOW, 'positions': [(120, 240), (150, 240), (120, 270), (150, 270)]},  # O
        {'color': PURPLE, 'positions': [(100, 310), (130, 310), (160, 310), (130, 340)]},  # T
        {'color': BLUE, 'positions': [(170, 340), (200, 340), (200, 370), (230, 370)]}     # J
    ]
    
    for block in blocks:
        for pos in block['positions']:
            pygame.draw.rect(
                logo_surface,
                block['color'],
                (pos[0], pos[1], GRID_SIZE - 1, GRID_SIZE - 1)
            )
    
    # إضافة نص
    font = pygame.font.SysFont(None, 72)
    title_text = font.render("TETRIS", True, WHITE)
    logo_surface.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    
    font_small = pygame.font.SysFont(None, 30)
    start_text = font_small.render("EID FATHI...", True, WHITE)
    logo_surface.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 400))
    
    return logo_surface

class Piece:
    def __init__(self):
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_index]
        self.color = COLORS[self.shape_index]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        
    def rotate(self):
        # تدوير القطعة
        rows = len(self.shape)
        cols = len(self.shape[0])
        
        # إنشاء مصفوفة جديدة مدورة
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        for r in range(rows):
            for c in range(cols):
                rotated[c][rows - 1 - r] = self.shape[r][c]
                
        # التحقق من عدم خروج القطعة عن الحدود بعد التدوير
        old_shape = self.shape
        self.shape = rotated
        
        if self.collision(0, 0, board):
            self.shape = old_shape
            
    def collision(self, dx, dy, board):
        # التحقق من الاصطدام
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = self.x + x + dx, self.y + y + dy
                    
                    # خارج حدود اللعبة
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return True
                    
                    # الاصطدام مع القطع الأخرى
                    if new_y >= 0 and board[new_y][new_x]:
                        return True
        return False
                    
    def move(self, dx, dy, board):
        # تحريك القطعة
        if not self.collision(dx, dy, board):
            self.x += dx
            self.y += dy
            return True
        return False
    
    def draw(self):
        # رسم القطعة على الشاشة
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        (self.x * GRID_SIZE + x * GRID_SIZE,
                         self.y * GRID_SIZE + y * GRID_SIZE,
                         GRID_SIZE - 1, GRID_SIZE - 1)
                    )

# إنشاء لوحة اللعبة
board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_board():
    # رسم اللوحة والقطع الثابتة
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if board[y][x]:
                pygame.draw.rect(
                    screen,
                    board[y][x],
                    (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1)
                )

def draw_grid():
    # رسم خطوط الشبكة
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

def clear_rows():
    # إزالة الصفوف الممتلئة
    full_rows = []
    for y in range(GRID_HEIGHT):
        if all(board[y]):
            full_rows.append(y)
    
    for row in full_rows:
        del board[row]
        board.insert(0, [0 for _ in range(GRID_WIDTH)])
    
    return len(full_rows)

def game_over():
    # التحقق من انتهاء اللعبة
    return any(board[0])

def show_splash_screen():
    # عرض شاشة البداية لمدة 2 ثوان
    logo = create_logo()
    screen.blit(logo, (0, 0))
    pygame.display.flip()
    time.sleep(2)

def main():
    global board
    
    # عرض شاشة البداية
    show_splash_screen()
    
    current_piece = Piece()
    next_piece = Piece()
    score = 0
    
    # توقيت سقوط القطعة
    fall_time = 0
    fall_speed = 0.5  # ثانية
    last_fall_time = pygame.time.get_ticks()
    
    running = True
    game_ended = False
    
    while running:
        screen.fill(BLACK)
        
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - last_fall_time) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if not game_ended:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.move(-1, 0, board)
                    elif event.key == pygame.K_RIGHT:
                        current_piece.move(1, 0, board)
                    elif event.key == pygame.K_DOWN:
                        current_piece.move(0, 1, board)
                    elif event.key == pygame.K_UP:
                        current_piece.rotate()
                    elif event.key == pygame.K_SPACE:
                        # الإسقاط السريع للقطعة
                        while current_piece.move(0, 1, board):
                            pass
        
        if not game_ended:
            # سقوط القطعة تلقائيًا بمرور الوقت
            if delta_time > fall_speed:
                if not current_piece.move(0, 1, board):
                    # إذا لم تستطع الحركة للأسفل، ثبت القطعة على اللوحة
                    for y, row in enumerate(current_piece.shape):
                        for x, cell in enumerate(row):
                            if cell and 0 <= current_piece.y + y < GRID_HEIGHT:
                                board[current_piece.y + y][current_piece.x + x] = current_piece.color
                    
                    # إزالة الصفوف الممتلئة وزيادة النقاط
                    cleared = clear_rows()
                    score += cleared * 100
                    
                    # التحقق من انتهاء اللعبة
                    if game_over():
                        game_ended = True
                    else:
                        # قطعة جديدة
                        current_piece = next_piece
                        next_piece = Piece()
                
                last_fall_time = current_time
            
            # رسم العناصر
            draw_board()
            current_piece.draw()
            draw_grid()
            
            # عرض النقاط
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
        else:
            # رسالة انتهاء اللعبة
            font = pygame.font.SysFont(None, 48)
            game_over_text = font.render("Game Over ", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 24))
            
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 24))
            
            # إعادة تشغيل
            restart_font = pygame.font.SysFont(None, 36)
            restart_text = restart_font.render("Press Enter", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 70))
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                # إعادة تهيئة اللعبة
                board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                current_piece = Piece()
                next_piece = Piece()
                score = 0
                game_ended = False
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
