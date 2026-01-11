import tkinter as tk
from tkinter import messagebox
import random
import time
import os
import sys

try:
    import pygame
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    SOUND_ENABLED = True
    print("Mixer init OK")
except Exception as e:
    SOUND_ENABLED = False
    print("Mixer init FAILED:", e)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

SIZE = 9

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        self.mode = None
        self.level = None
        self.max_hints = 0
        self.hints_used = 0
        self.start_time = None
        self.score = 0
        self.history = []
        self.bg_music_playing = False
        self.cells = [[None] * SIZE for _ in range(SIZE)]
        self.initial_board = [[0] * SIZE for _ in range(SIZE)]
        self.current_board = [[0] * SIZE for _ in range(SIZE)]
        self.solution = [[0] * SIZE for _ in range(SIZE)]

        # THÊM: Theo dõi ô nào do người chơi tự điền (không bị Hint sửa)
        self.player_filled = [[False for _ in range(SIZE)] for _ in range(SIZE)]

        # 10 puzzle cố định đầy đủ
        self.challenge_puzzles = [
            ([[5,3,4,0,7,0,0,0,0],[6,0,2,1,9,5,3,0,8],[0,9,8,0,0,2,0,6,0],[8,0,9,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]],
             [[5,3,4,6,7,8,9,1,2],[6,7,2,1,9,5,3,4,8],[1,9,8,3,4,2,5,6,7],[8,5,9,7,6,1,4,2,3],[4,2,6,8,5,3,7,9,1],[7,1,3,9,2,4,8,5,6],[9,6,1,5,3,7,2,8,4],[2,8,7,4,1,9,6,3,5],[3,4,5,2,8,6,1,7,9]]),
            ([[0,0,0,6,0,0,4,0,0],[7,0,0,0,0,3,6,0,0],[0,0,0,0,9,1,0,8,0],[0,0,0,0,0,0,0,0,0],[0,0,0,5,0,8,0,0,0],[0,0,0,0,0,0,0,0,0],[0,4,0,2,7,0,0,0,0],[0,0,5,0,0,0,0,0,9],[0,0,8,0,0,4,0,0,0]],
             [[1,2,3,6,8,7,4,9,5],[7,8,4,9,5,3,6,2,1],[5,6,9,4,2,1,3,8,7],[2,3,1,8,4,9,5,7,6],[4,9,6,5,1,8,7,3,2],[8,5,7,3,6,2,9,1,4],[9,4,2,1,7,5,8,6,3],[3,1,5,7,6,2,4,8,9],[6,7,8,9,3,4,1,5,2]]),
            ([[4,0,0,0,0,0,0,0,3],[0,0,0,7,0,0,0,0,0],[0,6,0,0,9,0,0,1,0],[0,5,0,0,0,0,4,0,0],[0,0,8,0,0,0,2,0,0],[0,0,3,0,0,0,0,6,0],[0,1,0,0,4,0,0,5,0],[0,0,0,0,0,6,0,0,0],[2,0,0,0,0,0,0,0,8]],
             [[4,8,1,9,5,6,7,2,3],[5,3,9,7,8,2,4,1,6],[7,6,2,4,9,3,8,5,1],[9,5,7,8,6,1,4,3,2],[1,4,8,3,7,5,2,9,6],[6,2,3,1,4,9,5,8,7],[8,1,6,2,4,7,3,5,9],[3,7,5,9,1,6,8,4,2],[2,9,4,5,3,8,6,7,1]]),
            ([[0,0,0,2,6,0,7,0,1],[6,8,0,0,7,0,0,9,0],[1,9,0,0,0,4,5,0,0],[8,2,0,1,0,0,0,4,0],[0,0,4,6,0,2,9,0,0],[0,5,0,0,0,3,0,2,8],[0,0,9,3,0,0,0,7,4],[0,4,0,0,5,0,0,3,6],[7,0,3,0,1,8,0,0,0]],
             [[4,3,5,2,6,9,7,8,1],[6,8,2,5,7,1,4,9,3],[1,9,7,8,3,4,5,6,2],[8,2,6,1,9,5,3,4,7],[3,7,4,6,8,2,9,1,5],[9,5,1,7,4,3,6,2,8],[5,1,9,3,2,6,8,7,4],[2,4,8,9,5,7,1,3,6],[7,6,3,4,1,8,2,5,9]]),
            ([[0,2,0,6,0,8,0,0,0],[5,8,0,0,0,9,7,0,0],[0,0,0,0,4,0,0,0,0],[3,7,0,0,0,0,5,0,0],[6,0,0,0,0,0,0,0,4],[0,0,8,0,0,0,0,1,3],[0,0,0,0,2,0,0,0,0],[0,0,9,8,0,0,0,3,6],[0,0,0,3,0,6,0,9,0]],
             [[1,2,3,6,7,8,9,4,5],[5,8,4,2,1,9,7,6,3],[9,6,7,5,4,3,1,8,2],[3,7,2,4,6,1,5,8,9],[6,9,1,7,8,5,3,2,4],[4,5,8,9,3,2,6,1,7],[8,3,6,1,2,4,9,5,7],[2,1,9,8,5,7,4,3,6],[7,4,5,3,9,6,2,9,1]]),
            ([[0,0,7,0,0,0,0,1,2],[0,0,0,1,0,7,0,0,3],[8,0,1,0,9,4,0,0,0],[0,5,0,0,0,0,0,0,0],[0,0,0,5,3,8,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,7,0,0,2,0,0],[0,0,0,0,0,0,0,0,0],[3,4,0,0,0,0,0,0,0]],
             [[9,3,7,8,6,5,4,1,2],[4,6,5,1,2,7,8,9,3],[8,2,1,3,9,4,6,5,7],[1,5,3,9,4,2,7,8,6],[2,9,4,5,3,8,1,7,5],[6,7,8,4,1,9,3,2,4],[5,1,9,7,8,6,2,3,4],[7,8,2,6,5,3,9,4,1],[3,4,6,2,7,1,5,8,9]]),
            ([[0,0,0,0,0,0,2,0,0],[0,8,0,0,0,7,0,9,0],[6,0,2,0,0,0,5,0,0],[0,7,0,0,6,0,0,0,0],[0,0,0,9,0,1,0,0,0],[0,0,0,0,2,0,0,4,0],[0,0,5,0,0,0,6,0,3],[0,9,0,4,0,0,0,7,0],[0,0,6,0,0,0,0,0,0]],
             [[9,5,7,6,1,3,2,8,4],[4,8,3,2,5,7,1,9,6],[6,1,2,8,4,9,5,3,7],[1,7,8,3,6,4,9,5,2],[5,2,4,9,7,1,3,6,8],[3,6,9,5,2,8,7,4,1],[8,4,5,7,9,2,6,1,3],[2,9,1,4,3,6,8,7,5],[7,3,6,1,8,5,4,2,9]]),
            ([[1,0,0,0,0,7,0,9,0],[0,3,0,0,2,0,0,0,8],[0,0,9,6,0,0,5,0,0],[0,0,5,3,0,0,9,0,0],[0,1,0,0,8,0,0,0,2],[6,0,0,0,0,4,0,0,0],[3,0,0,0,0,0,0,1,0],[0,4,0,0,0,0,0,0,7],[0,0,7,0,0,0,3,0,0]],
             [[1,6,2,8,5,7,4,9,3],[5,3,4,1,2,9,6,7,8],[7,8,9,6,4,3,5,2,1],[4,7,5,3,1,2,9,8,6],[9,1,3,5,8,6,7,4,2],[6,2,8,9,7,4,1,3,5],[3,5,6,4,9,8,2,1,7],[2,4,1,7,3,5,8,6,9],[8,9,7,2,6,1,3,5,4]]),
            ([[0,0,0,2,0,0,0,6,3],[3,0,0,0,0,5,4,0,1],[0,0,1,0,0,3,9,8,0],[0,0,0,0,0,0,0,9,0],[0,0,0,5,3,8,0,0,0],[0,3,0,0,0,0,0,0,0],[0,2,6,3,0,0,5,0,0],[5,0,3,7,0,0,0,0,8],[4,7,0,0,0,1,0,0,0]],
             [[8,5,4,2,1,9,7,6,3],[3,9,7,8,6,5,4,2,1],[2,6,1,4,7,3,9,8,5],[7,8,5,1,4,2,3,9,6],[6,4,9,5,3,8,1,7,2],[1,3,2,9,5,7,8,4,6],[9,2,6,3,8,4,5,1,7],[5,1,3,7,9,6,2,4,8],[4,7,8,6,2,1,9,3,5]]),
            ([[0,0,0,0,0,0,0,0,0],[0,0,0,3,0,5,0,0,0],[0,0,0,0,7,0,0,0,9],[0,0,0,0,0,0,4,0,0],[0,0,0,0,0,0,0,0,0],[0,0,6,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0],[0,0,0,6,0,1,0,0,0],[0,0,0,0,0,0,0,0,0]],
             [[5,1,9,8,4,7,6,2,3],[7,6,4,3,9,5,1,8,2],[2,8,3,1,7,6,5,4,9],[3,7,1,9,6,8,4,5,2],[4,9,8,5,2,3,7,1,6],[8,5,6,7,1,4,9,3,8],[1,3,5,4,8,9,2,6,7],[9,4,2,6,3,1,8,7,5],[6,2,7,5,4,8,3,9,1]])
        ]

        self.striped_icon = self.create_striped_circle()
        self.show_mode_selection()

        if SOUND_ENABLED:
            self.root.after(500, self.start_bg_music)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_bg_music(self):
        bg_file = "nhacnen.wav"
        print(f"Đang thử phát nhạc nền: {bg_file}")
        print(f"File tồn tại?: {os.path.exists(bg_file)}")
        print(f"Đường dẫn tuyệt đối: {os.path.abspath(bg_file)}")

        if not SOUND_ENABLED:
            print("Âm thanh bị tắt (pygame không import được)")
            return

        if not os.path.exists(bg_file):
            print("KHÔNG TÌM THẤY FILE NHẠC NỀN!")
            return

        try:
            pygame.mixer.music.load(bg_file)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
            self.bg_music_playing = True
            print("NHẠC NỀN ĐÃ BẮT ĐẦU PHÁT THÀNH CÔNG! 🎶")
        except Exception as e:
            print(f"Lỗi phát nhạc nền: {e}")

    def play_sound(self, filename):
        if SOUND_ENABLED and os.path.exists(filename):
            try:
                sound = pygame.mixer.Sound(filename)
                sound.set_volume(0.5)
                sound.play()
            except Exception as e:
                print(f"Lỗi phát âm thanh {filename}: {e}")

    def create_striped_circle(self):
        photo = tk.PhotoImage(width=40, height=40)
        for x in range(40):
            for y in range(40):
                if (x + y) % 10 < 5:
                    photo.put("#ffffff", (x, y))
                else:
                    photo.put("#4CAF50", (x, y))
        return photo

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_mode_selection(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="#e8f5e9")
        frame.pack(expand=True, pady=80)

        title = tk.Label(frame, text="🧩 SUDOKU GAME 🧩", font=("Helvetica", 40, "bold"), bg="#e8f5e9", fg="#2e7d32")
        title.pack(pady=40)

        subtitle = tk.Label(frame, text="Chọn chế độ chơi", font=("Arial", 22), bg="#e8f5e9", fg="#555")
        subtitle.pack(pady=10)

        btn_style = {"font": ("Arial", 18, "bold"), "width": 30, "height": 3, "relief": "raised", "bd": 6}

        tk.Button(frame, text="🏋️ Chế độ tập luyện", bg="#66bb6a", fg="white", **btn_style,
                  command=self.show_level_selection,
                  activebackground="#81c784").pack(pady=25)

        tk.Button(frame, text="⚔️ Chế độ thử thách", bg="#ff7043", fg="white", **btn_style,
                  command=lambda: self.start_game("thu_thach"),
                  activebackground="#ff8a65").pack(pady=15)

    def show_level_selection(self):
        self.clear_window()

        back_btn = tk.Button(self.root, text="← Quay lại", font=("Arial", 14, "bold"), bg="#ff5252", fg="white",
                             relief="raised", bd=4, command=self.show_mode_selection)
        back_btn.place(x=20, y=20)

        frame = tk.Frame(self.root, bg="#e8f5e9")
        frame.pack(expand=True, pady=80)

        tk.Label(frame, text="CHỌN ĐỘ KHÓ", font=("Helvetica", 32, "bold"),
                 bg="#e8f5e9", fg="#2e7d32").pack(pady=50)

        tk.Button(frame, text="🟢 Dễ", font=("Arial", 20, "bold"), width=20, height=2,
                  bg="#81c784", fg="white", command=lambda: self.start_game("tap_luyen", "de")).pack(pady=20)
        tk.Button(frame, text="🟡 Trung bình", font=("Arial", 20, "bold"), width=20, height=2,
                  bg="#ffb74d", fg="white", command=lambda: self.start_game("tap_luyen", "trung_binh")).pack(pady=20)
        tk.Button(frame, text="🔴 Khó", font=("Arial", 20, "bold"), width=20, height=2,
                  bg="#ef5350", fg="white", command=lambda: self.start_game("tap_luyen", "kho")).pack(pady=20)

    def start_game(self, mode, level=None):
        self.clear_window()
        self.mode = mode
        self.level = level

        if mode == "tap_luyen":
            self.max_hints = 999
        else:
            self.max_hints = 3
            self.start_time = time.time()
            self.score = 1000

        status_frame = tk.Frame(self.root, bg="#d0e8d1", height=70)
        status_frame.pack(fill="x", pady=(20, 10))
        status_frame.pack_propagate(False)

        tk.Label(status_frame, image=self.striped_icon, bg="#d0e8d1").pack(side="left", padx=40)

        if mode == "tap_luyen":
            if level == "de":
                text = "BẠN ĐANG Ở CHẾ ĐỘ DỄ"
            elif level == "trung_binh":
                text = "BẠN ĐANG Ở CHẾ ĐỘ TRUNG BÌNH"
            elif level == "kho":
                text = "BẠN ĐANG Ở CHẾ ĐỘ KHÓ"
            else:
                text = "BẠN ĐANG Ở CHẾ ĐỘ TẬP LUYỆN"
        else:
            text = "BẠN ĐANG Ở CHẾ ĐỘ THỬ THÁCH"

        tk.Label(status_frame, text=text, font=("Helvetica", 24, "bold"),
                 bg="#d0e8d1", fg="#2e7d32").pack(side="left", expand=True)

        back_btn = tk.Button(self.root, text="← Quay lại", font=("Arial", 16, "bold"), bg="#FF4444", fg="white",
                             width=12, height=2, command=lambda: [self.play_sound("click.wav"), self.confirm_back_to_menu()])
        back_btn.place(x=15, y=15)

        self.game_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.game_frame.pack(padx=20, pady=(10, 20))

        self.create_grid()
        self.create_buttons()
        self.create_status_bar()
        self.new_puzzle()

    def confirm_back_to_menu(self):
        if messagebox.askyesno("Quay lại", "Bạn có chắc muốn quay về menu?\nTiến độ chơi hiện tại sẽ bị mất!"):
            self.play_sound("click.wav")
            if self.mode == "tap_luyen":
                self.show_level_selection()
            else:
                self.show_mode_selection()

    def on_closing(self):
        if SOUND_ENABLED and self.bg_music_playing:
            pygame.mixer.music.stop()
        self.root.destroy()

    def create_grid(self):
        frame = tk.Frame(self.game_frame)
        frame.pack()

        for i in range(SIZE):
            for j in range(SIZE):
                bg = "#ffffff" if (i//3 + j//3) % 2 == 0 else "#f0f0f0"
                e = tk.Entry(frame, width=2, font=("Arial", 24, "bold"), justify="center",
                             bg=bg, relief="solid", bd=2, disabledbackground="#e0e0e0")
                e.grid(row=i, column=j, ipadx=5, ipady=5,
                       padx=(6 if j % 3 == 0 and j != 0 else 1),
                       pady=(6 if i % 3 == 0 and i != 0 else 1))
                e.bind("<KeyRelease>", self.on_key_release)
                self.cells[i][j] = e

    def create_buttons(self):
        f = tk.Frame(self.game_frame)
        f.pack(pady=15)

        buttons = [
            ("Giải", "#4CAF50", self.solve),
            ("Giải nhanh", "#2E7D32", self.solve_fast),
            ("Hint", "#2196F3", self.hint),
            ("Kiểm tra lỗi", "#f44336", self.check_errors),
            ("Undo", "#FF9800", self.undo),
            ("Clear", "#795548", self.clear_player_inputs),
            ("Mới", "#9C27B0", self.new_puzzle),
        ]

        for idx, (text, color, cmd) in enumerate(buttons):
            tk.Button(f, text=text, width=12, height=2, font=("Arial", 12, "bold"),
                      bg=color, fg="white", command=lambda c=cmd: [self.play_sound("click.wav"), c()],
                      relief="raised", bd=4).grid(row=0, column=idx, padx=8)

    def create_status_bar(self):
        self.status_label = tk.Label(self.game_frame, text="", font=("Arial", 14), bg="#f5f5f5")
        self.status_label.pack(pady=10)
        self.update_status()

    def update_status(self):
        if self.mode == "thu_thach" and self.start_time:
            elapsed = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed, 60)
            time_str = f"Thời gian: {mins:02d}:{secs:02d}"
            score_str = f" | Điểm: {self.score}"
        else:
            time_str = score_str = ""
        hint_str = f" | Hint còn: {self.max_hints - self.hints_used}"
        self.status_label.config(text=time_str + score_str + hint_str)
        self.root.after(1000, self.update_status)

    def new_puzzle(self):
        self.hints_used = 0
        if self.mode == "thu_thach":
            self.start_time = time.time()
            self.score = 1000
        self.history.clear()
        self.clear_colors()

        # Reset player_filled khi bắt đầu bảng mới
        self.player_filled = [[False for _ in range(SIZE)] for _ in range(SIZE)]

        if self.mode == "tap_luyen":
            puzzles = {
                "de": self.challenge_puzzles[:3],
                "trung_binh": self.challenge_puzzles[3:6],
                "kho": self.challenge_puzzles[6:],
            }
            puzzle = random.choice(puzzles[self.level])
        else:
            puzzle = random.choice(self.challenge_puzzles)

        self.initial_board = [row[:] for row in puzzle[0]]
        self.current_board = [row[:] for row in puzzle[0]]
        self.solution = [row[:] for row in puzzle[1]]

        self.update_board()

    def update_board(self):
        for i in range(SIZE):
            for j in range(SIZE):
                self.cells[i][j].config(state="normal")
                self.cells[i][j].delete(0, tk.END)
                if self.initial_board[i][j] != 0:
                    val = self.initial_board[i][j]
                    self.cells[i][j].insert(0, str(val))
                    self.cells[i][j].config(state="disabled", disabledforeground="black")
                else:
                    self.cells[i][j].config(fg="blue")
                self.current_board[i][j] = self.initial_board[i][j]

    def clear_colors(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.initial_board[i][j] == 0:
                    self.cells[i][j].config(fg="blue")
                else:
                    self.cells[i][j].config(fg="black")

    def is_safe(self, board, r, c, num):
        for x in range(SIZE):
            if board[r][x] == num or board[x][c] == num:
                return False
        sr, sc = r//3*3, c//3*3
        for i in range(3):
            for j in range(3):
                if board[sr+i][sc+j] == num:
                    return False
        return True

    def on_key_release(self, event):
        widget = event.widget
        try:
            r = widget.grid_info()["row"]
            c = widget.grid_info()["column"]
        except:
            return
        if self.initial_board[r][c] != 0:
            return

        text = widget.get().strip()
        if text == "":
            new_val = 0
            self.player_filled[r][c] = False  # Xóa → không còn tự điền
        elif text.isdigit() and len(text) == 1:
            new_val = int(text)
            self.player_filled[r][c] = True   # Người chơi tự điền
        else:
            widget.delete(0, tk.END)
            return

        old_val = self.current_board[r][c]
        if old_val != new_val:
            self.history.append((r, c, old_val))

        self.current_board[r][c] = new_val
        widget.config(fg="blue")

        if new_val != 0:
            if new_val == self.solution[r][c]:
                self.play_sound("correct.wav")
            else:
                self.play_sound("error.wav")

        if self.mode == "thu_thach" and new_val != 0 and new_val != self.solution[r][c]:
            self.score = max(0, self.score - 20)

        self.root.after(100, self.check_win)

    def undo(self):
        if not self.history:
            messagebox.showinfo("Undo", "Không có thao tác nào để hoàn tác!")
            return
        r, c, old_val = self.history.pop()
        self.cells[r][c].delete(0, tk.END)
        if old_val != 0:
            self.cells[r][c].insert(0, str(old_val))
            self.cells[r][c].config(fg="blue")
            self.player_filled[r][c] = True  # Vẫn là người chơi đã điền trước đó
        else:
            self.player_filled[r][c] = False
        self.current_board[r][c] = old_val
        self.root.after(100, self.check_win)

    def clear_player_inputs(self):
        if messagebox.askyesno("Xóa bảng", "Bạn có chắc muốn xóa hết các số bạn đã điền?\nCác ô cố định sẽ được giữ nguyên."):
            self.history.clear()
            for i in range(SIZE):
                for j in range(SIZE):
                    if self.initial_board[i][j] == 0:
                        self.cells[i][j].delete(0, tk.END)
                        self.cells[i][j].config(fg="blue")
                        self.current_board[i][j] = 0
                        self.player_filled[i][j] = False  # Reset trạng thái tự điền
            messagebox.showinfo("Đã xóa", "Tất cả số bạn điền đã được xóa!")
            self.root.after(100, self.check_win)

    def check_errors(self):
        self.clear_colors()
        board = [[0]*SIZE for _ in range(SIZE)]
        for i in range(SIZE):
            for j in range(SIZE):
                v = self.cells[i][j].get().strip()
                board[i][j] = int(v) if v.isdigit() else 0

        has_error = False
        for i in range(SIZE):
            for j in range(SIZE):
                val = board[i][j]
                if val != 0 and self.initial_board[i][j] == 0:
                    temp = board[i][j]
                    board[i][j] = 0
                    if not self.is_safe(board, i, j, val):
                        self.cells[i][j].config(fg="red")
                        has_error = True
                    board[i][j] = temp

        if not has_error:
            messagebox.showinfo("Kiểm tra", "Không có lỗi nào!")
        return has_error

    def hint(self):
        if self.hints_used >= self.max_hints:
            messagebox.showwarning("Hint", "Bạn đã hết lượt gợi ý!")
            return

        solution_board = [row[:] for row in self.initial_board]
        if not self.solve_fast_backtracking(solution_board):
            messagebox.showerror("Lỗi", "Không thể tìm lời giải cho bảng này!")
            return

        candidates_wrong = []
        candidates_empty = []

        for r in range(SIZE):
            for c in range(SIZE):
                if self.initial_board[r][c] != 0:
                    continue
                if self.player_filled[r][c]:  # Không sửa ô người chơi đã tự điền
                    continue

                current_val = self.cells[r][c].get().strip()

                if current_val == "":
                    candidates_empty.append((r, c))
                elif int(current_val) != solution_board[r][c]:
                    candidates_wrong.append((r, c))

        if candidates_wrong:
            target_r, target_c = random.choice(candidates_wrong)
        elif candidates_empty:
            target_r, target_c = random.choice(candidates_empty)
        else:
            messagebox.showinfo("Hint", "Không còn ô nào để gợi ý!\n"
                                        "Các ô bạn đã tự điền sẽ không bị thay đổi.")
            return

        correct_val = solution_board[target_r][target_c]

        self._clear_all_conflicts(target_r, target_c, correct_val)

        cell = self.cells[target_r][target_c]
        cell.config(state="normal")
        cell.delete(0, tk.END)
        cell.insert(0, str(correct_val))
        cell.config(fg="#9C27B0", font=("Arial", 24, "bold"))

        self.current_board[target_r][target_c] = correct_val
        self.player_filled[target_r][target_c] = False  # Hint điền → không tính là tự điền

        self.root.update_idletasks()

        self.hints_used += 1
        self.play_sound("correct.wav")
        self.root.after(100, self.check_win)

    def _clear_all_conflicts(self, r, c, val):
        s_val = str(val)
        for i in range(SIZE):
            if i != c and self.initial_board[r][i] == 0:
                if self.cells[r][i].get().strip() == s_val:
                    self.cells[r][i].delete(0, tk.END)
            if i != r and self.initial_board[i][c] == 0:
                if self.cells[i][c].get().strip() == s_val:
                    self.cells[i][c].delete(0, tk.END)

        sr, sc = (r // 3) * 3, (c // 3) * 3
        for i in range(3):
            for j in range(3):
                row, col = sr + i, sc + j
                if (row, col) != (r, c) and self.initial_board[row][col] == 0:
                    if self.cells[row][col].get().strip() == s_val:
                        self.cells[row][col].delete(0, tk.END)

    def solve(self):
        if self.check_errors():
            messagebox.showerror("Lỗi", "Có ô bị sai! Hãy sửa trước khi dùng tính năng giải.")
            return
        board = [row[:] for row in self.current_board]
        self.solve_visual(board)

    def solve_visual(self, board):
        # (giữ nguyên như cũ)
        best_r, best_c, best_count = None, None, 10
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] == 0:
                    count = sum(1 for num in range(1, 10) if self.is_safe(board, i, j, num))
                    if count < best_count:
                        best_count = count
                        best_r, best_c = i, j
                    if best_count == 0:
                        return False

        if best_r is None:
            self.check_win()
            return True

        r, c = best_r, best_c
        for num in range(1, 10):
            if self.is_safe(board, r, c, num):
                board[r][c] = num
                self.cells[r][c].delete(0, tk.END)
                self.cells[r][c].insert(0, str(num))
                self.cells[r][c].config(fg="green")
                self.root.update()
                self.root.after(30)

                if self.solve_visual(board):
                    return True

                board[r][c] = 0
                self.cells[r][c].delete(0, tk.END)
                self.cells[r][c].config(fg="blue")
                self.root.update()
                self.root.after(20)
        return False

    def solve_fast(self):
        if self.check_errors():
            messagebox.showerror("Lỗi", "Có ô bị sai! Hãy sửa trước khi giải.")
            return
        board = [row[:] for row in self.current_board]
        if self.solve_fast_backtracking(board):
            for i in range(SIZE):
                for j in range(SIZE):
                    val = board[i][j]
                    self.cells[i][j].delete(0, tk.END)
                    if val != 0:
                        self.cells[i][j].insert(0, str(val))
                        if self.initial_board[i][j] == 0:
                            self.cells[i][j].config(fg="green")
            self.check_win()

    def solve_fast_backtracking(self, board):
        best_r, best_c, best_count = None, None, 10
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] == 0:
                    count = sum(1 for num in range(1, 10) if self.is_safe(board, i, j, num))
                    if count < best_count:
                        best_count = count
                        best_r, best_c = i, j
                    if best_count == 0:
                        return False
        if best_r is None:
            return True
        r, c = best_r, best_c
        for num in range(1, 10):
            if self.is_safe(board, r, c, num):
                board[r][c] = num
                if self.solve_fast_backtracking(board):
                    return True
                board[r][c] = 0
        return False

    def check_win(self):
        for i in range(SIZE):
            for j in range(SIZE):
                v = self.cells[i][j].get().strip()
                if not v.isdigit() or int(v) != self.solution[i][j]:
                    return

        self.play_sound("win.wav")
        messagebox.showinfo("Chúc mừng!", "Bạn đã hoàn thành Sudoku!")
        self.new_puzzle()


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()