"""
test_system.py - Comprehensive Unit Tests for Student Result Management System.
Verifies all requirements: OOP classes, calculations, conditional logic,
search, top/lowest scorers, summary, and CSV persistence.
"""

import os
import tempfile
import unittest
from src.student import Student
from src.result_manager import ResultManager


class TestStudentClass(unittest.TestCase):
    """Unit tests for the Student class."""

    def setUp(self):
        self.perfect_marks = {
            "Mathematics": 100.0,
            "Physics": 100.0,
            "Chemistry": 100.0,
            "English": 100.0,
            "Computer Science": 100.0,
        }
        self.pass_marks = {
            "Mathematics": 85.0,
            "Physics": 78.0,
            "Chemistry": 92.0,
            "English": 88.0,
            "Computer Science": 90.0,
        }
        self.borderline_marks = {
            "Mathematics": 40.0,
            "Physics": 40.0,
            "Chemistry": 40.0,
            "English": 40.0,
            "Computer Science": 40.0,
        }
        self.one_fail_subject = {
            "Mathematics": 90.0,
            "Physics": 35.0,  # Below 40
            "Chemistry": 85.0,
            "English": 80.0,
            "Computer Science": 88.0,
        }
        self.all_fail_marks = {
            "Mathematics": 30.0,
            "Physics": 25.0,
            "Chemistry": 35.0,
            "English": 28.0,
            "Computer Science": 32.0,
        }

    def test_calculations_perfect_score(self):
        student = Student("STU01", "Alice Wonder", self.perfect_marks)
        self.assertEqual(student.total_marks, 500.0)
        self.assertEqual(student.average_marks, 100.0)
        self.assertEqual(student.percentage, 100.0)
        self.assertEqual(student.grade, "A+")
        self.assertEqual(student.status, "PASS")

    def test_calculations_standard_student(self):
        student = Student("STU02", "Bob Marley", self.pass_marks)
        self.assertEqual(student.total_marks, 433.0)
        self.assertEqual(student.average_marks, 86.6)
        self.assertEqual(student.percentage, 86.6)
        self.assertEqual(student.grade, "A")
        self.assertEqual(student.status, "PASS")

    def test_grade_boundaries(self):
        # 90%+ -> A+
        s_aplus = Student("T1", "A+", {"Mathematics": 90, "Physics": 90, "Chemistry": 90, "English": 90, "Computer Science": 90})
        self.assertEqual(s_aplus.grade, "A+")

        # 80-89% -> A
        s_a = Student("T2", "A", {"Mathematics": 80, "Physics": 80, "Chemistry": 80, "English": 80, "Computer Science": 80})
        self.assertEqual(s_a.grade, "A")

        # 70-79% -> B
        s_b = Student("T3", "B", {"Mathematics": 70, "Physics": 70, "Chemistry": 70, "English": 70, "Computer Science": 70})
        self.assertEqual(s_b.grade, "B")

        # 60-69% -> C
        s_c = Student("T4", "C", {"Mathematics": 60, "Physics": 60, "Chemistry": 60, "English": 60, "Computer Science": 60})
        self.assertEqual(s_c.grade, "C")

        # 50-59% -> D
        s_d = Student("T5", "D", {"Mathematics": 50, "Physics": 50, "Chemistry": 50, "English": 50, "Computer Science": 50})
        self.assertEqual(s_d.grade, "D")

        # < 50% -> F
        s_f = Student("T6", "F", {"Mathematics": 35, "Physics": 35, "Chemistry": 35, "English": 35, "Computer Science": 35})
        self.assertEqual(s_f.grade, "F")

    def test_pass_fail_conditional_logic(self):
        # Borderline passing (all 40)
        s_border = Student("B1", "Borderline Pass", self.borderline_marks)
        self.assertEqual(s_border.status, "PASS")

        # Student with high overall marks but failed 1 subject (< 40)
        s_fail_subj = Student("F1", "Failed One Subject", self.one_fail_subject)
        self.assertEqual(s_fail_subj.status, "FAIL")
        self.assertIn("Physics", s_fail_subj.get_failed_subjects())

        # Student failing all subjects
        s_fail_all = Student("F2", "Failed All", self.all_fail_marks)
        self.assertEqual(s_fail_all.status, "FAIL")
        self.assertEqual(len(s_fail_all.get_failed_subjects()), 5)

    def test_invalid_mark_raises_exception(self):
        # Mark > 100
        invalid_high = dict(self.pass_marks)
        invalid_high["Mathematics"] = 105.0
        with self.assertRaises(ValueError):
            Student("ERR1", "Error High", invalid_high)

        # Mark < 0
        invalid_low = dict(self.pass_marks)
        invalid_low["Physics"] = -5.0
        with self.assertRaises(ValueError):
            Student("ERR2", "Error Low", invalid_low)

        # Non-numeric mark
        invalid_type = dict(self.pass_marks)
        invalid_type["Chemistry"] = "NOT_A_NUMBER"
        with self.assertRaises(ValueError):
            Student("ERR3", "Error String Mark", invalid_type)

    def test_empty_id_or_name_raises_exception(self):
        with self.assertRaises(ValueError):
            Student("", "Valid Name", self.pass_marks)
        with self.assertRaises(ValueError):
            Student("   ", "Valid Name", self.pass_marks)
        with self.assertRaises(ValueError):
            Student("STU99", "", self.pass_marks)
        with self.assertRaises(ValueError):
            Student("STU99", "   ", self.pass_marks)

    def test_from_dict_handles_empty_and_whitespace_marks(self):
        raw_row = {
            "ID": "STU88",
            "Name": "Partial Data",
            "Mathematics": "85.0",
            "Physics": "",
            "Chemistry": "   ",
            "English": None,
            "Computer Science": "90",
        }
        s = Student.from_dict(raw_row)
        self.assertEqual(s.marks["Mathematics"], 85.0)
        self.assertEqual(s.marks["Physics"], 0.0)
        self.assertEqual(s.marks["Chemistry"], 0.0)
        self.assertEqual(s.marks["English"], 0.0)
        self.assertEqual(s.marks["Computer Science"], 90.0)
        self.assertEqual(s.total_marks, 175.0)

    def test_serialization_dict(self):
        student = Student("STU99", "Serialization Test", self.pass_marks)
        d = student.to_dict()
        self.assertEqual(d["ID"], "STU99")
        self.assertEqual(d["Name"], "Serialization Test")
        self.assertEqual(d["Total"], 433.0)

        restored = Student.from_dict(d)
        self.assertEqual(restored.student_id, student.student_id)
        self.assertEqual(restored.total_marks, student.total_marks)
        self.assertEqual(restored.grade, student.grade)
        self.assertEqual(restored.status, student.status)

    def test_report_card_output(self):
        student = Student("STU10", "Report Card Test", self.pass_marks)
        report = student.generate_report_card()
        self.assertIn("STU10", report)
        self.assertIn("Report Card Test", report)
        self.assertIn("433.00", report)
        self.assertIn("[PASS]", report)


