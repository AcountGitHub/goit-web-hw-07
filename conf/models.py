from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    group_id = Column('group_id', ForeignKey('groups.id',
                                             ondelete='CASCADE', onupdate='CASCADE'))
    group = relationship('Group', backref='students')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers.id',
                                                 ondelete='SET NULL', onupdate='CASCADE'))
    teacher = relationship('Teacher', backref='disciplines')


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=True)
    grade_date = Column('grade_date', Date, nullable=False)
    student_id = Column('student_id', ForeignKey('students.id',
                                                 ondelete='CASCADE', onupdate='CASCADE'))
    subjects_id = Column('subject_id', ForeignKey('subjects.id',
                                                 ondelete='CASCADE', onupdate='CASCADE'))
    student = relationship('Student', backref='grade')
    discipline = relationship('Subject', backref='grade')