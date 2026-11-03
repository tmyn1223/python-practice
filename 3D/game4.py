import math
import random
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# --- 基本的世界（地面・プレイヤー・空） ---
ground = Entity(model='plane', scale=60, texture='white_cube',
                texture_scale=(60, 60), color=color.light_gray,
                collider='box')

player = FirstPersonController()
player.y = 2
player.speed = 8
player.cursor.visible = True

Sky()

# --- リアルなバスケットゴールの設置（グループ化用親オブジェクト） ---
goal_group = Entity(position=(0, 0, -15))

# バックボード（白・薄型）
backboard = Entity(parent=goal_group, model='cube', scale=(4, 2.6, 0.1), position=(0, 6, 0), color=color.white, collider='box')
# バックボードの中央の四角い枠（シュートターゲット）
board_target = Entity(parent=goal_group, model='cube', scale=(1.2, 0.8, 0.12), position=(0, 5.7, 0.02), color=color.red)

# リング（しっかり見えるように形状と大きさを調整）
rim = Entity(parent=goal_group, model='cube', scale=(1.6, 0.15, 1.6), position=(0, 4.8, 1.0), color=color.orange, collider='box')
# リングの内側をくり抜く代わりに、中心に小さめの立方体を置いてリング状に見せる、または見やすいシンプルな直方体の組み合わせにする
rim_hole = Entity(parent=goal_group, model='cube', scale=(1.2, 0.16, 1.2), position=(0, 4.8, 1.0), color=color.gray)

# ネット（円錐）
net = Entity(parent=goal_group, model='cone', scale=(1.1, 1.5, 1.1), position=(0, 3.8, 1.0), color=color.white, rotation_x=180)

# 支柱（ポール）をバックボードの後ろ側に配置
pole = Entity(parent=goal_group, model='cube', scale=(0.4, 9, 0.4), position=(0, 4.5, -0.3), color=color.dark_gray, collider='box')

# --- 障害物を20個設置 ---
obstacles = []
for i in range(20):
    rx = random.uniform(-10, 10)
    rz = random.uniform(-12, -4)
    ry = random.uniform(1.5, 5)
    
    obs = Entity(
        model='cube', 
        scale=(random.uniform(1, 2), random.uniform(1, 2.5), random.uniform(1, 2)), 
        position=(rx, ry, rz), 
        color=color.random_color(), 
        collider='box'
    )
    obs.speed = random.uniform(1.5, 3.5)
    obs.direction = 1 if i % 2 == 0 else -1
    obstacles.append(obs)

all_colliders = [backboard, rim, pole] + obstacles

# --- 予測軌道のドット ---
prediction_dots = []
for i in range(30):
    dot = Entity(model='sphere', scale=0.12, color=color.yellow, enabled=False)
    prediction_dots.append(dot)

# --- UI（パワーゲージ・スコア） ---
power_bg = Entity(parent=camera.ui, model='quad', scale=(0.4, 0.04), position=(0, -0.4), color=color.dark_gray)
power_fill = Entity(parent=camera.ui, model='quad', scale=(0.0, 0.035), position=(-0.2, -0.4), origin=(-0.5, 0), color=color.orange)
power_text = Text(text="POWER: 0%", position=(0, -0.45), origin=(0,0), scale=1.2, color=color.yellow)

score = 0
score_text = Text(text=f'Score: {score}', position=(-0.85, 0.45), scale=2, color=color.white)
guide_text = Text(text="[Control] Hold Left Click to charge / WASD: Move", position=(-0.85, -0.4), scale=1, color=color.white)

# --- 変数 ---
balls = []
is_charging = False
power = 0
max_power = 35
charge_time = 0

def input(key):
    global is_charging, power, charge_time
    if key == 'left mouse down':
        is_charging = True
        charge_time = 0
        power = 0
        for dot in prediction_dots:
            dot.enabled = True

    elif key == 'left mouse up':
        if is_charging:
            ball = Entity(
                model='sphere', 
                scale=0.8, 
                color=color.orange, 
                position=player.position + camera.forward * 1 + Vec3(0, 1, 0),
                collider='sphere'
            )
            speed = max(5, power)
            ball.velocity = camera.forward * speed
            ball.gravity = -20
            balls.append(ball)
            
            is_charging = False
            power = 0
            charge_time = 0
            power_fill.scale_x = 0
            power_text.text = "POWER: 0%"
            for dot in prediction_dots:
                dot.enabled = False

def update():
    global score, power, charge_time
    
    for obs in obstacles:
        obs.x += obs.direction * obs.speed * time.dt
        if abs(obs.x) > 10:
            obs.direction *= -1

    if is_charging:
        charge_time += time.dt * 1.0  
        normalized_power = (charge_time % 1.0)
        power = normalized_power * max_power
        
        power_fill.scale_x = 0.4 * normalized_power
        power_text.text = f"POWER: {int(normalized_power * 100)}%"

        sim_pos = player.position + camera.forward * 1 + Vec3(0, 1, 0)
        sim_vel = camera.forward * power
        sim_gravity = -20
        
        for dot in prediction_dots:
            sim_vel += Vec3(0, sim_gravity, 0) * 0.04
            sim_pos += sim_vel * 0.04
            dot.position = sim_pos

    # 撃たれたボールの移動と衝突判定
    for ball in balls[:]:
        ball.velocity += Vec3(0, ball.gravity, 0) * time.dt
        ball.position += ball.velocity * time.dt
        
        hit_any = False
        hit_obj = None
        for obj in all_colliders:
            hit = ball.intersects(obj)
            if hit.hit:
                hit_any = True
                hit_obj = obj
                break
        
        if hit_any:
            ball.velocity *= -0.65
            if hit_obj == backboard:
                ball.z = (goal_group.z - 0.8)
            else:
                ball.position -= ball.velocity * time.dt * 4
            continue

        # ゴール判定
        world_rim_y = goal_group.y + rim.y
        world_rim_z = goal_group.z + rim.z
        
        if (abs(ball.x - goal_group.x) < 0.8 and 
            abs(ball.z - world_rim_z) < 0.8 and 
            world_rim_y - 0.2 < ball.y < world_rim_y + 0.4 and 
            ball.velocity.y < 0):
            score += 1
            score_text.text = f'Score: {score}'
            
            # ゴールが決まると高さをランダムに変更
            goal_group.y = random.uniform(0.0, 3.0)
            
            destroy(ball)
            balls.remove(ball)
            continue
            
        if ball.y < 0 or abs(ball.z) > 40 or abs(ball.x) > 40:
            destroy(ball)
            balls.remove(ball)

app.run()