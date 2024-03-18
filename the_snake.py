import pygame as pg
from random import randint, choice

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')
# Настройка времени:
clock = pg.time.Clock()


# Класс игрового объекта
class GameObject:
    """Класс игрового объекта."""

    def __init__(self, body_color=None):
        """Инициализация игрового объекта.
        Устанавливает начальные значения атрибутов объекта.
        """
        self.body_color = body_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Метод для отображения игрового объекта на экране."""
        raise NotImplementedError('Метод draw должен быть переопределен в подклассе')


# Класс Яблока
class Apple(GameObject):
    """Класс Яблока, наследуется от класса GameObject."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализация яблока."""
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Установка случайной позиции для яблока."""
        self.position = [
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        ]

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, APPLE_COLOR, rect)  # ДОЛЖЕН БЫТЬ self.body_color, по аналогии со Snake
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


# Класс Змейки
class Snake(GameObject):
    """Класс Змейки, наследуется от класса GameObject."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация змейки.
        Устанавливает начальные значения атрибутов змейки,
        включая длину, позиции, направление и цвет.
        """
        super().__init__(body_color)
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.last = None
        self.length = 1
        self.reset()

    def draw(self):
        """Отрисовка змейки на экране."""
        # Отрисовка головы Змейки
        head_rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Движение змейки."""
        head_x, head_y = self.positions[0]
        direction_x, direction_y = self.direction
        position = (
            (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        )

        self.positions.insert(0, position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def update_direction(self):
        """Обновление направления объекта."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]


def handle_keys(game_object):
    """Обработка нажатий клавиш для управления объектом."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция программы."""
    # Инициализация PyGame:
    screen.fill(BOARD_BACKGROUND_COLOR)
    pg.init()
    snake = Snake()
    apple = Apple(snake.position)

    while True:
        clock.tick(SPEED)
        snake.draw()
        apple.draw()

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head_position = snake.get_head_position()
        for index in range(4, len(snake.positions)):
            if head_position == snake.positions[index]:
                # Определенное действие при попадании головы в позиции от 4 элемента змейки
                pass

        if snake.get_head_position() != apple.position:
            snake.move()
        else:
            snake.length += 1
            apple.randomize_position()
            snake.move()

        if snake.length != len(set(snake.positions)):
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()
            snake.reset()

        pg.display.update()


if __name__ == '__main__':
    main()
    pg.quit()
