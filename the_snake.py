import pygame
from random import choice, randint

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')
# Настройка времени:
clock = pygame.time.Clock()
screen.fill(BOARD_BACKGROUND_COLOR)
pygame.display.flip()


# Класс игрового объекта
class GameObject:
    def __init__(self):
        self.next_direction = None
        self.body_color = None
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.direction = None

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


# Класс Яблока
class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        self.position = [randint(0, GRID_WIDTH - 1) * GRID_SIZE, randint(0, GRID_HEIGHT - 1) * GRID_SIZE]

    def draw(self, surface):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


# Класс Змейки
class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.last = None
        self.length = 1
        self.positions = [self.position.copy()]
        self.direction = RIGHT
        self.body_color = SNAKE_COLOR

    def move(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.positions[0]
        new_head = [head_x + self.direction[0] * GRID_SIZE, head_y + self.direction[1] * GRID_SIZE]
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

        # Перемещение змейки на противоположную сторону, если выходит за границы
        if new_head[0] < 0:
            new_head[0] = SCREEN_WIDTH - GRID_SIZE
        elif new_head[0] >= SCREEN_WIDTH:
            new_head[0] = 0
        if new_head[1] < 0:
            new_head[1] = SCREEN_HEIGHT - GRID_SIZE
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head[1] = 0

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 1
        self.positions = [self.position.copy()]
        self.direction = RIGHT
        self.next_direction = None


def main():
    snake = Snake()
    apple = Apple()

    screen.fill(BOARD_BACKGROUND_COLOR)
    apple.randomize_position()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.handle_keys()
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            snake.length += 1

        # Проверка столкновения головы змеи с телом
        for segment in snake.positions[1:]:
            if snake.positions[0] == segment:
                snake.reset()  # Вызов метода reset у объекта snake
                break

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
pygame.quit()
