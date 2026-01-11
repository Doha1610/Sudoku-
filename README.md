🧩 Sudoku Game (Python – Tkinter) 

- Sudoku game with a graphical user interface**, built using **Python and Tkinter**, featuring multiple game modes, smart hints, automatic solving, and sound effects 🎵. 

✨ Features

 🎮 Two game modes

  - Practice Mode: unlimited hints, relaxed gameplay 
  - Challenge Mode: limited hints, time tracking, and scoring system 

🎚 Three difficulty levels 

  - Easy 
  - Medium 
  - Hard 

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

- Python 3.8+ 
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
 

🧠 Algorithms Used 

- Backtracking
- MRV (Minimum Remaining Values) heuristic for faster solving 
- Constraint checking for rows, columns, and 3×3 sub-grids 

 


