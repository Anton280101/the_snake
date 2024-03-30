from random import choice, randint

import pygame as pg

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
SPEED = 15

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

OPPOSITE = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}


class GameObject:
    """Класс игрового объекта."""

    def __init__(self, bg_color=None):
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color = bg_color

    def draw_cell(self, surface, position):
        """Создание ячейки."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE,))
        if self.body_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(surface, self.body_color, rect)
        else:
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)

    def draw(self, surface):
        """Метод для отображения игрового объекта на экране."""
        raise NotImplementedError(
               'Метод draw должен быть переопределен в подклассе'
        )


class Apple(GameObject):
    """Класс для яблока, наследуется от GameObject."""

    def __init__(self, bg_color=APPLE_COLOR, occupied_cells=()):
        super().__init__(bg_color)
        self.occupied_cells = occupied_cells
        self.randomize_position(self.occupied_cells)

    def randomize_position(self, occupied_cells):
        """Реализация случайного появления яблока."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_cells:
                break

    def draw(self, surface):
        """Метод draw класса Apple."""
        self.draw_cell(surface, self.position)


class Snake(GameObject):
    """Класс для змейки, наследуется от GameObject."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация змейки с заданными позицией и цветом."""
        super().__init__(body_color)
        self.reset()
        self.next_direction = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки."""
        head_x, head_y = self.get_head_position()
        x_direction, y_direction = self.direction
        x_new = (GRID_SIZE * x_direction + head_x) % SCREEN_WIDTH
        y_new = (GRID_SIZE * y_direction + head_y) % SCREEN_HEIGHT

        self.positions.insert(0, (x_new, y_new))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self, surface):
        """Метод draw класса Snake. Рисует змейку."""
        for position in self.positions[:-1]:
            self.draw_cell(surface, position)

        self.draw_cell(surface, self.positions[0])

        if self.last:
            last_rect = pg.Rect(
                self.last,
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    keys = {pg.K_UP: UP, pg.K_DOWN: DOWN,
            pg.K_LEFT: LEFT, pg.K_RIGHT: RIGHT}
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            print(f'Press key... {event.key}')
            direction = keys.get(event.key)
            if direction and game_object.direction != OPPOSITE[direction]:
                game_object.next_direction = direction


def main():
    """Создаем экземпляры классов"""
    # Инициализация PyGame:
    pg.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        apple.draw(screen)
        snake.draw(screen)

        pg.display.update()


if __name__ == '__main__':
    main()
    pg.quit()
