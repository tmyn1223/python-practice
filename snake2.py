import pygame
import random

pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move Hero")

my_font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

def spawn_food_and_obstacles():
    global rect_x, rect_y, obstacles
    
    rect_x = random.randint(60, WIDTH - 60)
    rect_y = random.randint(60, HEIGHT - 60)
    
    obstacles = []
    for _ in range(2):
        offset_x = random.choice([-1, 1]) * random.randint(50, 100)
        offset_y = random.choice([-1, 1]) * random.randint(50, 100)
        
        obs_x = max(20, min(WIDTH - 80, rect_x + offset_x))
        obs_y = max(20, min(HEIGHT - 80, rect_y + offset_y))
        
        # 壁ランダム
        if random.random() < 0.5:
            obs_w, obs_h = 15, 80
        
        obstacles.append((obs_x, obs_y, obs_w, obs_h))

def reset_game():
    global hero_x, hero_y, rect_x, rect_y, speed, direction_x, direction_y, snake, score, game_over
    global food_size, obstacles
    
    hero_x = random.randint(100, 400)
    hero_y = random.randint(100, 400)
    speed = 20
    score = 0
    food_size = 30
    direction_x = speed
    direction_y = 0
    game_over = False
    
    spawn_food_and_obstacles()
    
    snake = []
    for i in range(6):
        snake.append((hero_x - i * 20, hero_y))

reset_game()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_c:
                    reset_game()
                elif event.key == pygame.K_e:
                    running = False
            else:
                if event.key == pygame.K_UP:
                    direction_x = 0
                    direction_y = -speed
                elif event.key == pygame.K_DOWN:
                    direction_x = 0
                    direction_y = speed
                elif event.key == pygame.K_LEFT:
                    direction_x = -speed
                    direction_y = 0
                elif event.key == pygame.K_RIGHT:
                    direction_x = speed
                    direction_y = 0

                elif event.key == pygame.K_LSHIFT:
                    speed = 40
                    if direction_x > 0: direction_x = speed
                    elif direction_x < 0: direction_x = -speed
                    elif direction_y > 0: direction_y = speed
                    elif direction_y < 0: direction_y = -speed
            
        if event.type == pygame.KEYUP and not game_over:
            if event.key == pygame.K_LSHIFT:
                speed = 20
                if direction_x > 0: direction_x = speed
                elif direction_x < 0: direction_x = -speed
                elif direction_y > 0: direction_y = speed
                elif direction_y < 0: direction_y = -speed

    if not game_over:
        hero_x += direction_x
        hero_y += direction_y
        snake.insert(0, (hero_x, hero_y))
        snake.pop()

        # 頭の判定
        hero_rect = pygame.Rect(hero_x - 15, hero_y - 15, 30, 30)

        # えさの判定
        if abs(hero_x - rect_x) < (food_size + 10) and abs(hero_y - rect_y) < (food_size + 10):
            spawn_food_and_obstacles()
            speed += 2
            score += 1
            food_size = max(5, food_size - 3)

        # 壁の判定
        for obs_x, obs_y, obs_w, obs_h in obstacles:
            wall_rect = pygame.Rect(obs_x, obs_y, obs_w, obs_h)
            if hero_rect.colliderect(wall_rect):
                game_over = True

        # 画面外判定
        if hero_x > 500 or hero_x < 0 or hero_y > 500 or hero_y < 0:
            game_over = True

    screen.fill((209, 27, 0))

    for i, (x, y) in enumerate(snake):
        if i == 0:
            pygame.draw.circle(screen, (0, 200, 0), (x, y), 20)
            pygame.draw.circle(screen, (255, 200, 255), (x + 6, y - 5), 4)
            pygame.draw.circle(screen, (255, 255, 255), (x + 6, y - 6), 4)
            pygame.draw.circle(screen, (0, 0, 0), (x + 6, y - 5), 2)
            pygame.draw.circle(screen, (0, 0, 0), (x + 6, y - 5), 2)
            pygame.draw.line(screen, (255, 0, 0), (x + 20, y), (x + 30, y - 4), 2)
        else:
            radius = max(4, 20 - i * 2)
            green = max(80, 200 - i * 20)
            pygame.draw.circle(screen, (0, green, 0), (x, y), radius)
    
    pygame.draw.rect(screen, (0, 234, 19), (rect_x, rect_y, food_size, food_size))

    #壁
    for obs_x, obs_y, obs_w, obs_h in obstacles:
        pygame.draw.rect(screen, (100, 100, 100), (obs_x, obs_y, obs_w, obs_h))

    score_text = my_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        go_text = my_font.render("GAME OVER", True, (255, 50, 50))
        msg_text = small_font.render("Press 'C' to Restart / 'E' to Exit", True, (255, 255, 255))
        
        screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, 180))
        screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, 250))

    pygame.display.update()
    clock.tick(10)

pygame.quit()