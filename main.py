#!/usr/bin/env python3
"""
main.py - Coaching Center Student Result Management System
Terminal-based Menu-Driven Interface.
"""

import sys
import os
from typing import Dict

from src.student import Student
from src.result_manager import ResultManager
from src.utils import (
    Colors,
    clear_screen,
    print_banner,
    print_section,
    print_success,
    print_error,
    print_warning,
    print_info,
    pause,
    prompt_string,
    prompt_float,
    render_student_table,
)


def display_menu(manager: ResultManager) -> None:
    """Display the main navigation menu."""
    student_count = manager.count()
    print(f"{Colors.BLUE}{'=' * 68}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}   COACHING CENTER RESULT & PERFORMANCE MANAGEMENT SYSTEM{Colors.RESET}")
    print(f"{Colors.GRAY}   Active Records: {student_count} student(s) | Storage: CSV Persistent{Colors.RESET}")
    print(f"{Colors.BLUE}{'=' * 68}{Colors.RESET}")
    print(f"{Colors.WHITE}{Colors.BOLD} [1]{Colors.RESET} Add New Student Record")
    print(f"{Colors.WHITE}{Colors.BOLD} [2]{Colors.RESET} View All Enrolled Students")
    print(f"{Colors.WHITE}{Colors.BOLD} [3]{Colors.RESET} Search Student by ID (Report Card)")
    print(f"{Colors.WHITE}{Colors.BOLD} [4]{Colors.RESET} View Highest and Lowest Scoring Students")
    print(f"{Colors.WHITE}{Colors.BOLD} [5]{Colors.RESET} Generate Class Performance Summary")
    print(f"{Colors.WHITE}{Colors.BOLD} [6]{Colors.RESET} Update Student Marks")
    print(f"{Colors.WHITE}{Colors.BOLD} [7]{Colors.RESET} Delete Student Record")
    print(f"{Colors.WHITE}{Colors.BOLD} [8]{Colors.RESET} Save Records to CSV File")
    print(f"{Colors.WHITE}{Colors.BOLD} [9]{Colors.RESET} Reload Records from CSV File")
    print(f"{Colors.WHITE}{Colors.BOLD} [0]{Colors.RESET} Exit Application")
    print(f"{Colors.BLUE}{'=' * 68}{Colors.RESET}")


def handle_add_student(manager: ResultManager) -> None:
    """Handle adding a new student with ID, Name, and marks for 5 subjects."""
    print_banner("ADD NEW STUDENT RECORD", "Enter student credentials and 5-subject marks")

    student_id = prompt_string("Enter Student ID (e.g. STU101)").upper()
    if not student_id:
        return

    # Check for duplicate ID
    if manager.search_student(student_id):
        print_error(f"Student with ID '{student_id}' already exists! IDs must be unique.")
        pause()
        return

    name = prompt_string("Enter Student Full Name")
    if not name:
        return

    print_section("Enter Marks Obtained (0.0 to 100.0) for 5 Core Subjects")
    marks: Dict[str, float] = {}
    for subject in Student.SUBJECTS:
        score = prompt_float(f"  -> {subject}", min_val=0.0, max_val=100.0)
        if score is None:
            print_warning("Student enrollment cancelled.")
            pause()
            return
        marks[subject] = score

    try:
        new_student = Student(student_id=student_id, name=name, marks=marks)
        if manager.add_student(new_student):
            # Auto-save to CSV for persistence
            manager.save_to_csv()
            print_success(f"Student '{name}' (ID: {student_id}) enrolled successfully!")
            print(f"\n{new_student.generate_report_card()}")
        else:
            print_error(f"Failed to add student. ID '{student_id}' already exists.")
    except Exception as err:
        print_error(f"Failed to create student: {err}")

    pause()


def handle_view_all_students(manager: ResultManager) -> None:
    """Handle displaying all student records in tabular form with sorting."""
    print_banner("ENROLLED STUDENTS DIRECTORY", "Complete performance breakdown")

    if manager.count() == 0:
        print_warning("No student records found. Add students first or load CSV data.")
        pause()
        return

    print(f"{Colors.YELLOW}Sort by:{Colors.RESET} [1] ID  |  [2] Name  |  [3] Total Score / Rank")
    choice = prompt_string("Choose sorting option (1-3, default 1)", allow_empty=True)

    sort_criteria = "id"
    if choice == "2":
        sort_criteria = "name"
    elif choice == "3":
        sort_criteria = "total"

    students = manager.get_all_students(sort_by=sort_criteria)
    render_student_table(students)
    pause()


