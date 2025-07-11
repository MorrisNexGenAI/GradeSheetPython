import os
import django
from django.db import transaction

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grade_system.settings")
django.setup()

# Import models after setting up Django
from subjects.models import Subject
from levels.models import Level
from academic_years.models import AcademicYear
from students.models import Student
from enrollment.models import Enrollment
from pass_and_failed.models import PassFailedStatus
from grades.models import Grade
from periods.models import Period
from datetime import date

with transaction.atomic():
    # Clear existing data
    Grade.objects.all().delete()
    print("Deleted all existing grades.")
    PassFailedStatus.objects.all().delete()
    print("Deleted all existing pass/failed statuses.")
    Enrollment.objects.all().delete()
    print("Deleted all existing enrollments.")
    Student.objects.all().delete()
    print("Deleted all existing students.")
    AcademicYear.objects.all().delete()
    print("Deleted all existing academic years.")
    Subject.objects.all().delete()
    print("Deleted all existing subjects.")
    Level.objects.all().delete()
    print("Deleted all existing levels.")
    Period.objects.all().delete()
    print("Deleted all existing periods.")

    # Create academic years
    academic_years_data = [
        {"name": "2024/2025", "start_date": date(2024, 9, 1), "end_date": date(2025, 7, 30)},
        {"name": "2025/2026", "start_date": date(2025, 9, 1), "end_date": date(2026, 7, 30)},
    ]
    academic_years = []
    for ay_data in academic_years_data:
        ay = AcademicYear.objects.create(
            name=ay_data["name"],
            start_date=ay_data["start_date"],
            end_date=ay_data["end_date"]
        )
        academic_years.append(ay)
        print(f"Created AcademicYear {ay.name} (ID: {ay.id}, Start: {ay.start_date}, End: {ay.end_date})")

    # Create levels (7-9)
    levels = []
    for i in range(7, 10):
        level = Level.objects.create(name=str(i))
        levels.append(level)
        print(f"Created Level {i} (ID: {level.id})")

    # Create subjects
    subjects = [
        "Mathematics", "English", "Science", "Civics", "History",
        "Geography", "RME", "Vocabulary", "Agriculture"
    ]
    subject_objects = []
    for level in levels:
        for subject_name in subjects:
            subject = Subject.objects.create(subject=subject_name, level=level)
            subject_objects.append(subject)
            print(f"Created subject: {subject_name} (ID: {subject.id}) for level {level.name} (ID: {level.id})")

    # Create periods
    periods = [
        {"period": "1st", "is_exam": False},
        {"period": "2nd", "is_exam": False},
        {"period": "3rd", "is_exam": False},
        {"period": "1exam", "is_exam": True},
        {"period": "4th", "is_exam": False},
        {"period": "5th", "is_exam": False},
        {"period": "6th", "is_exam": False},
        {"period": "2exam", "is_exam": True},
    ]
    period_objects = []
    for period_data in periods:
        period = Period.objects.create(period=period_data["period"], is_exam=period_data["is_exam"])
        period_objects.append(period)
        print(f"Created period: {period.period} (ID: {period.id}, is_exam: {period.is_exam})")

    # Create students
    students_data = [
        {"firstName": "John", "lastName": "Doe", "gender": "M", "dob": "2010-01-01"},
        {"firstName": "Jane", "lastName": "Smith", "gender": "F", "dob": "2010-02-15"},
        {"firstName": "Alex", "lastName": "Johnson", "gender": "O", "dob": "2010-03-10"},
    ]
    students = []
    for student_data in students_data:
        student = Student.objects.create(
            firstName=student_data["firstName"],
            lastName=student_data["lastName"],
            gender=student_data["gender"],
            dob=student_data["dob"]
        )
        students.append(student)
        print(f"Created student: {student.firstName} {student.lastName} (ID: {student.id})")

    # Create enrollments
    enrollments = []
    for student in students:
        for level in levels:  # Enroll in all levels for testing
            for academic_year in academic_years[:1]:  # Use 2024/2025
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    level=level,
                    academic_year=academic_year,
                    defaults={
                        'date_enrolled': academic_year.start_date,
                        'enrollment_status': 'ENROLLED'
                    }
                )
                enrollments.append(enrollment)
                print(f"{'Created' if created else 'Found'} enrollment for student {student.id} in level {level.id}, academic year {academic_year.id}")

    # Create PassFailedStatus records
    for enrollment in enrollments:
        status, created = PassFailedStatus.objects.get_or_create(
            student=enrollment.student,
            level=enrollment.level,
            academic_year=enrollment.academic_year,
            enrollment=enrollment,
            defaults={
                'status': 'PENDING',
                'grades_complete': True
            }
        )
        print(f"{'Created' if created else 'Found'} PassFailedStatus for student {enrollment.student.id} in level {enrollment.level.id}")

    # Create sample grades for students
    for enrollment in enrollments:
        level_subjects = Subject.objects.filter(level=enrollment.level)
        for subject in level_subjects:
            for period in period_objects:
                Grade.objects.create(
                    enrollment=enrollment,
                    subject=subject,
                    period=period,
                    score=85  # Integer score
                )
                print(f"Created grade for student {enrollment.student.id}, subject {subject.id}, period {period.period}")

print("Database seeded successfully with academic years, levels, subjects, periods, students, enrollments, pass/failed statuses, and grades.")