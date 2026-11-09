"""
generate_screenshots.py - Automatically generates high-definition terminal screenshots
for the project documentation and README.md.
"""

import os
import re
from PIL import Image, ImageDraw, ImageFont

# Ensure screenshots directory exists
SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Theme configuration (Modern VS Code / macOS dark terminal)
BG_COLOR = (30, 30, 30)         # #1E1E1E
HEADER_COLOR = (45, 45, 45)     # #2D2D2D
TEXT_COLOR = (220, 220, 220)     # Default off-white
CYAN = (86, 156, 214)           # Light Blue / Cyan
GREEN = (78, 201, 176)          # Mint / Green
YELLOW = (220, 220, 170)        # Warm Yellow
RED = (244, 71, 71)             # Soft Red
GRAY = (128, 128, 128)          # Gray
WHITE = (255, 255, 255)         # Pure White
BORDER_COLOR = (60, 60, 60)

FONT_SIZE = 15
LINE_HEIGHT = 22
PADDING_X = 24
PADDING_Y = 20
HEADER_HEIGHT = 38


def get_font():
    """Attempt to load a crisp monospace font cross-platform, falling back to default."""
    font_paths = [
        # Windows
        "C:\\Windows\\Fonts\\consola.ttf",   # Consolas
        "C:\\Windows\\Fonts\\lucon.ttf",     # Lucida Console
        "C:\\Windows\\Fonts\\cour.ttf",      # Courier New
        # macOS
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Monaco.ttf",
        "/Library/Fonts/Courier New.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, FONT_SIZE)
            except Exception:
                pass
    return ImageFont.load_default()


def render_terminal_window(title: str, text_lines: list, output_filename: str):
    """Render a realistic terminal window image with title bar and contents."""
    font = get_font()

    # Determine dimensions
    max_line_len = max((len(re.sub(r'\x1b\[[0-9;]*m', '', line)) for line in text_lines), default=60)
    width = max(860, max_line_len * 9 + PADDING_X * 2)
    height = HEADER_HEIGHT + (len(text_lines) * LINE_HEIGHT) + (PADDING_Y * 2)

    image = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(image)

    # Draw header bar
    draw.rectangle([(0, 0), (width, HEADER_HEIGHT)], fill=HEADER_COLOR)
    draw.line([(0, HEADER_HEIGHT), (width, HEADER_HEIGHT)], fill=BORDER_COLOR, width=1)

    # Window control dots (macOS style)
    draw.ellipse([(14, 13), (26, 25)], fill=(255, 95, 86))   # Close
    draw.ellipse([(34, 13), (46, 25)], fill=(255, 189, 46))  # Minimize
    draw.ellipse([(54, 13), (66, 25)], fill=(39, 201, 63))   # Zoom

    # Terminal Title
    title_text = f"Coaching Center CLI - {title}"
    draw.text((width // 2 - (len(title_text) * 4), 11), title_text, fill=GRAY, font=font)

    # Render lines with contextual syntax coloring
    curr_y = HEADER_HEIGHT + PADDING_Y

    for line in text_lines:
        clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
        color = TEXT_COLOR

        if "=" * 20 in clean_line:
            color = CYAN
        elif "--- " in clean_line or "---" in clean_line:
            color = YELLOW
        elif "[OK]" in clean_line or "PASS" in clean_line or "HIGHEST" in clean_line or "Rank 1" in clean_line:
            color = GREEN
        elif "[ERROR]" in clean_line or "FAIL" in clean_line or "LOWEST" in clean_line or "Failed" in clean_line:
            color = RED
        elif "[1]" in clean_line or "[2]" in clean_line or "[3]" in clean_line or "[4]" in clean_line or "[5]" in clean_line or "[6]" in clean_line or "[7]" in clean_line or "[8]" in clean_line or "[9]" in clean_line or "[0]" in clean_line:
            color = WHITE
        elif "Active Records" in clean_line or "Subject-Wise" in clean_line or "Grade Distribution" in clean_line:
            color = YELLOW
        elif clean_line.startswith(" Total records") or clean_line.startswith(" Total Enrolled"):
            color = CYAN

        draw.text((PADDING_X, curr_y), clean_line, fill=color, font=font)
        curr_y += LINE_HEIGHT

    out_path = os.path.join(SCREENSHOTS_DIR, output_filename)
    image.save(out_path, "PNG")
    print(f"Generated screenshot: {out_path}")


def generate_all_screenshots():
    # 1. Main Menu
    menu_lines = [
        "====================================================================",
        "   COACHING CENTER RESULT & PERFORMANCE MANAGEMENT SYSTEM",
        "   Active Records: 7 student(s) | Storage: CSV Persistent",
        "====================================================================",
        " [1] Add New Student Record",
        " [2] View All Enrolled Students",
        " [3] Search Student by ID (Report Card)",
        " [4] View Highest and Lowest Scoring Students",
        " [5] Generate Class Performance Summary",
        " [6] Update Student Marks",
        " [7] Delete Student Record",
        " [8] Save Records to CSV File",
        " [9] Reload Records from CSV File",
        " [0] Exit Application",
        "====================================================================",
        "Select an option (0-9): 2",
    ]
    render_terminal_window("Main Menu", menu_lines, "01_main_menu.png")

    # 2. View All Students
    view_lines = [
        "========================================================================",
        "                      ENROLLED STUDENTS DIRECTORY                       ",
        "                      Complete performance breakdown                    ",
        "========================================================================",
        "----------------------------------------------------------------------------------------",
        " #   ID       Name               Math  Phys  Chem  Eng   CS    Total    Pct     Grd  Status",
        "----------------------------------------------------------------------------------------",
        " 1   STU101   Amina Rahman        95    92    88    91    96    462.0   92.4%   A+   PASS ",
        " 2   STU102   Tariqul Islam       82    85    79    76    88    410.0   82.0%   A    PASS ",
        " 3   STU103   Farhana Yasmin      74    68    72    81    75    370.0   74.0%   B    PASS ",
        " 4   STU104   Nafis Iqbal         62    58    65    60    65    310.0   62.0%   C    PASS ",
        " 5   STU105   Sadia Chowdhury     52    50    55    48    55    260.0   52.0%   D    PASS ",
        " 6   STU106   Rohan Ahmed         78    34    82    70    80    344.0   68.8%   C    FAIL ",
        " 7   STU107   Mahmud Hasan        35    32    42    38    45    192.0   38.4%   F    FAIL ",
        "----------------------------------------------------------------------------------------",
        " Total records displayed: 7",
        "",
        "Press Enter to return to menu...",
    ]
    render_terminal_window("Enrolled Students Directory", view_lines, "02_view_all_students.png")

    # 3. Search Student Report Card
    search_lines = [
        "========================================================================",
        "                          SEARCH STUDENT BY ID                          ",
        "                 Retrieve individual report card and results            ",
        "========================================================================",
        "Enter Student ID to search: STU101",
        "[OK] Found record for ID: STU101",
        "",
        "============================================================",
        "    EXCELLENCE COACHING CENTER - STUDENT REPORT CARD        ",
        "============================================================",
        " Student ID : STU101             Student Name : Amina Rahman",
        "------------------------------------------------------------",
        " Subject                      Max Marks    Marks Obtained   ",
        "------------------------------------------------------------",
        " Mathematics                  100           95.00  (P)      ",
        " Physics                      100           92.00  (P)      ",
        " Chemistry                    100           88.00  (P)      ",
        " English                      100           91.00  (P)      ",
        " Computer Science             100           96.00  (P)      ",
        "------------------------------------------------------------",
        " Total Marks : 462.00 / 500",
        " Average     :  92.40",
        " Percentage  :  92.40%",
        " Grade       : A+    | Final Status : [PASS]",
        " * Congratulations! Promoted to next level.",
        "============================================================",
        "",
        "Press Enter to return to menu...",
    ]
    render_terminal_window("Student Search & Report Card", search_lines, "03_search_student_report.png")

    # 4. Highest and Lowest Scorers
    high_low_lines = [
        "========================================================================",
        "                     CLASS TOPPERS & LOWEST SCORERS                     ",
        "                       Extreme performance analysis                     ",
        "========================================================================",
        "",
        "============================================================",
        " HIGHEST-SCORING STUDENT(S) (Rank 1)",
        "============================================================",
        " [Rank 1.1] ID: STU101 | Name: Amina Rahman        ",
        "   Total: 462.0/500 (92.4%) | Grade: A+ | Status: PASS",
        "   Subject Breakdown: {'Math': 95.0, 'Phys': 92.0, 'Chem': 88.0, 'Eng': 91.0, 'CS': 96.0}",
        "",
        "============================================================",
        " LOWEST-SCORING STUDENT(S)",
        "============================================================",
        " [Record 1] ID: STU107 | Name: Mahmud Hasan        ",
        "   Total: 192.0/500 (38.4%) | Grade: F | Status: FAIL",
        "   Subject Breakdown: {'Math': 35.0, 'Phys': 32.0, 'Chem': 42.0, 'Eng': 38.0, 'CS': 45.0}",
        "   Needs remediation in: Mathematics, Physics, English",
        "",
        "Press Enter to return to menu...",
    ]
    render_terminal_window("Toppers & Lowest Scorers", high_low_lines, "04_high_low_scorers.png")

    # 5. Class Performance Summary
    summary_lines = [
        "========================================================================",
        "                       CLASS PERFORMANCE SUMMARY                        ",
        "                Aggregate statistics and academic metrics               ",
        "========================================================================",
        "=================================================================",
        " Total Enrolled Students : 7",
        " Total Passed            : 5 (71.43%)",
        " Total Failed            : 2 (28.57%)",
        " Class Average Total     : 335.43 / 500",
        " Class Average Percentage: 67.09%",
        "-----------------------------------------------------------------",
        "--- Subject-Wise Average Performance: ---",
        "   Mathematics        : 68.29/100  |###########################             |",
        "   Physics            : 59.86/100  |#######################                 |",
        "   Chemistry          : 69.00/100  |###########################             |",
        "   English            : 66.29/100  |##########################              |",
        "   Computer Science   : 73.43/100  |#############################           |",
        "-----------------------------------------------------------------",
        "--- Grade Distribution Breakdown: ---",
        "   Grade A+  :  1 student(s) ( 14.3%)  [*]",
        "   Grade A   :  1 student(s) ( 14.3%)  [*]",
        "   Grade B   :  1 student(s) ( 14.3%)  [*]",
        "   Grade C   :  2 student(s) ( 28.6%)  [**]",
        "   Grade D   :  1 student(s) ( 14.3%)  [*]",
        "   Grade F   :  1 student(s) ( 14.3%)  [*]",
        "-----------------------------------------------------------------",
        " Top Performer(s)   : Amina Rahman (462.0)",
        " Lowest Performer(s): Mahmud Hasan (192.0)",
        "=================================================================",
        "",
        "Press Enter to return to menu...",
    ]
    render_terminal_window("Class Performance Summary", summary_lines, "05_class_summary.png")

    # 6. Add Student Record Flow
    add_lines = [
        "========================================================================",
        "                         ADD NEW STUDENT RECORD                         ",
        "               Enter student credentials and 5-subject marks            ",
        "========================================================================",
        "Enter Student ID (e.g. STU101): STU108",
        "Enter Student Full Name: Zubaida Karim",
        "",
        "--- Enter Marks Obtained (0.0 to 100.0) for 5 Core Subjects ---",
        "  -> Mathematics (0-100): 88.5",
        "  -> Physics (0-100): 91.0",
        "  -> Chemistry (0-100): 84.0",
        "  -> English (0-100): 89.0",
        "  -> Computer Science (0-100): 93.5",
        "",
        "[OK] Student 'Zubaida Karim' (ID: STU108) enrolled successfully!",
        "",
        "============================================================",
        "    EXCELLENCE COACHING CENTER - STUDENT REPORT CARD        ",
        "============================================================",
        " Student ID : STU108             Student Name : Zubaida Karim",
        "------------------------------------------------------------",
        " Total Marks : 446.00 / 500",
        " Average     :  89.20",
        " Percentage  :  89.20%",
        " Grade       : A     | Final Status : [PASS]",
        "============================================================",
        "",
        "Press Enter to return to menu...",
    ]
    render_terminal_window("Add Student Record", add_lines, "06_add_student.png")


if __name__ == "__main__":
    generate_all_screenshots()

