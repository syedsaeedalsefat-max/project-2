# Coaching Center Student Result Management System

A terminal-based Python application to manage student marks and generate performance reports.

---

## 📋 Prerequisites

Before running the project, ensure you have:
- **Python 3.8** or higher installed on your machine.
- **Git** (optional, for cloning the repository).

To check your Python version, run:
```bash
python --version
```

---

## ⚙️ Installation (Step-by-Step)

### Step 1: Clone or Download the Repository
Open your terminal (PowerShell, Command Prompt, or Bash) and clone the repository:
```bash
git clone https://github.com/syedsaeedalsefat-max/project-2.git
cd project-2
```

*(If you already have the folder downloaded, navigate directly to that directory in your terminal).*

---

### Step 2: (Recommended) Create and Activate a Virtual Environment

Creating an isolated virtual environment prevents conflicts with other Python packages on your system.

- **On Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

- **On Windows (Command Prompt - CMD):**
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate.bat
  ```

- **On macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

---

### Step 3: Install Dependencies (Optional)
The core application runs entirely on Python's built-in standard library with **zero external dependencies required**.

If you wish to use optional development tools, install dependencies via:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Application (Step-by-Step)

### Method 1: Run via Terminal (Standard)
With your terminal inside the project directory, execute:

- **Windows:**
  ```powershell
  python main.py
  ```

- **macOS / Linux:**
  ```bash
  python3 main.py
  ```

---

### Method 2: Script / One-Click Run
- **Windows:** Double-click the **`run.bat`** file in the project folder to start the application directly.
- **macOS / Linux:** Execute `./run.sh` in your terminal.

---

## 🎮 How to Use the Menu
Once the program starts, you will see a numbered terminal menu:

1. **`[1] Add New Student Record`**: Enter student ID, Name, and marks for 5 subjects (Mathematics, Physics, Chemistry, English, Computer Science).
2. **`[2] View All Enrolled Students`**: View a formatted directory table with options to sort by ID, Name, or Total Score.
3. **`[3] Search Student by ID`**: Look up an individual student and view their complete academic report card.
4. **`[4] View Highest and Lowest Scoring Students`**: Display the top performers (Rank 1) and lowest-scoring students.
5. **`[5] Generate Class Performance Summary`**: View pass rate, class average, subject-wise performance bars, and grade distribution.
6. **`[6] Update Student Marks`**: Modify marks for an existing student record.
7. **`[7] Delete Student Record`**: Remove a student record with confirmation.
8. **`[8] Save Records to CSV File`**: Explicitly save student records to `data/students.csv`.
9. **`[9] Reload Records from CSV File`**: Reload data from the CSV file.
10. **`[0] Exit Application`**: Automatically saves all changes and safely exits the program.

---

## 🧪 (Optional) How to Run Unit Tests
To run the automated test suite and verify all calculations:
```bash
python -m unittest discover -s tests -v
```
