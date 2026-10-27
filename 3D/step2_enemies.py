from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

import random

app = Ursina()

ground = Entity(model='plane',scale = 60,texture='grass',texture_scale=(60,60),
                color = color.lime,collider='box')

player = FirstPersonController()

enemies = []

for i in range(8):
    enemy = Entity(model='sphere',color=color.yellow,scale=1.5,collider='box',
                   position=(random.randint(-20,20),0.75,random.randint(10,25)))
    enemies.append(enemy)

score= 0
score_text = Text(text='Score: 0', position=(-0.85, 0.45), scale=2)


# Step 3 - add 2​

def input(key):

    global score

    if key == 'left mouse down':

        if mouse.hovered_entity in enemies:

            enemy = mouse.hovered_entity

            enemies.remove(enemy)

            destroy(enemy)

            score += 1

            score_text.text = 'Score: ' + str(score)
#Step 4
def update():
    for enemy in enemies:
        enemy.look_at_2d(player.position,'y')
        enemy.position += enemy.forward * time.dt * 2

Sky()
app.run()