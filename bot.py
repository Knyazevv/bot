import pygame
import sys

# Ініціалізація Pygame
pygame.init()

# Розмір ігрового вікна
WIDTH, HEIGHT = 300, 300
WINDOW_SIZE = (WIDTH, HEIGHT)
GRID_SIZE = 3  # Розмірність ігрового поля
CELL_SIZE = WIDTH // GRID_SIZE

# Колір
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)

# Інші кольори
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)

# Ігрова логіка
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player_turn = 'X'
game_over = False


def computer_move():
    # Функція для обчислення мінімального значення (для гравця X)
    def min_value(board):
        winner = check_winner()
        if winner:
            if winner == 'X':
                return -1
            elif winner == 'O':
                return 1
        if check_draw():
            return 0

        min_val = float('inf')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == '':
                    board[row][col] = 'X'
                    val = max_value(board)
                    min_val = min(min_val, val)
                    board[row][col] = ''
        return min_val

    # Функція для обчислення максимального значення (для гравця O)
    def max_value(board):
        winner = check_winner()
        if winner:
            if winner == 'X':
                return -1
            elif winner == 'O':
                return 1
        if check_draw():
            return 0

        max_val = float('-inf')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == '':
                    board[row][col] = 'O'
                    val = min_value(board)
                    max_val = max(max_val, val)
                    board[row][col] = ''
        return max_val

    best_move = None
    best_score = float('-inf')
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == '':
                board[row][col] = 'O'
                score = min_value(board)
                board[row][col] = ''
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move



# Функція для відображення кнопок "Нова гра" і "Закрити"
def draw_end_game_buttons(new_game_button, close_button, font):
    pygame.draw.rect(screen, (0, 255, 0), new_game_button)
    pygame.draw.rect(screen, (255, 0, 0), close_button)
    new_game_text = font.render("Нова гра", True, LINE_COLOR)
    close_text = font.render("Закрити", True, LINE_COLOR)
    screen.blit(new_game_text, new_game_button.move(10, 10))
    screen.blit(close_text, close_button.move(10, 10))

# Створення ігрового вікна
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Хрестики-нолики")

# Функція для малювання ігрового поля
def draw_grid():
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), 2)
        pygame.draw.line(screen, LINE_COLOR, (row * CELL_SIZE, 0), (row * CELL_SIZE, HEIGHT), 2)

# Функція для малювання "Хрестика" (X)
def draw_x(row, col):
    x_pos = col * CELL_SIZE
    y_pos = row * CELL_SIZE
    pygame.draw.line(screen, X_COLOR, (x_pos, y_pos), (x_pos + CELL_SIZE, y_pos + CELL_SIZE), 3)
    pygame.draw.line(screen, X_COLOR, (x_pos + CELL_SIZE, y_pos), (x_pos, y_pos + CELL_SIZE), 3)

# Функція для малювання "Нолика" (O)
def draw_o(row, col):
    x_pos = col * CELL_SIZE + CELL_SIZE // 2
    y_pos = row * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 2 - 10
    pygame.draw.circle(screen, O_COLOR, (x_pos, y_pos), radius, 3)

# Перевірка переможця
def check_winner():
    for row in range(GRID_SIZE):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != '':
            return board[row][0]

    for col in range(GRID_SIZE):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return board[0][2]

    return None

# Перевірка на нічию
def check_draw():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == '':
                return False
    return True

# Функція для очищення ігрового поля
def reset_board():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            board[row][col] = ''

# Головна функція для запуску гри
def main():
    global player_turn, game_over
    font = pygame.font.Font(None, 36)
    new_game_button = pygame.Rect(10, 220, 120, 50)
    close_button = pygame.Rect(170, 220, 120, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    col = event.pos[0] // CELL_SIZE
                    row = event.pos[1] // CELL_SIZE
                    if board[row][col] == '':
                        board[row][col] = player_turn
                        player_turn = 'O' if player_turn == 'X' else 'X'
                        winner = check_winner()
                        if winner:
                            game_over = True
                        elif check_draw():
                            game_over = True

        # Очистка екрану
        screen.fill(WHITE)

        # Малювання ігрового поля
        draw_grid()

        # Малювання "Хрестиків" і "Ноликів"
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == 'X':
                    draw_x(row, col)
                elif board[row][col] == 'O':
                    draw_o(row, col)

        # Перевірка, чи гра закінчилася
        if not game_over:
            if player_turn == 'O':
                # Розраховуємо хід комп'ютера і змінюємо стан гри
                row, col = computer_move()
                board[row][col] = player_turn
                player_turn = 'X'
                winner = check_winner()
                if winner:
                    game_over = True
                elif check_draw():
                    game_over = True

        # Виведення переможця або нічиєї
        if game_over:
            winner_text = "Нічия!" if not winner else f"Переможець: {winner}"
            text_color = (255, 0, 0)
            text = font.render(winner_text, True, text_color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(text, text_rect)

            # Виклик функції для відображення кнопок "Нова гра" і "Закрити" і передача змінних
            draw_end_game_buttons(new_game_button, close_button, font)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if new_game_button.collidepoint(event.pos):
                        reset_board()
                        player_turn = 'X'
                        game_over = False
                    elif close_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()


        # Оновлення відображення
        pygame.display.update()

if __name__ == "__main__":
    main()
