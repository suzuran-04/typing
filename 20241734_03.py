import tkinter as tk
import random
import time
import math

# ゲームの設定
WIDTH, HEIGHT = 600, 400
player_size = 20
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5

# 赤い目（敵）の設定
enemy_size = 20
enemy_x, enemy_y = random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size)
enemy_speed = 5  # 敵の追跡速度

# ゲームウィンドウの設定
root = tk.Tk()
root.title("Simple Horror Game")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
canvas.pack()

# プレイヤーの描画
player = canvas.create_rectangle(player_x, player_y, player_x + player_size, player_y + player_size, fill='white')

# 赤い目の描画
enemy = canvas.create_oval(enemy_x, enemy_y, enemy_x + enemy_size, enemy_y + enemy_size, fill='red')

# プレイヤーの移動
def move_player(event):
    global player_x, player_y

    if event.keysym == 'Left':
        player_x -= player_speed
    elif event.keysym == 'Right':
        player_x += player_speed
    elif event.keysym == 'Up':
        player_y -= player_speed
    elif event.keysym == 'Down':
        player_y += player_speed

    # プレイヤーが画面外に出ないように制限
    player_x = max(0, min(player_x, WIDTH - player_size))
    player_y = max(0, min(player_y, HEIGHT - player_size))

    # プレイヤーの位置を更新
    canvas.coords(player, player_x, player_y, player_x + player_size, player_y + player_size)

# 敵の移動（プレイヤーを追いかける）
def move_enemy():
    global enemy_x, enemy_y

    # プレイヤーの位置との距離を計算
    dx = player_x - enemy_x
    dy = player_y - enemy_y
    distance = math.sqrt(dx**2 + dy**2)

    # 敵がプレイヤーに近づくための方向ベクトルを計算
    if distance != 0:
        dx /= distance
        dy /= distance

    # 敵をプレイヤーの方向に移動させる
    enemy_x += dx * enemy_speed
    enemy_y += dy * enemy_speed

    # 敵の位置を更新
    canvas.coords(enemy, enemy_x, enemy_y, enemy_x + enemy_size, enemy_y + enemy_size)

# 衝突判定
def check_collision():
    player_coords = canvas.coords(player)
    enemy_coords = canvas.coords(enemy)

    # 衝突判定（プレイヤーと敵が重なっているか）
    if (player_coords[2] > enemy_coords[0] and player_coords[0] < enemy_coords[2] and
        player_coords[3] > enemy_coords[1] and player_coords[1] < enemy_coords[3]):
        return True
    return False

# ゲームループ
def game_loop():
    # 敵の移動
    move_enemy()

    # 衝突判定
    if check_collision():
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text="GAME OVER", fill='red', font=('Arial', 30))
        root.after(5000, root.quit)  # 5秒後にゲームを終了

    # ゲームの更新
    root.after(50, game_loop)

# キーイベントのバインディング
root.bind('<Left>', move_player)
root.bind('<Right>', move_player)
root.bind('<Up>', move_player)
root.bind('<Down>', move_player)

# ゲーム開始
game_loop()

# ウィンドウを表示
root.mainloop()
