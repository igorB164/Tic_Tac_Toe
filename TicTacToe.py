import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 300, 350
LINE_WIDTH = 5
BOARD_SIZE = 3
CELL_SIZE = WIDTH // BOARD_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 40)
PADDING = 10
SYMBOL_OFFSET = 20
BTN_HEIGHT = 50

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-нолики")

# Игровые переменные
board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
current_player = "X"
game_over = False
scores = {"X": 0, "O": 0}
winner_text = ""

def draw_grid():
    """Отрисовка игрового поля"""
    screen.fill(WHITE)
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), 
                        (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), 
                        (i * CELL_SIZE, HEIGHT - BTN_HEIGHT), LINE_WIDTH)

def draw_winning_line(start_pos, end_pos):
    """Отрисовка линии победителя"""
    pygame.draw.line(screen, RED, start_pos, end_pos, LINE_WIDTH)

def check_winner():
    """Проверка победной комбинации или ничьи"""
    global game_over, winner_text

    # Проверка строк и столбцов
    for i in range(BOARD_SIZE):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            draw_winning_line((0, i * CELL_SIZE + CELL_SIZE // 2),
                            (WIDTH, i * CELL_SIZE + CELL_SIZE // 2))
            declare_winner(board[i][0])
            return
        
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            draw_winning_line((i * CELL_SIZE + CELL_SIZE // 2, 0),
                            (i * CELL_SIZE + CELL_SIZE // 2, HEIGHT - BTN_HEIGHT))
            declare_winner(board[0][i])
            return

    # Проверка диагоналей
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        draw_winning_line((0, 0), (WIDTH, HEIGHT - BTN_HEIGHT))
        declare_winner(board[0][0])
        return
        
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        draw_winning_line((WIDTH, 0), (0, HEIGHT - BTN_HEIGHT))
        declare_winner(board[0][2])
        return

    # Проверка на ничью
    if all(all(cell is not None for cell in row) for row in board):
        game_over = True
        winner_text = "Ничья!"

def declare_winner(player):
    """Объявление победителя и обновление счета"""
    global game_over, winner_text
    game_over = True
    winner_text = f"Победил {player}!"
    scores[player] += 1

def reset_game():
    """Сброс игры для новой партии"""
    global board, game_over, current_player, winner_text
    board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    game_over = False
    winner_text = ""
    current_player = "X"

def draw_symbols():
    """Отрисовка крестиков и ноликов на поле"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == "X":
                pygame.draw.line(screen, BLACK, 
                                (col * CELL_SIZE + SYMBOL_OFFSET, row * CELL_SIZE + SYMBOL_OFFSET),
                                ((col + 1) * CELL_SIZE - SYMBOL_OFFSET, (row + 1) * CELL_SIZE - SYMBOL_OFFSET), 
                                LINE_WIDTH)
                pygame.draw.line(screen, BLACK,
                                ((col + 1) * CELL_SIZE - SYMBOL_OFFSET, row * CELL_SIZE + SYMBOL_OFFSET),
                                (col * CELL_SIZE + SYMBOL_OFFSET, (row + 1) * CELL_SIZE - SYMBOL_OFFSET),
                                LINE_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, BLACK,
                                  (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                  CELL_SIZE // 2 - SYMBOL_OFFSET, LINE_WIDTH)

def draw_game_over_message():
    """Отрисовка сообщения о результате игры"""
    text_surface = FONT.render(winner_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    
    background_rect = pygame.Rect(
        text_rect.left - PADDING,
        text_rect.top - PADDING,
        text_rect.width + 2 * PADDING,
        text_rect.height + 2 * PADDING,
    )
    
    pygame.draw.rect(screen, (200, 200, 200), background_rect)
    pygame.draw.rect(screen, BLACK, background_rect, 2)
    screen.blit(text_surface, text_rect)

def draw_score():
    """Отрисовка счета"""
    score_text = FONT.render(f"X: {scores['X']}  O: {scores['O']}", True, BLACK)
    screen.blit(score_text, (10, HEIGHT - 40))

def draw_new_game_button():
    """Отрисовка кнопки новой игры"""
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - BTN_HEIGHT, WIDTH, BTN_HEIGHT))
    btn_text = FONT.render("Новая игра", True, WHITE)
    screen.blit(btn_text, (WIDTH // 2 - btn_text.get_width() // 2, HEIGHT - 40))

# Основной игровой цикл
running = True
while running:
    draw_grid()
    draw_score()
    draw_new_game_button()
    draw_symbols()

    if game_over:
        draw_game_over_message()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if HEIGHT - BTN_HEIGHT <= y <= HEIGHT:
                reset_game()
            elif not game_over:
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if board[row][col] is None:
                    board[row][col] = current_player
                    check_winner()
                    current_player = "O" if current_player == "X" else "X"

    pygame.display.flip()

pygame.quit()
sys.exit()