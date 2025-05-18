import random
import logging
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

# Import models
from conf.models import Base, Group, Student, Teacher, Subject, Grade
from conf.db import session, engine


NUMBER_GROUPS = 3
NUMBER_STUDENTS = 50
NUMBER_TEACHERS = 5
NUMBER_SUBJECTS = 8
NUMBER_GRADES = 1000  # NUMBER_STUDENTS*20

def generate_fake_data(number_groups, number_teachers, number_students,
                       number_subjects, number_grades) -> tuple:
    fake_groups = []
    fake_students = []
    fake_teachers = []
    fake_subjects = []
    fake_grades = []

    fake_data = Faker()

    # Create groups in the amount number_groups
    for _ in range(number_groups):
        fake_groups.append(Group(name=fake_data.word()))

    # Generate number_teachers teachers
    for _ in range(number_teachers):
        fake_teachers.append(Teacher(fullname=fake_data.name()))

    # Generate number_students students
    for _ in range(number_students):
        fake_students.append(Student(fullname=fake_data.name(),
                                     group=random.choice(fake_groups)))

    # Generate number_subjects subjects
    for _ in range(number_subjects):
        fake_subjects.append(Subject(name=fake_data.word(),
                                     teacher=random.choice(fake_teachers)))

    # Create fake grades
    for _ in range(number_grades):
        fake_grades.append(Grade(student=random.choice(fake_students),
                                 discipline=random.choice(fake_subjects),
                                 grade=random.randint(0,100),
                                 grade_date=fake_data.date_this_year()))

    return fake_groups, fake_teachers, fake_students, fake_subjects, fake_grades


def insert_data(records: list):
    try:
        session.add_all(records)
        session.commit()
    except SQLAlchemyError as e:
        logging.error(e)
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    # Recreating the database
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Generate data
    groups, teachers, students, subjects, grades = \
        generate_fake_data(NUMBER_GROUPS, NUMBER_TEACHERS,
                            NUMBER_STUDENTS, NUMBER_SUBJECTS, NUMBER_GRADES)
    # Insert data
    insert_data(groups)
    insert_data(teachers)
    insert_data(students)
    insert_data(subjects)
    insert_data(grades)
    print("PostgreSQL database successfully filled.")