def handle_search_student(manager: ResultManager) -> None:
    """Handle searching for a single student by ID and printing report card."""
    print_banner("SEARCH STUDENT BY ID", "Retrieve individual report card and results")

    search_id = prompt_string("Enter Student ID to search").upper()
    if not search_id:
        return

    student = manager.search_student(search_id)
    if student:
        print_success(f"Found record for ID: {student.student_id}")
        print(f"\n{student.generate_report_card()}")
    else:
        print_error(f"No student record found matching ID '{search_id}'.")

    pause()


def handle_highest_lowest(manager: ResultManager) -> None:
    """Handle displaying the highest-scoring and lowest-scoring students."""
    print_banner("CLASS TOPPERS & LOWEST SCORERS", "Extreme performance analysis")

    if manager.count() == 0:
        print_warning("No student records available for analysis.")
        pause()
        return

    highest_scorers = manager.get_highest_scoring_students()
    lowest_scorers = manager.get_lowest_scoring_students()

    # Display Highest Scorers
    print(f"\n{Colors.GREEN}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD} HIGHEST-SCORING STUDENT(S) (Rank 1){Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    for idx, s in enumerate(highest_scorers, 1):
        print(
            f" [Rank 1.{idx}] ID: {s.student_id} | Name: {s.name:<20}\n"
            f"   Total: {s.total_marks}/500 ({s.percentage}%) | Grade: {s.grade} | Status: {s.status}"
        )
        print(f"   Subject Breakdown: {s.marks}")

    # Display Lowest Scorers
    print(f"\n{Colors.RED}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.RED}{Colors.BOLD} LOWEST-SCORING STUDENT(S){Colors.RESET}")
    print(f"{Colors.RED}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    for idx, s in enumerate(lowest_scorers, 1):
        print(
            f" [Record {idx}] ID: {s.student_id} | Name: {s.name:<20}\n"
            f"   Total: {s.total_marks}/500 ({s.percentage}%) | Grade: {s.grade} | Status: {s.status}"
        )
        print(f"   Subject Breakdown: {s.marks}")
        failed = s.get_failed_subjects()
        if failed:
            print(f"   {Colors.YELLOW}Needs remediation in: {', '.join(failed)}{Colors.RESET}")

    pause()


def handle_class_summary(manager: ResultManager) -> None:
    """Handle generating a complete statistical class performance report."""
    print_banner("CLASS PERFORMANCE SUMMARY", "Aggregate statistics and academic metrics")

    summary = manager.generate_class_summary()
    total = summary["total_students"]

    if total == 0:
        print_warning("No student records enrolled. Cannot generate class summary.")
        pause()
        return

    print(f"{Colors.CYAN}{'=' * 65}{Colors.RESET}")
    print(f" Total Enrolled Students : {total}")
    print(
        f" Total Passed            : {Colors.GREEN}{summary['passed_count']}{Colors.RESET} "
        f"({Colors.GREEN}{summary['pass_percentage']}%{Colors.RESET})"
    )
    print(
        f" Total Failed            : {Colors.RED}{summary['failed_count']}{Colors.RESET} "
        f"({Colors.RED}{round(100 - summary['pass_percentage'], 2)}%{Colors.RESET})"
    )
    print(f" Class Average Total     : {summary['class_average_total']} / 500")
    print(f" Class Average Percentage: {summary['class_average_percentage']}%")
    print(f"{Colors.CYAN}{'-' * 65}{Colors.RESET}")

    # Subject-wise Averages
    print(f"{Colors.YELLOW}{Colors.BOLD} Subject-Wise Average Performance:{Colors.RESET}")
    for subj, avg in summary["subject_averages"].items():
        bar_len = int(avg / 2.5)  # Scale to 40 chars max
        bar = "#" * bar_len
        print(f"   {subj:<18} : {avg:>5.2f}/100  |{bar:<40}|")

    print(f"{Colors.CYAN}{'-' * 65}{Colors.RESET}")

    # Grade Distribution Breakdown
    print(f"{Colors.YELLOW}{Colors.BOLD} Grade Distribution Breakdown:{Colors.RESET}")
    for grade, count in summary["grade_distribution"].items():
        pct = round((count / total) * 100, 1) if total > 0 else 0.0
        bar = "*" * count
        print(f"   Grade {grade:<3} : {count:>2} student(s) ({pct:>5.1f}%)  [{bar}]")

    print(f"{Colors.CYAN}{'-' * 65}{Colors.RESET}")

    # High / Low Summary
    high_names = ", ".join(f"{s.name} ({s.total_marks})" for s in summary["highest_scorers"])
    low_names = ", ".join(f"{s.name} ({s.total_marks})" for s in summary["lowest_scorers"])
    print(f" Top Performer(s)   : {Colors.GREEN}{high_names}{Colors.RESET}")
    print(f" Lowest Performer(s): {Colors.RED}{low_names}{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 65}{Colors.RESET}")

    pause()


def handle_update_marks(manager: ResultManager) -> None:
    """Handle updating marks for an existing student."""
    print_banner("UPDATE STUDENT MARKS", "Modify subject marks and recalculate results")

    search_id = prompt_string("Enter Student ID to update").upper()
    student = manager.search_student(search_id)
    if not student:
        print_error(f"Student with ID '{search_id}' not found.")
        pause()
        return

    print_info(f"Updating marks for: {student.name} (Current Total: {student.total_marks})")
    new_marks: Dict[str, float] = {}
    for subj in Student.SUBJECTS:
        current_score = student.marks.get(subj, 0.0)
        raw = prompt_string(f"New mark for {subj} [Current: {current_score}] (leave empty to keep)", allow_empty=True)
        if raw.strip() == "":
            new_marks[subj] = current_score
        else:
            try:
                score = float(raw)
                if 0 <= score <= 100:
                    new_marks[subj] = score
                else:
                    print_warning(f"Invalid range. Retaining current score {current_score}.")
                    new_marks[subj] = current_score
            except ValueError:
                print_warning(f"Invalid numeric input. Retaining current score {current_score}.")
                new_marks[subj] = current_score

    manager.update_student_marks(search_id, new_marks)
    manager.save_to_csv()
    print_success(f"Successfully updated marks for student '{student.name}'!")
    print(f"\n{student.generate_report_card()}")
    pause()


def handle_delete_student(manager: ResultManager) -> None:
    """Handle deleting a student record with confirmation."""
    print_banner("DELETE STUDENT RECORD", "Remove a student from the coaching center")

    search_id = prompt_string("Enter Student ID to delete").upper()
    student = manager.search_student(search_id)
    if not student:
        print_error(f"Student with ID '{search_id}' not found.")
        pause()
        return

    print_warning(f"Are you sure you want to permanently delete {student.name} (ID: {student.student_id})?")
    confirm = prompt_string("Type 'YES' to confirm deletion", allow_empty=True).upper()
    if confirm == "YES":
        manager.delete_student(search_id)
        manager.save_to_csv()
        print_success(f"Student '{student.name}' removed successfully.")
    else:
        print_info("Deletion cancelled.")

    pause()


def handle_save_csv(manager: ResultManager) -> None:
    """Handle explicit save to CSV file."""
    print_banner("EXPORT TO CSV", "Save records to persistent storage")
    ok, msg = manager.save_to_csv()
    if ok:
        print_success(msg)
    else:
        print_error(msg)
    pause()


def handle_reload_csv(manager: ResultManager) -> None:
    """Handle reloading data from CSV."""
    print_banner("RELOAD FROM CSV", "Refresh records from persistent file")
    ok, msg = manager.load_from_csv()
    if ok:
        print_success(msg)
    else:
        print_warning(msg)
    pause()


def main() -> None:
    """Main loop for the terminal application."""
    # Initialize the ResultManager (loads existing CSV if available)
    manager = ResultManager()

    while True:
        try:
            clear_screen()
            display_menu(manager)
            choice = prompt_string("Select an option (0-9)").strip()

            if choice == "1":
                handle_add_student(manager)
            elif choice == "2":
                handle_view_all_students(manager)
            elif choice == "3":
                handle_search_student(manager)
            elif choice == "4":
                handle_highest_lowest(manager)
            elif choice == "5":
                handle_class_summary(manager)
            elif choice == "6":
                handle_update_marks(manager)
            elif choice == "7":
                handle_delete_student(manager)
            elif choice == "8":
                handle_save_csv(manager)
            elif choice == "9":
                handle_reload_csv(manager)
            elif choice == "0":
                # Ensure data is saved on exit
                manager.save_to_csv()
                print(f"\n{Colors.GREEN}{Colors.BOLD}Thank you for using the Coaching Center Result System! Goodbye.{Colors.RESET}\n")
                sys.exit(0)
            elif choice == "":
                # User cancelled input prompt
                continue
            else:
                print_error("Invalid selection! Please enter a number between 0 and 9.")
                pause()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{Colors.YELLOW}Program interrupted by user. Exiting cleanly...{Colors.RESET}")
            manager.save_to_csv()
            sys.exit(0)
        except Exception as err:
            print_error(f"Unexpected error occurred: {err}")
            pause()


if __name__ == "__main__":
    main()

