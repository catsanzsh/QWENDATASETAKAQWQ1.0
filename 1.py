import pygame
import sys
import random

pygame.init()

# Game setup
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)
BALL_COLOR = (255, 255, 255)
PADDLE_COLOR = (255, 255, 255)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Game objects
ball = pygame.Rect(WIDTH//2 - 15, HEIGHT//2 - 15, 30, 30)
player_paddle = pygame.Rect(10, HEIGHT//2 - 70, 10, 140)
opponent_paddle = pygame.Rect(WIDTH - 20, HEIGHT//2 - 70, 10, 140)
ball_velocity = [random.choice((4, -4)), 4]
player_score = 0
opponent_score = 0

game_over = False
winner = None

def reset_ball():
    global ball_velocity
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_velocity = [random.choice((4, -4)), 4]

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= 5
    if keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
        player_paddle.y += 5
    
    # Opponent movement (AI)
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += 3
    else:
        opponent_paddle.y -= 3
    opponent_paddle.top = max(opponent_paddle.top, 0)
    opponent_paddle.bottom = min(opponent_paddle.bottom, HEIGHT)
    
    # Ball movement
    ball.x += ball_velocity[0]
    ball.y += ball_velocity[1]
    
    # Wall collisions
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_velocity[1] *= -1
    # Score check
    if ball.left <= 0:
        opponent_score += 1
        if opponent_score >=5:
            game_over = True
            winner = "opponent"
        reset_ball()
    if ball.right >= WIDTH:
        player_score += 1
        if player_score >=5:
            game_over = True
            winner = "player"
        reset_ball()
    
    # Paddle collisions
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_velocity[0] *= -1
    
    # Drawing
    screen.fill(BG_COLOR)
    pygame.draw.ellipse(screen, BALL_COLOR, ball)
    pygame.draw.rect(screen, PADDLE_COLOR, player_paddle)
    pygame.draw.rect(screen, PADDLE_COLOR, opponent_paddle)
    pygame.draw.aaline(screen, (80,80,80), (WIDTH/2,0), (WIDTH/2,HEIGHT))
    
    # Score display
    font = pygame.font.Font(None, 36)
    player_text = font.render(f"{player_score}", True, (150,150,150))
    opponent_text = font.render(f"{opponent_score}", True, (150,150,150))
    screen.blit(player_text, (WIDTH//2 - 50, 20))
    screen.blit(opponent_text, (WIDTH//2 + 30, 20))
    
    # Game over message
    if game_over:
        font = pygame.font.Font(None, 72)
        message = "YOU WIN!" if winner == "player" else "YOU LOSE!"
        text = font.render(message, True, (255,255,255))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)
    
    pygame.display.flip()
    
    if game_over:
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()
    
    clock.tick(FPS)
