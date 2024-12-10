import tkinter as tk
import random
import math
import time

# ゲームの設定
WIDTH, HEIGHT = 600, 400
player_size = 20
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
game_duration = 10  # プレイヤーが耐える時間（秒）
bullet_size = 10
bullet_speed = 5
bullets = []  # 弾（敵）のリスト
game_count = 0  # ゲームカウント

# ゲームウィンドウの設定
root = tk.Tk()
root.title("弾幕シューティング")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
canvas.pack()

# 背景画像を設定（背景画像は "background.png" として保存）
background_image = tk.PhotoImage(file="background.png")
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# プレイヤーの描画
player = canvas.create_rectangle(player_x, player_y, player_x + player_size, player_y + player_size, fill='white')

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

# 弾の発射（端から発射）
def spawn_bullet():
    # 画面の四隅または端からランダムに弾を発射
    spawn_position = random.choice(['top', 'bottom', 'left', 'right'])
    
    if spawn_position == 'top':
        bullet_x = random.randint(0, WIDTH)
        bullet_y = 0
        angle = random.uniform(math.pi / 4, 3 * math.pi / 4)  # 放射角度
    elif spawn_position == 'bottom':
        bullet_x = random.randint(0, WIDTH)
        bullet_y = HEIGHT
        angle = random.uniform(-3 * math.pi / 4, -math.pi / 4)  # 放射角度
    elif spawn_position == 'left':
        bullet_x = 0
        bullet_y = random.randint(0, HEIGHT)
        angle = random.uniform(0, math.pi)  # 放射角度
    else:  # 'right'
        bullet_x = WIDTH
        bullet_y = random.randint(0, HEIGHT)
        angle = random.uniform(-math.pi, 0)  # 放射角度

    # 弾の速度と移動方向
    velocity_x = math.cos(angle) * bullet_speed
    velocity_y = math.sin(angle) * bullet_speed

    bullet = {'x': bullet_x, 'y': bullet_y, 'vx': velocity_x, 'vy': velocity_y, 'obj': None}
    bullets.append(bullet)

# 弾の移動
def move_bullets():
    global bullets

    for bullet in bullets:
        # 弾の移動
        bullet['x'] += bullet['vx']
        bullet['y'] += bullet['vy']

        # 弾の描画更新
        if bullet['obj'] is None:  # 初めて弾を描画する場合
            bullet['obj'] = canvas.create_oval(bullet['x'] - bullet_size / 2, bullet['y'] - bullet_size / 2,
                                               bullet['x'] + bullet_size / 2, bullet['y'] + bullet_size / 2,
                                               fill='red')
        else:  # 既に描画された弾を移動
            canvas.coords(bullet['obj'], bullet['x'] - bullet_size / 2, bullet['y'] - bullet_size / 2,
                           bullet['x'] + bullet_size / 2, bullet['y'] + bullet_size / 2)

    # 画面外に出た弾を削除
    for bullet in bullets[:]:
        if bullet['x'] < 0 or bullet['x'] > WIDTH or bullet['y'] < 0 or bullet['y'] > HEIGHT:
            if bullet['obj']:  # 描画された弾を削除
                canvas.delete(bullet['obj'])
            bullets.remove(bullet)

# 衝突判定
def check_collision():
    player_coords = canvas.coords(player)
    for bullet in bullets:
        bullet_coords = canvas.coords(bullet['obj'])
        if (player_coords[2] > bullet_coords[0] and player_coords[0] < bullet_coords[2] and
                player_coords[3] > bullet_coords[1] and player_coords[1] < bullet_coords[3]):
            return True
    return False

# ゲーム終了後にメッセージを表示
def show_end_game_message(message):
    canvas.create_text(WIDTH // 2, HEIGHT // 2, text=message, fill='yellow', font=('Arial', 20))

# ゲームループ
def game_loop():
    global game_count

    # ゲーム開始から10秒経過したら次のゲームへ
    start_time = time.time()

    # 10秒ごとに新しい弾を発射
    if random.random() < 0.1:  # 10%の確率で弾を発射
        spawn_bullet()

    # 弾の移動
    move_bullets()

    # 衝突判定
    if check_collision():
        show_end_game_message("GAME OVER")  # ゲームオーバーのメッセージを表示
        root.after(1000, root.quit)  # 1秒後にゲームを終了

    # 10秒経過したら次のゲームへ
    if time.time() - start_time > game_duration:
        game_count += 1
        if game_count < 5:
            show_end_game_message(f"Game {game_count} Ended! Next Game Starts!")  # ゲーム終了メッセージ
            root.after(1000, game_loop)  # 次のゲーム開始
        else:
            show_end_game_message("おめでとう！ 5ゲームクリア！")  # 5ゲーム終了後のメッセージ
            root.after(1000, root.quit)  # 5ゲーム終了

    else:
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
