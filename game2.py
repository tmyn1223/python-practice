from ursina import *

app = Ursina()

# ウィンドウ設定
window.title = 'Basketball Free Throw - Mouse Control'
window.color = color.rgb(0, 30, 30)
camera.clip_plane_near = 0.1
camera.clip_plane_far = 100.0

DirectionalLight().look_at(Vec3(1, -1, -1))
AmbientLight(color=color.rgb(150, 150, 150))

# 背景
floor = Entity(model='plane', scale=(20, 1, 30), color=color.rgb(80, 50, 30))
wall = Entity(model='cube', position=(0, 6, 15), scale=(20, 12, 1), color=color.rgb(40, 40, 40))

# バスケットゴール
backboard = Entity(model='cube', position=(0, 6, 10), scale=(3, 2, 0.2), color=color.white)
rim = Entity(model='cylinder', position=(0, 5.0, 9.2), scale=(1.2, 0.1, 1.2), color=color.red)

# スコア
score = 0
score_text = Text(text=f'SCORE: {score}', position=(-0.85, 0.45), scale=2, color=color.white)
guide_text = Text(text='[Click & Drag] to Aim and Release to Shoot!', position=(-0.4, 0.35), scale=1.2, color=color.yellow)

# ボール
ball = Entity(model='sphere', position=(0, 1.5, 2), scale=0.8, color=color.orange)

# 状態管理
is_shooting = False
is_dragging = False
drag_start_pos = Vec2(0, 0)
velocity = Vec3(0, 0, 0)

def reset_ball():
    global is_shooting, velocity
    is_shooting = False
    velocity = Vec3(0, 0, 0)
    ball.position = (0, 1.5, 2)

def input(key):
    global is_dragging, drag_start_pos, is_shooting

    if key == 'left mouse down' and not is_shooting:
        is_dragging = True
        drag_start_pos = mouse.position

    elif key == 'left mouse up' and is_dragging and not is_shooting:
        is_dragging = False

        drag_vector = mouse.position - drag_start_pos
        # ドラッグ量をそのまま発射ベクトルにする
        power_x = drag_vector.x * 6.0
        power_y = max(drag_vector.y * 8.0, 1.0)
        power_z = 8.0 + max(abs(drag_vector.x), abs(drag_vector.y)) * 10.0

        # 逆方向に引いたときだけ前へ飛ばすようにする
        if drag_vector.length() < 0.05:
            reset_ball()
            return

        global velocity
        velocity = Vec3(power_x, power_y, power_z)

        is_shooting = True

def update():
    global is_shooting, score, velocity

    if is_shooting:
        ball.position += velocity
        velocity.y -= 0.017  # 重力
        velocity.z *= 0.998  # 前進を少し減衰
        velocity.x *= 0.998

        # リム付近でシュート成功
        if abs(ball.x - rim.x) < 0.8 and abs(ball.y - rim.y) < 0.8 and abs(ball.z - rim.z) < 0.8 and velocity.y < 0:
            score += 100
            score_text.text = f'SCORE: {score}'
            reset_ball()

        # 落下 or 飛び過ぎでリセット
        if ball.y < 0 or ball.z > 14:
            reset_ball()

# カメラ
camera.position = (0, 6, -3)
camera.rotation = (20, 0, 0)

app.run()