class TestResultManagerClass(unittest.TestCase):
    """Unit tests for the ResultManager class."""

    def setUp(self):
        # Use a temporary file for CSV to avoid modifying actual data
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_csv = os.path.join(self.temp_dir.name, "test_students.csv")
        self.manager = ResultManager(csv_filepath=self.temp_csv)

        self.s1 = Student("S01", "Student One", {
            "Mathematics": 95, "Physics": 90, "Chemistry": 92, "English": 88, "Computer Science": 94
        })  # Total 459, PASS
        self.s2 = Student("S02", "Student Two", {
            "Mathematics": 70, "Physics": 75, "Chemistry": 72, "English": 68, "Computer Science": 70
        })  # Total 355, PASS
        self.s3 = Student("S03", "Student Three", {
            "Mathematics": 35, "Physics": 30, "Chemistry": 40, "English": 45, "Computer Science": 50
        })  # Total 200, FAIL

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_search_student(self):
        self.assertTrue(self.manager.add_student(self.s1))
        self.assertEqual(self.manager.count(), 1)

        # Search existing
        found = self.manager.search_student("S01")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Student One")

        # Search case-insensitive
        found_lower = self.manager.search_student("s01")
        self.assertIsNotNone(found_lower)
        self.assertEqual(found_lower.student_id, "S01")

        # Search non-existing
        self.assertIsNone(self.manager.search_student("UNKNOWN"))

    def test_duplicate_id_rejected(self):
        self.manager.add_student(self.s1)
        duplicate = Student("S01", "Duplicate Guy", {
            "Mathematics": 50, "Physics": 50, "Chemistry": 50, "English": 50, "Computer Science": 50
        })
        self.assertFalse(self.manager.add_student(duplicate))
        self.assertEqual(self.manager.count(), 1)

    def test_delete_student(self):
        self.manager.add_student(self.s1)
        self.assertEqual(self.manager.count(), 1)
        self.assertTrue(self.manager.delete_student("S01"))
        self.assertEqual(self.manager.count(), 0)
        self.assertFalse(self.manager.delete_student("S01"))

    def test_highest_and_lowest_scoring_students(self):
        self.manager.add_student(self.s1)  # 459
        self.manager.add_student(self.s2)  # 355
        self.manager.add_student(self.s3)  # 200

        highest = self.manager.get_highest_scoring_students()
        lowest = self.manager.get_lowest_scoring_students()

        self.assertEqual(len(highest), 1)
        self.assertEqual(highest[0].student_id, "S01")
        self.assertEqual(highest[0].total_marks, 459.0)

        self.assertEqual(len(lowest), 1)
        self.assertEqual(lowest[0].student_id, "S03")
        self.assertEqual(lowest[0].total_marks, 200.0)

    def test_highest_lowest_ties(self):
        tied_high = Student("S04", "Tied High", {
            "Mathematics": 95, "Physics": 90, "Chemistry": 92, "English": 88, "Computer Science": 94
        })  # Total 459
        self.manager.add_student(self.s1)
        self.manager.add_student(tied_high)

        highest = self.manager.get_highest_scoring_students()
        self.assertEqual(len(highest), 2)
        ids = {s.student_id for s in highest}
        self.assertEqual(ids, {"S01", "S04"})

    def test_class_summary_generation(self):
        self.manager.add_student(self.s1)  # Pass
        self.manager.add_student(self.s2)  # Pass
        self.manager.add_student(self.s3)  # Fail

        summary = self.manager.generate_class_summary()
        self.assertEqual(summary["total_students"], 3)
        self.assertEqual(summary["passed_count"], 2)
        self.assertEqual(summary["failed_count"], 1)
        self.assertAlmostEqual(summary["pass_percentage"], 66.67, places=1)
        self.assertIn("Mathematics", summary["subject_averages"])
        self.assertIn("A+", summary["grade_distribution"])

    def test_csv_save_and_load(self):
        self.manager.add_student(self.s1)
        self.manager.add_student(self.s2)
        self.manager.add_student(self.s3)

        # Save to CSV
        save_ok, msg = self.manager.save_to_csv()
        self.assertTrue(save_ok)
        self.assertTrue(os.path.exists(self.temp_csv))

        # Create fresh manager pointing to same CSV
        fresh_manager = ResultManager(csv_filepath=self.temp_csv)
        self.assertEqual(fresh_manager.count(), 3)
        loaded_s1 = fresh_manager.search_student("S01")
        self.assertIsNotNone(loaded_s1)
        self.assertEqual(loaded_s1.name, "Student One")
        self.assertEqual(loaded_s1.total_marks, 459.0)
        self.assertEqual(loaded_s1.grade, "A+")
        self.assertEqual(loaded_s1.status, "PASS")

    def test_update_student_marks(self):
        self.manager.add_student(self.s1)
        self.assertEqual(self.s1.marks["Mathematics"], 95.0)

        # Successful update
        ok = self.manager.update_student_marks("S01", {"Mathematics": 100.0, "Physics": 95.0})
        self.assertTrue(ok)
        self.assertEqual(self.s1.marks["Mathematics"], 100.0)
        self.assertEqual(self.s1.marks["Physics"], 95.0)
        # Verify recalculate happened
        self.assertEqual(self.s1.total_marks, 469.0)

        # Update non-existent student
        self.assertFalse(self.manager.update_student_marks("DOES_NOT_EXIST", {"Mathematics": 80.0}))

    def test_update_student_marks_atomic_rollback(self):
        self.manager.add_student(self.s1)
        original_math = self.s1.marks["Mathematics"]
        original_total = self.s1.total_marks

        # Attempt updating with one valid and one invalid mark (> 100)
        with self.assertRaises(ValueError):
            self.manager.update_student_marks("S01", {"Mathematics": 50.0, "Physics": 999.0})

        # Ensure atomic rollback: valid field must not have mutated
        self.assertEqual(self.s1.marks["Mathematics"], original_math)
        self.assertEqual(self.s1.total_marks, original_total)

    def test_get_all_students_sorting(self):
        self.manager.add_student(self.s1)  # Name: Student One, Total: 459
        self.manager.add_student(self.s2)  # Name: Student Two, Total: 355
        self.manager.add_student(self.s3)  # Name: Student Three, Total: 200

        # Sort by total marks (descending)
        by_total = self.manager.get_all_students(sort_by="total")
        self.assertEqual([s.student_id for s in by_total], ["S01", "S02", "S03"])

        # Sort by name
        by_name = self.manager.get_all_students(sort_by="name")
        self.assertEqual([s.student_id for s in by_name], ["S01", "S03", "S02"])

        # Sort by ID
        by_id = self.manager.get_all_students(sort_by="id")
        self.assertEqual([s.student_id for s in by_id], ["S01", "S02", "S03"])

    def test_load_from_csv_clears_stale_records(self):
        # Manager starts with 3 students
        self.manager.add_student(self.s1)
        self.manager.add_student(self.s2)
        self.manager.add_student(self.s3)
        self.assertEqual(self.manager.count(), 3)

        # Save only s1 to CSV
        single_manager = ResultManager(csv_filepath=self.temp_csv)
        single_manager.students = {"S01": self.s1}
        single_manager.save_to_csv()

        # Reloading in the original manager should clear deleted records (count becomes 1, not 3)
        ok, msg = self.manager.load_from_csv(self.temp_csv)
        self.assertTrue(ok)
        self.assertEqual(self.manager.count(), 1)
        self.assertIsNotNone(self.manager.search_student("S01"))
        self.assertIsNone(self.manager.search_student("S02"))
        self.assertIsNone(self.manager.search_student("S03"))

    def test_empty_manager_summary_and_scorers(self):
        empty_manager = ResultManager(csv_filepath=os.path.join(self.temp_dir.name, "empty.csv"))
        empty_manager.students.clear()

        self.assertEqual(empty_manager.get_highest_scoring_students(), [])
        self.assertEqual(empty_manager.get_lowest_scoring_students(), [])

        summary = empty_manager.generate_class_summary()
        self.assertEqual(summary["total_students"], 0)
        self.assertEqual(summary["class_average_total"], 0.0)
        self.assertEqual(summary["highest_scorers"], [])
        self.assertEqual(summary["lowest_scorers"], [])


if __name__ == "__main__":
    unittest.main()

