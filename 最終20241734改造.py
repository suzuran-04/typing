import tkinter as tk

# ゲームのデータ
word_list = [
    ("私は偽物です", "watasihanisemonodesu"),
    ("あたなが本物です", "anatagahonmonodesu"),
    ("だから私の目をあげます", "dakarawatasinomewoagemasu"),
]

# ゲーム状態
current_word, romaji = word_list[0]
typed_romaji = ""
correct_indices = []

# タイピングゲーム開始のフラグ
typing_started = False

# RPGゲーム用のセリフ進行
def next_dialogue(event):
    global dialogue_index, typing_started
    if dialogue_index == 0:
        # セリフ1: "RPGゲームへようこそ"
        canvas.itemconfig(text_id, text="RPGゲームへようこそ")
        dialogue_index += 1  # 次のセリフに進む
    elif dialogue_index == 1:
        # セリフ2: "こんにちは"
        canvas.itemconfig(text_id, text="こんにちは")
        dialogue_index += 1
    elif dialogue_index == 2:
        # セリフ3: "元気ですか？"
        canvas.itemconfig(text_id, text="あなたにはこれからタイピングをしていただきます")
        dialogue_index += 1
    elif dialogue_index == 3:
        # セリフ4: "さようなら"
        canvas.itemconfig(text_id, text="さようなら")
        dialogue_index += 1
    else:
        canvas.itemconfig(text_id, text="ゲーム終了")
        dialogue_index = 0  # セリフの最初に戻る

    # セリフが全て表示された後、タイピングゲームを開始
    if dialogue_index == 4:
        start_typing_game()

# タイピングゲームを開始する
def start_typing_game():
    global typing_started
    if not typing_started:
        typing_started = True
        update_display()  # タイピングゲームの初期表示を更新
        root.bind("<Key>", on_key_press)  # キーイベントのバインディング

# 次の単語に進む関数
def next_word():
    global current_word, romaji, typed_romaji, correct_indices

    # 現在の単語が終わった場合、次の単語に進む
    current_word, romaji = word_list[(word_list.index((current_word, romaji)) + 1) % len(word_list)]
    typed_romaji = ""  # 入力をリセット
    correct_indices = []  # 正解部分もリセット
    update_display()  # 画面を更新

# ローマ字入力処理
def on_key_press(event):
    global typed_romaji, correct_indices, current_word, romaji

    key = event.char.lower()  # 小文字で処理
    if key.isalpha() and key == romaji[len(typed_romaji)].lower():  # 現在入力すべきローマ字と一致する場合のみ
        typed_romaji += key

        # ローマ字が一致している部分を緑色に変更
        if typed_romaji == romaji[:len(typed_romaji)]:
            correct_indices = list(range(len(typed_romaji)))
        else:
            correct_indices = []

        update_display()

        # タイピングが完了したら次の単語に進む
        if typed_romaji == romaji:
            next_word()

# 表示を更新する関数
def update_display():
    canvas.delete("all")  # 既存の描画をクリア

    # ひらがな部分を表示
    for i, char in enumerate(current_word):
        canvas.create_text(200 + i * 40, 100, text=char, font=("Times New Roman", 30), fill="white")

    # ローマ字部分を表示
    for i, char in enumerate(romaji):
        color = "gray"  # デフォルトの色
        if i < len(correct_indices):  # 正解部分
            color = "red"
        elif i == len(typed_romaji) and typed_romaji != romaji[:len(typed_romaji)]:  # 誤り部分
            color = "red"
        
        canvas.create_text(200 + i * 40, 150, text=char, font=("Times New Roman", 30), fill=color)

# 初期設定
root = tk.Tk()
root.title("RPGゲーム & ひらがなタイピング")

# キャンバス作成
canvas = tk.Canvas(root, width=1200, height=800, bg="black")
canvas.pack()

# 背景の設定（黒）
canvas.create_rectangle(0, 0, 1200, 800, fill="black", outline="black")

# 赤い丸の作成 (中央に配置、直径200)
circle_x1, circle_y1, circle_x2, circle_y2 = 500, 300, 700, 500
canvas.create_oval(circle_x1, circle_y1, circle_x2, circle_y2, fill="red", outline="red")

# 目のサイズと間隔を調整して、赤い円の中に中央に配置
eye_radius = 30  # 目の半径
eye_distance = 10  # 目と目の間隔

# 左目の位置
left_eye_center_x = (circle_x1 + circle_x2) / 2 - eye_distance - eye_radius
left_eye_center_y = (circle_y1 + circle_y2) / 2
canvas.create_oval(left_eye_center_x - eye_radius, left_eye_center_y - eye_radius,
                   left_eye_center_x + eye_radius, left_eye_center_y + eye_radius,
                   fill="white", outline="white")

# 右目の位置
right_eye_center_x = (circle_x1 + circle_x2) / 2 + eye_distance + eye_radius
right_eye_center_y = (circle_y1 + circle_y2) / 2
canvas.create_oval(right_eye_center_x - eye_radius, right_eye_center_y - eye_radius,
                   right_eye_center_x + eye_radius, right_eye_center_y + eye_radius,
                   fill="white", outline="white")

# 瞳の作成 (黒い瞳)
canvas.create_oval(left_eye_center_x - 20, left_eye_center_y - 20,
                   left_eye_center_x + 20, left_eye_center_y + 20, fill="black", outline="black")
canvas.create_oval(right_eye_center_x - 20, right_eye_center_y - 20,
                   right_eye_center_x + 20, right_eye_center_y + 20, fill="black", outline="black")

# 初期テキストを作成
text_id = canvas.create_text(600, 200, text="RPGゲームへようこそ", fill="white", font=("Times New Roman", 40))

# セリフを進めるためのカウンター
dialogue_index = 0

# キーイベントのバインディング
root.bind('<Return>', next_dialogue)

# メインループ
root.mainloop()
