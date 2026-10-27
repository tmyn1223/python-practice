import pygame
import random
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Move Hero")
hero_x = 250
hero_y = 250
rect_x = 100
rect_y = 100
hero_color = (255,60,55)
rect_color = (0,255,45)
my_font = pygame.font.SysFont(None,50)
running = True
Game_over = False
speed = 20
pygame.mixer.init()
sound = pygame.mixer.Sound("voice_01.wav")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                speed = 170
            hero_color =(25,245,35)
            rect_color =(100,0,255)
            if event.key == pygame.K_UP:
                hero_y -= speed
            elif event.key == pygame.K_DOWN:
                hero_y += speed
            elif event.key == pygame.K_LEFT:
                hero_x -= speed
            elif event.key == pygame.K_RIGHT:
                hero_x += speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                speed = 20
            hero_color = (255,0,0)

    screen.fill((25,255,255))
    pygame.draw.circle(screen,hero_color,(hero_x,hero_y),30)
    pygame.draw.rect(screen,rect_color,(rect_x,rect_y,30,30))
    if abs(hero_x - rect_x)<30 and abs(hero_y - rect_y)<30:
        rect_x = random.randint(20,400)
        rect_y = random.randint(20.480)
    if (hero_x>500 or hero_x<0 or hero_y>500 or hero_y<0):
        msg = my_font.render("Game Over",True,(239,244,234))
        (msg,(150,200))
        screen.blit(msg, (150,200))
    pygame.display.update()
pygame.quit()
