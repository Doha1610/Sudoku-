🧩 Sudoku Game (Python – Tkinter) 

- Sudoku game with a graphical user interface**, built using **Python and Tkinter**, featuring multiple game modes, smart hints, automatic solving, and sound effects 🎵. 

✨ Features

 🎮 Two game modes

  - Practice Mode: unlimited hints, relaxed gameplay 
  - Challenge Mode: limited hints, time tracking, and scoring system 
<img width="404" height="386" alt="image" src="https://github.com/user-attachments/assets/cc662489-c51e-445d-af1b-c41e580c35d0" />

🎚 Three difficulty levels 

  - Easy 
  - Medium 
  - Hard 
<img width="390" height="417" alt="image" src="https://github.com/user-attachments/assets/719a338e-59cc-44e9-9542-488f94eb84d1" />

 💡 Smart Hint system

  - Does not overwrite cells filled by the player 
  - Prioritizes correcting incorrect cells 

🧠 Sudoku Solver

  - Step-by-step visual solving 
  - Fast solve using backtracking 

🔍 Error Checking 

  - Detects invalid moves based on Sudoku rules 
  - Highlights incorrect cells in red 

 ↩ Undo 

  Revert previous player actions 

🧹 Clear Board

  Clears all player inputs while keeping fixed cells intact 

🎵 Sound Effects 

  Background music 
  Sounds for correct moves, errors, and winning 

 

🖥️ User Interface 

- Clean and user-friendly Tkinter GUI 
- Alternating colors for 3×3 sub-grids 
- Clear distinction between: 

-  Fixed cells (black) 
- Player-filled cells (blue) 
 - Hint / solver-filled cells (purple / green) 

 <img width="546" height="368" alt="image" src="https://github.com/user-attachments/assets/fb8bfcdc-1af9-4b65-ab8e-da977dd4bb91" />


📂 Project Structure 

```
Sudoku-/
│
├── main.py          # Main application
├── README.md        # Project documentation
├── nhacnen.wav      # Background music
├── click.wav        # Click sound
├── correct.wav      # Correct move sound
├── error.wav        # Error sound
├── win.wav          # Winning sound
```

---

⚙️ Requirements 

- Python 
- Libraries: 

  +`tkinter` (included with Python) 
  + `pygame` 

Install pygame:

```bash
pip install pygame
```

 

▶️ How to Run 

```bash
python main.py
```

---

🧩 Sudoku Data 

- Includes 10 fully valid Sudoku puzzles
- Each puzzle comes with its correct solution
- Puzzles are selected based on game mode and difficulty 
 
<img width="1362" height="940" alt="Screenshot 2025-12-30 002337" src="https://github.com/user-attachments/assets/d444fc0d-ddbd-42f2-9b04-333544fa082d" />

🧠 Algorithms Used 

- Backtracking
- MRV (Minimum Remaining Values) heuristic for faster solving 
- Constraint checking for rows, columns, and 3×3 sub-grids 

 


