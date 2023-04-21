from PyQt5.QtWidgets import QMessageBox, QApplication
import pygame
import random
import sys


# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Display
pygame.init()
screen = pygame.display.set_mode((470, 470))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
screen.fill(BLACK)
app = QApplication([])

# Making Game
class Snake:
    def __init__(self, x, y, width, height):
        self.image = None
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = (0, 0)
        self.body = []

    def draw(self, color):
        pygame.draw.rect(screen, color, self.rect)
        for part in self.body:
            pygame.draw.rect(screen, WHITE, part)

    def move(self):
        dx, dy = self.direction
        new_part_x = self.rect.x
        new_part_y = self.rect.y
        self.rect.x += dx
        self.rect.y += dy
        if self.body:
            self.body.pop(0)
            self.body.append(pygame.Rect(new_part_x, new_part_y, 17, 17))

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

class Text:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = None

    def set_text(self, text, fsize):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, WHITE)
        screen.blit(self.image, (self.x, self.y))

    def draw_text(self, shift_x=0, shift_y=0):
        screen.blit(self.image, (self.x + shift_x, self.y + shift_y))

# Getting random cords for the snake's head
get_random_cord_x = random.randint(0, 470)
get_random_cord_y = random.randint(0, 470)

# Snake Head
snake_head = Snake(get_random_cord_x, get_random_cord_y, 17, 17)
snake_head.draw(RED)
snake_body = []

# Getting random cords for the Fruits
get_random_cord_x = random.randint(10, 450)
get_random_cord_y = random.randint(10, 450)

# Fruits
fruits = Snake(get_random_cord_x, get_random_cord_y, 10, 10)
fruits.draw(GREEN)

# Points Text
points_score = 0
points = Text(0, 0)
points.set_text(f"Points: {points_score}", 15)
points.draw_text()

# Events
running = True
while running:
    pygame.display.update()
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                snake_head.direction = (-10, 0)
            elif event.key == pygame.K_d:
                snake_head.direction = (10, 0)
            elif event.key == pygame.K_w:
                snake_head.direction = (0, -10)
            elif event.key == pygame.K_s:
                snake_head.direction = (0, 10)

    if snake_head.rect.left > screen.get_width():
        snake_head.rect.right = 0
    elif snake_head.rect.right < 0:
        snake_head.rect.left = screen.get_width()
    elif snake_head.rect.top > screen.get_height():
        snake_head.rect.bottom = 0
    elif snake_head.rect.bottom < 0:
        snake_head.rect.top = screen.get_height()

    # Move snake and check for collision with fruits
    snake_head.move()
    for snake_part in snake_head.body:
        if snake_head.collidepoint(snake_part.centerx, snake_part.centery):
            pygame.display.update()
            QMessageBox.information(None, "YOU LOST!", 'You lost the game! Thanks for playing')
            sys.exit()
    if snake_head.collidepoint(fruits.rect.centerx, fruits.rect.centery):
        fruits.rect.x = random.randint(10, 450)
        fruits.rect.y = random.randint(10, 450)
        new_snake_part = pygame.Rect(snake_head.rect.x, snake_head.rect.y, 17, 17)
        snake_head.body.append(new_snake_part)
        points_score += 1
        points.set_text(f"Points: {points_score}", 15)
        points.draw_text()

    # Redraw everything
    screen.fill(BLACK)
    snake_head.draw(RED)
    fruits.draw(GREEN)
    points.draw_text()


pygame.quit()
sys.exit(app.exec_())
