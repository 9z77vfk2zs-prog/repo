import pygame
import random
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

GAME_SPEED = 10


class GameObject:
    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        raise NotImplementedError("Метод draw должен быть реализован в дочернем классе")


class Apple(GameObject):
    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self, surface):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last_position = None

    def update_direction(self):
        if self.next_direction:
            if (
                self.next_direction[0] + self.direction[0] != 0
                or self.next_direction[1] + self.direction[1] != 0
            ):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_position = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.last_position = self.positions[-1] if len(self.positions) > 0 else None
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        return self.positions[0]

    def grow(self):
        self.length += 1

    def check_self_collision(self):
        head = self.get_head_position()
        return head in self.positions[1:]

    def draw(self, surface):
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        if self.last_position and self.last_position not in self.positions:
            rect = pygame.Rect(self.last_position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BACKGROUND_COLOR, rect)


def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)

        snake.update_direction()

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()

            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.check_self_collision():
            snake.reset()

        screen.fill(BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        clock.tick(GAME_SPEED)


if __name__ == "__main__":
    main()
