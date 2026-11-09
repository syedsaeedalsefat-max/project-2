"""
student.py - Student Class Module for Coaching Center Result Management System.
Defines student data structure, performance calculations, and report formatting.
"""

from typing import Dict, Any


class Student:
    """
    Represents an individual student in the coaching center.
    
    Attributes:
        student_id (str): Unique identifier for the student.
        name (str): Full name of the student.
        marks (dict): Dictionary mapping subject names to marks obtained (0-100).
        total_marks (float): Sum of marks across all subjects.
        average_marks (float): Average score across all subjects.
        percentage (float): Percentage of total marks obtained.
        grade (str): Letter grade based on performance.
        status (str): Pass or Fail status.
    """

    # Standard subjects for the coaching center
    SUBJECTS = (
        "Mathematics",
        "Physics",
        "Chemistry",
        "English",
        "Computer Science",
    )
    PASS_MARK_PER_SUBJECT = 40.0
    PASS_PERCENTAGE_OVERALL = 40.0
    MAX_MARKS_PER_SUBJECT = 100.0

    def __init__(self, student_id: str, name: str, marks: Dict[str, float]):
        """
        Initialize a new Student instance and calculate academic performance metrics.

        Args:
            student_id: Unique string identifier.
            name: Student's name.
            marks: Dictionary with subject name as key and float marks (0-100) as value.
        """
        self.student_id = str(student_id).strip().upper()
        self.name = str(name).strip()
        if not self.student_id:
            raise ValueError("Student ID cannot be empty.")
        if not self.name:
            raise ValueError("Student name cannot be empty.")
        self.marks: Dict[str, float] = {}

        # Validate and store marks for the defined subjects
        for subject in self.SUBJECTS:
            raw_val = marks.get(subject, 0.0)
            try:
                val = float(raw_val)
            except (ValueError, TypeError):
                raise ValueError(
                    f"Marks for {subject} must be a valid number. Got: {raw_val}"
                )
            if val < 0.0 or val > self.MAX_MARKS_PER_SUBJECT:
                raise ValueError(
                    f"Marks for {subject} must be between 0 and {self.MAX_MARKS_PER_SUBJECT}. Got: {val}"
                )
            self.marks[subject] = round(val, 2)

        # Performance metrics
        self.total_marks = self.calculate_total()
        self.average_marks = self.calculate_average()
        self.percentage = self.calculate_percentage()
        self.grade = self.calculate_grade()
        self.status = self.calculate_status()

    def recalculate(self) -> None:
        """Recalculate performance metrics whenever marks are updated."""
        self.total_marks = self.calculate_total()
        self.average_marks = self.calculate_average()
        self.percentage = self.calculate_percentage()
        self.grade = self.calculate_grade()
        self.status = self.calculate_status()

    def calculate_total(self) -> float:
        """Calculate and return the sum of all 5 subject marks."""
        return round(sum(self.marks.values()), 2)

    def calculate_average(self) -> float:
        """Calculate and return the average score across 5 subjects."""
        if not self.marks:
            return 0.0
        return round(self.total_marks / len(self.SUBJECTS), 2)

    def calculate_percentage(self) -> float:
        """
        Calculate and return percentage based on maximum possible marks (500).
        Percentage = (Total Marks / 500) * 100
        """
        total_possible = len(self.SUBJECTS) * self.MAX_MARKS_PER_SUBJECT
        if total_possible == 0:
            return 0.0
        return round((self.total_marks / total_possible) * 100.0, 2)

    def calculate_grade(self) -> str:
        """
        Determine academic grade based on percentage:
            >= 90%: A+ (Outstanding)
            >= 80%: A  (Excellent)
            >= 70%: B  (Good)
            >= 60%: C  (Average)
            >= 50%: D  (Below Average)
            <  50%: F  (Fail / Needs Improvement)
        """
        pct = self.percentage
        if pct >= 90.0:
            return "A+"
        elif pct >= 80.0:
            return "A"
        elif pct >= 70.0:
            return "B"
        elif pct >= 60.0:
            return "C"
        elif pct >= 50.0:
            return "D"
        else:
            return "F"

    def calculate_status(self) -> str:
        """
        Determine pass/fail status using conditional logic:
        A student must secure at least PASS_MARK_PER_SUBJECT (40) in EVERY subject,
        AND have an overall percentage of at least PASS_PERCENTAGE_OVERALL (40%).
        """
        # Check individual subject pass criteria
        has_failed_subject = any(
            score < self.PASS_MARK_PER_SUBJECT for score in self.marks.values()
        )
        if has_failed_subject or self.percentage < self.PASS_PERCENTAGE_OVERALL:
            return "FAIL"
        return "PASS"

    def get_failed_subjects(self) -> list:
        """Return list of subject names where student scored below passing mark."""
        return [
            subj for subj, score in self.marks.items()
            if score < self.PASS_MARK_PER_SUBJECT
        ]

    def to_dict(self) -> Dict[str, Any]:
        """Convert Student object to dictionary format for serialization."""
        data = {
            "ID": self.student_id,
            "Name": self.name,
        }
        for subject in self.SUBJECTS:
            data[subject] = self.marks.get(subject, 0.0)
        data.update({
            "Total": self.total_marks,
            "Average": self.average_marks,
            "Percentage": self.percentage,
            "Grade": self.grade,
            "Status": self.status,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """Instantiate a Student object from a dictionary (e.g. from CSV row)."""
        student_id = str(data.get("ID", "")).strip()
        name = str(data.get("Name", "")).strip()
        marks = {}
        for subject in cls.SUBJECTS:
            val = data.get(subject)
            if val is None or str(val).strip() == "":
                marks[subject] = 0.0
            else:
                try:
                    marks[subject] = float(val)
                except (ValueError, TypeError):
                    marks[subject] = 0.0
        return cls(student_id=student_id, name=name, marks=marks)

    def generate_report_card(self) -> str:
        """Generate a formatted ASCII academic report card for terminal display."""
        border = "=" * 60
        sub_border = "-" * 60
        status_symbol = "[PASS]" if self.status == "PASS" else "[FAIL]"
        
        lines = [
            border,
            f"{'EXCELLENCE COACHING CENTER - STUDENT REPORT CARD':^60}",
            border,
            f" Student ID : {self.student_id:<18} Student Name : {self.name}",
            sub_border,
            f" {'Subject':<28} {'Max Marks':<12} {'Marks Obtained':<15}",
            sub_border,
        ]
        
        for subj in self.SUBJECTS:
            marks_val = self.marks[subj]
            subj_status = "P" if marks_val >= self.PASS_MARK_PER_SUBJECT else "F*"
            lines.append(f" {subj:<28} {self.MAX_MARKS_PER_SUBJECT:<12.0f} {marks_val:>6.2f}  ({subj_status})")
        
        lines.extend([
            sub_border,
            f" Total Marks : {self.total_marks:>6.2f} / {len(self.SUBJECTS) * self.MAX_MARKS_PER_SUBJECT:.0f}",
            f" Average     : {self.average_marks:>6.2f}",
            f" Percentage  : {self.percentage:>6.2f}%",
            f" Grade       : {self.grade:<5} | Final Status : {status_symbol}",
        ])
        
        failed = self.get_failed_subjects()
        if failed:
            lines.append(f" * Re-examination required in: {', '.join(failed)}")
        else:
            lines.append(" * Congratulations! Promoted to next level.")
            
        lines.append(border)
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Student(id={self.student_id!r}, name={self.name!r}, total={self.total_marks}, grade={self.grade!r}, status={self.status!r})"

