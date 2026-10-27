from ursina import *

from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()

# Step 1 - add 1​

# 地面​

ground = Entity(model='plane', scale=60, texture='grass',

                texture_scale=(100, 100),color=color.light_gray,

                collider='box')


# Step 1 - add 2​

# プレイヤー​

player = FirstPersonController()


# Step 1 - add 3​

# 空​

Sky()

app.run()