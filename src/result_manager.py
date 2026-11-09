"""
result_manager.py - ResultManager Class Module for Coaching Center.
Manages student records, calculations, queries, statistical reporting, and CSV persistence.
"""

import csv
import os
from typing import Dict, List, Optional, Tuple, Any
from .student import Student


class ResultManager:
    """
    Manages collection of students, operations, summaries, and persistence.
    """

    DEFAULT_CSV_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "students.csv",
    )

    def __init__(self, csv_filepath: Optional[str] = None):
        """
        Initialize the ResultManager.

        Args:
            csv_filepath: Path to the CSV storage file. Defaults to data/students.csv.
        """
        self.csv_filepath = csv_filepath or self.DEFAULT_CSV_PATH
        self.students: Dict[str, Student] = {}
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.csv_filepath), exist_ok=True)
        # Attempt to auto-load on instantiation
        self.load_from_csv()

    # -------------------------------------------------------------------------
    # Core Student Management
    # -------------------------------------------------------------------------

    def add_student(self, student: Student) -> bool:
        """
        Add a new student to the manager.

        Args:
            student: Student instance to add.

        Returns:
            True if added successfully, False if student ID already exists.
        """
        if student.student_id in self.students:
            return False
        self.students[student.student_id] = student
        return True

    def search_student(self, student_id: str) -> Optional[Student]:
        """
        Search for a student using their unique ID (case-insensitive).

        Args:
            student_id: The ID string to search for.

        Returns:
            The matching Student instance, or None if not found.
        """
        clean_id = str(student_id).strip().upper()
        return self.students.get(clean_id)

    def delete_student(self, student_id: str) -> bool:
        """
        Remove a student by ID.

        Args:
            student_id: The ID of student to remove.

        Returns:
            True if removed, False if student did not exist.
        """
        clean_id = str(student_id).strip().upper()
        if clean_id in self.students:
            del self.students[clean_id]
            return True
        return False

    def update_student_marks(self, student_id: str, new_marks: Dict[str, float]) -> bool:
        """
        Update marks for an existing student and recalculate their metrics atomically.

        Args:
            student_id: The ID of student to update.
            new_marks: Dictionary of subject names to updated marks.

        Returns:
            True if updated, False if student not found.
        """
        student = self.search_student(student_id)
        if not student:
            return False

        # Phase 1: Validate all marks before mutating state (atomic update)
        validated: Dict[str, float] = {}
        for subj, score in new_marks.items():
            if subj in student.SUBJECTS:
                try:
                    val = float(score)
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid numeric mark for {subj}: {score}")
                if not (0.0 <= val <= student.MAX_MARKS_PER_SUBJECT):
                    raise ValueError(
                        f"Marks for {subj} must be between 0 and {student.MAX_MARKS_PER_SUBJECT}. Got: {val}"
                    )
                validated[subj] = round(val, 2)

        # Phase 2: Apply mutations and recalculate
        for subj, score in validated.items():
            student.marks[subj] = score
        student.recalculate()
        return True

    def get_all_students(self, sort_by: str = "id") -> List[Student]:
        """
        Return a list of all students.

        Args:
            sort_by: Sorting criterion ('id', 'name', 'total', 'percentage').

        Returns:
            Sorted list of Student objects.
        """
        student_list = list(self.students.values())
        criterion = str(sort_by).strip().lower()
        if criterion == "name":
            return sorted(student_list, key=lambda s: (s.name.lower(), s.student_id))
        elif criterion in ("total", "percentage"):
            return sorted(student_list, key=lambda s: (-s.total_marks, s.student_id))
        else:
            return sorted(student_list, key=lambda s: s.student_id)

    def count(self) -> int:
        """Return the total number of students enrolled."""
        return len(self.students)

    # -------------------------------------------------------------------------
    # Performance Analysis & Querying
    # -------------------------------------------------------------------------

    def get_highest_scoring_students(self) -> List[Student]:
        """
        Find and return the highest-scoring student(s) based on total marks.
        Returns a list to properly account for ties.
        """
        if not self.students:
            return []
        max_score = max(s.total_marks for s in self.students.values())
        return [s for s in self.students.values() if s.total_marks == max_score]

    def get_lowest_scoring_students(self) -> List[Student]:
        """
        Find and return the lowest-scoring student(s) based on total marks.
        Returns a list to properly account for ties.
        """
        if not self.students:
            return []
        min_score = min(s.total_marks for s in self.students.values())
        return [s for s in self.students.values() if s.total_marks == min_score]

    def generate_class_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive class performance statistics.

        Returns:
            Dictionary containing overall metrics, pass rates, grade distribution,
            subject averages, and top/lowest performers.
        """
        total_students = len(self.students)
        if total_students == 0:
            return {
                "total_students": 0,
                "passed_count": 0,
                "failed_count": 0,
                "pass_percentage": 0.0,
                "class_average_total": 0.0,
                "class_average_percentage": 0.0,
                "highest_scorers": [],
                "lowest_scorers": [],
                "subject_averages": {},
                "grade_distribution": {},
            }

        students_list = list(self.students.values())
        passed_students = [s for s in students_list if s.status == "PASS"]
        failed_students = [s for s in students_list if s.status == "FAIL"]

        passed_count = len(passed_students)
        failed_count = len(failed_students)
        pass_percentage = round((passed_count / total_students) * 100.0, 2)

        total_marks_all = sum(s.total_marks for s in students_list)
        class_avg_total = round(total_marks_all / total_students, 2)
        class_avg_pct = round(sum(s.percentage for s in students_list) / total_students, 2)

        # Subject-wise average marks
        subject_averages = {}
        for subj in Student.SUBJECTS:
            subj_total = sum(s.marks.get(subj, 0.0) for s in students_list)
            subject_averages[subj] = round(subj_total / total_students, 2)

        # Grade distribution breakdown
        grades = ["A+", "A", "B", "C", "D", "F"]
        grade_distribution = {g: 0 for g in grades}
        for s in students_list:
            if s.grade in grade_distribution:
                grade_distribution[s.grade] += 1
            else:
                grade_distribution[s.grade] = 1

        highest_scorers = self.get_highest_scoring_students()
        lowest_scorers = self.get_lowest_scoring_students()

        return {
            "total_students": total_students,
            "passed_count": passed_count,
            "failed_count": failed_count,
            "pass_percentage": pass_percentage,
            "class_average_total": class_avg_total,
            "class_average_percentage": class_avg_pct,
            "highest_scorers": highest_scorers,
            "lowest_scorers": lowest_scorers,
            "subject_averages": subject_averages,
            "grade_distribution": grade_distribution,
        }

    # -------------------------------------------------------------------------
    # CSV Persistence (Bonus Challenge)
    # -------------------------------------------------------------------------

    def get_csv_headers(self) -> List[str]:
        """Return the column headers for the CSV file."""
        headers = ["ID", "Name"]
        headers.extend(Student.SUBJECTS)
        headers.extend(["Total", "Average", "Percentage", "Grade", "Status"])
        return headers

    def save_to_csv(self, filepath: Optional[str] = None) -> Tuple[bool, str]:
        """
        Save all student records to a CSV file.

        Args:
            filepath: Target file path. Defaults to configured self.csv_filepath.

        Returns:
            Tuple of (success: bool, message: str).
        """
        target_path = filepath or self.csv_filepath
        try:
            os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
            with open(target_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.get_csv_headers())
                writer.writeheader()
                for student in self.get_all_students(sort_by="id"):
                    writer.writerow(student.to_dict())
            return True, f"Successfully saved {len(self.students)} student record(s) to '{target_path}'."
        except Exception as e:
            return False, f"Failed to save to CSV: {str(e)}"

    def load_from_csv(self, filepath: Optional[str] = None, clear_existing: bool = True) -> Tuple[bool, str]:
        """
        Load student records from CSV file into memory.

        Args:
            filepath: Source file path. Defaults to configured self.csv_filepath.
            clear_existing: Whether to clear existing records before loading (default True).

        Returns:
            Tuple of (success: bool, message: str).
        """
        target_path = filepath or self.csv_filepath
        if not os.path.exists(target_path):
            return False, f"CSV file not found at '{target_path}' (will be created on save)."

        try:
            loaded_students: Dict[str, Student] = {}
            loaded_count = 0
            with open(target_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    raw_id = row.get("ID")
                    if not raw_id or not str(raw_id).strip():
                        continue
                    student = Student.from_dict(row)
                    loaded_students[student.student_id] = student
                    loaded_count += 1

            if clear_existing:
                self.students = loaded_students
            else:
                self.students.update(loaded_students)

            return True, f"Successfully loaded {loaded_count} student record(s) from '{target_path}'."
        except Exception as e:
            return False, f"Failed to load from CSV: {str(e)}"

