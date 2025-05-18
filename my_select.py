from sqlalchemy import func, desc, select, distinct, and_
from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session


def select_1():
    """
    SELECT s.fullname AS student_name,
    ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    INNER JOIN grades g ON s.id = g.student_id
    GROUP BY s.id, s.fullname
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    return session.query(Student.fullname,
                         func.round(func.avg(Grade.grade),2).label('average_grade'))\
           .select_from(Student).join(Grade).group_by(Student.id)\
           .order_by(desc('average_grade')).limit(5).all()


def select_2():
    """
    SELECT s.fullname AS student_name,
    ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    INNER JOIN grades g ON s.id = g.student_id
    WHERE g.subject_id = 3
    GROUP BY s.id, s.fullname
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    return session.query(Student.fullname,
                         func.round(func.avg(Grade.grade),2).label('average_grade'))\
           .select_from(Student).join(Grade).filter(Grade.subjects_id == 3)\
           .group_by(Student.id).order_by(desc('average_grade')).limit(1).all()


def select_3():
    """
    SELECT g.name AS group_name,
    ROUND(AVG(gr.grade), 2) AS average_grade
    FROM grades gr
    INNER JOIN students s ON gr.student_id = s.id
    INNER JOIN groups g ON s.group_id = g.id
    WHERE gr.subject_id = 3
    GROUP BY g.id, g.name
    ORDER BY average_grade DESC;
    """
    return session.query(Group.name,
                         func.round(func.avg(Grade.grade),2).label('average_grade'))\
           .select_from(Grade).join(Student).join(Group).filter(Grade.subjects_id == 3)\
           .group_by(Group.id).order_by(desc('average_grade')).all()


def select_4():
    """
    SELECT ROUND(AVG(grade), 2) AS average_grade
    FROM grades;
    """
    return session.query(func.round(func.avg(Grade.grade),2).label('average_grade'))\
           .select_from(Grade).all()


def select_5():
    """
    SELECT s.name AS subject_name
    FROM subjects s
    WHERE s.teacher_id = 2;
    """
    return session.query(Subject.name).select_from(Subject)\
           .filter_by(teacher_id=2).all()


def select_6():
    """
    SELECT s.fullname AS student_name
    FROM students s
    WHERE s.group_id = 1;
    """
    return session.query(Student.fullname).select_from(Student)\
           .filter_by(group_id=1).all()


def select_7():
    """
    SELECT s.fullname AS student_name,
    g.name AS group_name,
    sub.name AS subject_name,
    gr.grade, gr.grade_date
    FROM grades gr
    INNER JOIN students s ON gr.student_id = s.id
    INNER JOIN groups g ON s.group_id = g.id
    INNER JOIN subjects sub ON gr.subject_id = sub.id
    WHERE g.id = 1 AND sub.id = 3
    ORDER BY s.fullname, gr.grade_date;
    """
    return session.query(Student.fullname, Group.name, Subject.name, Grade.grade,
                         Grade.grade_date).select_from(Grade).join(Student)\
           .join(Group).join(Subject).filter(and_(Group.id == 1, Subject.id == 3))\
           .order_by(Student.fullname).order_by(Grade.grade_date).all()


def select_8():
    """
    SELECT t.fullname AS teacher_name,
    ROUND(AVG(g.grade), 2) AS average_grade
    FROM teachers t
    INNER JOIN subjects s ON t.id = s.teacher_id
    INNER JOIN grades g ON s.id = g.subject_id
    WHERE t.id = 2
    GROUP BY t.fullname;
    """
    return session.query(Teacher.fullname,
                         func.round(func.avg(Grade.grade),2).label('average_grade'))\
           .select_from(Teacher).join(Subject).join(Grade).filter(Teacher.id == 2)\
           .group_by(Teacher.id).all()


def select_9():
    """
    SELECT DISTINCT sub.name AS subject_name
    FROM grades g
    INNER JOIN subjects sub ON g.subject_id = sub.id
    WHERE g.student_id = 5;
    """
    return session.query(distinct(Subject.name)).select_from(Grade)\
           .join(Subject).filter(Grade.student_id == 5).all()


def select_10():
    """
    SELECT DISTINCT s.name AS subject_name
    FROM grades g
    INNER JOIN subjects s ON s.id = g.subject_id
    WHERE g.student_id = 10 AND s.teacher_id = 4
    """
    return session.query(distinct(Subject.name)).select_from(Grade)\
           .join(Subject).filter(and_(Grade.student_id == 10,
                                      Subject.teacher_id == 4)).all()


def select_11():
    """
    SELECT ROUND(AVG(g.grade), 2) AS average_grade,
    s.fullname AS student_name,
    t.fullname AS teacher_name
    FROM grades g
    INNER JOIN subjects sub ON g.subject_id = sub.id
    INNER JOIN students s ON g.student_id = s.id
    INNER JOIN teachers t ON sub.teacher_id = t.id
    WHERE s.id = 20 AND t.id = 3
    GROUP BY s.fullname, t.fullname;
    """
    return session.query(func.round(func.avg(Grade.grade),2).label('average_grade'),
                         Student.fullname, Teacher.fullname)\
           .select_from(Grade).join(Subject).join(Student).join(Teacher)\
           .filter(and_(Student.id == 20, Teacher.id == 3)).group_by(Student.id)\
           .group_by(Teacher.id).all()


def select_12():
    """
    SELECT s.fullname AS student_name,
    g.name AS group_name,
    sub.name AS subject_name,
    gr.grade,
    gr.grade_date
    FROM grades gr
    INNER JOIN students s ON gr.student_id = s.id
    INNER JOIN groups g ON s.group_id = g.id
    INNER JOIN subjects sub ON gr.subject_id = sub.id
    WHERE g.id = 1 AND sub.id = 3 AND
    gr.grade_date = (
        SELECT MAX(gr2.grade_date)
        FROM grades gr2
        INNER JOIN students s2 ON gr2.student_id = s2.id
        WHERE  gr2.subject_id = 3 AND s2.group_id = 1
    )
    ORDER BY s.fullname;
    """
    subquery = (select(func.max(Grade.grade_date)).join(Student).filter(and_(
        Grade.subjects_id == 3, Student.group_id == 1
    ))).scalar_subquery()
    return session.query(Student.fullname, Group.name, Subject.name, Grade.grade,
                         Grade.grade_date).select_from(Grade).join(Student)\
        .join(Group).join(Subject).filter(and_(Group.id == 1, Subject.id == 3,
                                            Grade.grade_date == subquery)).all()


if __name__ == "__main__":
    print(select_12())