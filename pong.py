import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 500

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# define font
font = pygame.font.SysFont('Arial', 30)

# define game variables
live_ball = False
margin = 50
cpu_score = 0
player_score = 0
fps = 60
winner = 0
speed_increase = 0

# define the colors
bg = (50, 50, 50)
white = (255, 255, 255)


def draw_board():
    screen.fill(bg)
    pygame.draw.line(screen, white, (0, margin), (screen_width, margin))


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


class paddle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 20, 100)
        self.speed = 5

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed)
        if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed)

    def draw(self):
        pygame.draw.rect(screen, white, self.rect)

    def ai(self):
        # ai to move the paddle
        # move down if ball is lower than paddle
        if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed)
        # move up if ball is higher than paddle
        if self.rect.centery > pong.rect.top and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed)


class ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):

        # add collision with top
        if self.rect.top < margin:
            self.speed_y *= -1
        # add collision with bottom
        if self.rect.bottom > screen_height:
            self.speed_y *= -1
        # add collision with paddles
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
            self.speed_x *= -1

        # check for out of bounds
        if self.rect.left < 0:
            self.winner = 1
        if self.rect.left > screen_width:
            self.winner = -1

        print(self.winner)
        # update ball position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        return self.winner

    def draw(self):
        pygame.draw.circle(screen, white, (self.rect.x + self.ball_rad,
                           self.rect.y + self.ball_rad), self.ball_rad)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.ball_rad = 8
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = -4
        self.speed_y = 4
        self.winner = 0  # 1 means cpu wins, -1 means player wins

# create the paddles


player_paddle = paddle(screen_width - 40, screen_height//2)
cpu_paddle = paddle(20, screen_height//2)

# create the ball
pong = ball(screen_width - 60, screen_height//2 + 50)

run = True
while run:

    fpsClock.tick(fps)
    draw_board()
    draw_text(f'CPU: {cpu_score}', font, white, 20, 15)
    draw_text(f'P1: {player_score}', font, white, screen_width-100, 15)
    draw_text('BALL SPEED: ' + str(abs(pong.speed_x)),
              font, white, screen_width // 2 - 100, 15)

    # draw the paddles
    player_paddle.draw()
    cpu_paddle.draw()

    if live_ball:
        speed_increase += 1
        # move the ball
        winner = pong.move()
        if winner == 0:
            # move paddle
            player_paddle.move()
            cpu_paddle.ai()
            # draw the ball
            pong.draw()
        else:
            live_ball = False
            if winner == 1:
                player_score += 1
            else:
                cpu_score += 1
    # print player instructions
    if not live_ball:
        if winner == 0:
            draw_text('CLICK ANYWHERE TO START', font,
                      white, 100, screen_height // 2 - 100)
        if winner == 1:
            draw_text('YOU WON', font, white, 220, screen_height // 2 - 50)
            draw_text('CLICK ANYWHERE TO START', font,
                      white, 100, screen_height // 2 - 100)
        if winner == -1:
            draw_text('YOU LOST', font, white, 220, screen_height // 2 - 50)
            draw_text('CLICK ANYWHERE TO START', font,
                      white, 100, screen_height // 2 - 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not live_ball:
            live_ball = True
            pong.reset(screen_width - 60, screen_height//2 + 50)

    if speed_increase > 500:
        speed_increase = 0
        if pong.speed_x < 0:
            pong.speed_x -= 1
        if pong.speed_x > 0:
            pong.speed_x += 1
        if pong.speed_y < 0:
            pong.speed_y -= 1
        if pong.speed_y > 0:
            pong.speed_y += 1

    pygame.display.update()

pygame.quit()
