from ursina import *

app = Ursina()

# ウィンドウ設定
window.title = 'Basketball Free Throw - Mouse Control'
window.color = color.rgb(0, 30, 30)

# カメラの描画範囲（クリッピング）を明示的に広げることで、奥のオブジェクトが消えるのを防ぐ
camera.clip_plane_near = 0.1
camera.clip_plane_far = 100.0

# ライティングと背景（白飛びを防ぐため）
DirectionalLight().look_at(Vec3(1, -1, -1))
AmbientLight(color=color.rgb(150, 150, 150))

# 背景（床と壁）
floor = Entity(model='plane', scale=(20, 1, 30), color=color.rgb(80, 50, 30))
wall = Entity(model='cube', position=(0, 6, 15), scale=(20, 12, 1), color=color.rgb(40, 40, 40))

# バスケットゴール
backboard = Entity(model='cube', position=(0, 6, 10), scale=(3, 2, 0.2), color=color.white)
rim = Entity(model='cylinder', position=(0, 5.0, 9.2), scale=(1.2, 0.1, 1.2), color=color.red)

# スコアと操作説明のテキスト
score = 0
score_text = Text(text=f'SCORE: {score}', position=(-0.85, 0.45), scale=2, color=color.white)
guide_text = Text(text='[Click & Drag] to Aim and Release to Shoot!', position=(-0.4, 0.35), scale=1.2, color=color.yellow)

# バスケットボール
ball = Entity(model='sphere', position=(0, 1.5, 2), scale=0.8, color=color.orange)

# 状態管理
is_shooting = False
is_dragging = False
drag_start_pos = Vec2(0, 0)
velocity = Vec3(0, 0, 0)

def input(key):
    global is_dragging, drag_start_pos, is_shooting
    if key == 'left mouse down' and not is_shooting:
        is_dragging = True
        drag_start_pos = mouse.position
    elif key == 'left mouse up' and is_dragging and not is_shooting:
        is_dragging = False
        drag_vector = mouse.position - drag_start_pos
        
        is_shooting = True
        power_x = drag_vector.x * 2.0
        power_y = max(drag_vector.y * 3.0, 0.2)
        power_z = max(drag_vector.y * 4.0, 0.5)
        
        global velocity
        velocity = Vec3(power_x, power_y, power_z)

def update():
    global is_shooting, score, velocity
    
    if is_shooting:
        # 物理シミュレーション（移動と重力）
        ball.position += velocity
        velocity.y -= 0.015  # 重力
        
        # ゴール判定（リングの近くを通過し、かつ落下中であること）
        if distance(ball.position, rim.position) < 1.0 and velocity.y < 0:
            score += 100
            score_text.text = f'SCORE: {score}'
            reset_ball()
            
        # 地面に落ちた、または遠くに行き過ぎた場合のリセット
        if ball.y < 0 or ball.z > 14:
            reset_ball()

def reset_ball():
    global is_shooting, velocity
    is_shooting = False
    velocity = Vec3(0, 0, 0)
    ball.position = (0, 1.5, 2)

# カメラの位置（少し上から全体を見渡すアングル）
camera.position = (0, 6, -3)
camera.rotation = (20, 0, 0)

app.run()