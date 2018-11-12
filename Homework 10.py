import unittest 
from collections import defaultdict
from prettytable import PrettyTable
import os
import sqlite3



def file_reader(path, number, header, separator):
    '''part 2 of homework, path is file path, separate is separator, header is whether there is a header or not, number is number of fields'''
    
    try: 
        fp = open (path, 'r')
    except FileNotFoundError: 
        print("can't open", path)
    else: 
        with fp:
            for n, line in enumerate(fp):
                if n == 0 and header: 
                    continue #skip the header row
                else: 
                    fields = line.rstrip('\r\n').split(separator)
                    if len(fields) != number: 
                        raise ValueError
                    else: 
                        yield tuple(fields)



class Major:
    pt_hdr = ['Major', 'Required Courses', 'Elective Courses']

    def __init__(self, major): 
        self.major = major
        self.required = set()
        self.electives = set()
        self.passing = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}

    def add_course(self, flag, course): 
        '''adding majors with list of required and electives courses'''
        if flag == 'E':
            self.electives.add(course)
        elif flag == 'R':
            self.required.add(course)
        else: 
            raise ValueError(f'flag not in proper format for course {course}')

    
    def grade_check(self, courses):
        '''returning all the courses looking for passing grades'''
        completed_courses = {course for course, grade in courses.items() if grade in self.passing}
        remaining_required = self.required - completed_courses
        if self.electives.intersection(completed_courses): 
            remaining_electives = 'None'
        else: 
            remaining_electives = self.electives
        
        if completed_courses == set():
            completed_courses = 'None'
            
        return completed_courses, remaining_required, remaining_electives

    def pt_rows(self): 
        return [self.major, sorted(self.required), sorted(self.electives)]

    


class Student: 
    pt_hdr = ['CWID', 'Name', 'Major', 'Completed Coures', 'Remaining Required', 'Remaining Electives']

    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course = dict() # course is key, grade is value

        
    def add_courses(self, course, grade):
        '''adding courses to student'''
        self.course[course] = grade


    def pt_rows(self):
        '''creating row for pretty table- give a list'''
        completed_courses, remaining_required, remaining_electives = self.major.grade_check(self.course)


        return [self.cwid, self.name, self.major.major, completed_courses, remaining_required, remaining_electives]



class Instructors:
    pt_hdr = ['CWID', 'Name', 'Department', 'Courses', 'Students']
    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.course = defaultdict(int) #key:course value: number of students

    def add_student (self, course):
        if course in self.course: 
            self.course[course] +=1
        else: 
            self.course[course] = 1

    def pt_rows(self):
        for course, students in self.course.items(): 
            yield [self.cwid, self.name, self.dept, course, students]
        




class Repository: 
    
    def __init__(self, path, ptables =True):
        self.path = path
        self.students = dict()
        self.instructors = dict()
        self.majors = dict() #key is major, value is instance of major 

        
       
        self.get_majors(os.path.join(path, 'majors.txt'))
        self.get_students(os.path.join(path, 'students.txt'))
        self.get_instructors(os.path.join(path, 'instructors.txt'))
        self.get_grades(os.path.join(path, 'grades.txt'))
        
        

        if ptables:
            print('Student Summary')
            self.student_table()
        
            print('Instructor Summary')
            self.instructor_table()

            print('Major summary')
            self.majors_table()
    
    def get_students(self, path):
        '''get students'''
        for cwid, name, major in file_reader(path, 3, False, '\t'):
            if cwid in self.students: 
                print('warning, student already in database')
            self.students[cwid] = Student(cwid, name, self.majors[major])
    
    def get_instructors(self,path):
        '''get instructors'''
        for cwid, name, dept in file_reader(path, 3, False, '\t'):
            self.instructors[cwid] = Instructors(cwid, name, dept)


    def get_grades(self, path):
        for cwid, course, grade, instructorID in file_reader(path, 4, False, '\t'):
            if cwid in self.students:
                self.students[cwid].add_courses(course, grade)
            else:  
                print('student CWID is not known')
        
        for cwid, course, grade, instructorID in file_reader(path, 4, False, '\t'):
            if instructorID in self.instructors: 
                self.instructors[instructorID].add_student(course)
            else: 
                print('Instructor is not known')
    
    def get_majors(self, path): 
        '''getting majors from file'''
        for major, flag, course in file_reader(path, 3, False, '\t'):
            if major not in self.majors:
                self.majors[major] = Major(major)
            
            self.majors[major].add_course(flag, course)


    def student_table(self):
        '''creating a pretty table for students'''
        pt = PrettyTable(field_names = Student.pt_hdr)
        for student in self.students.values():
            pt.add_row(student.pt_rows())
        print(pt)
        

    def instructor_table(self):
        '''creating instructor table'''
        pt = PrettyTable(field_names =Instructors.pt_hdr)

        db_file ='C:/Users/kiera/Downloads/jrr.db'
        db = sqlite3.connect(db_file)
        
        for row in db.execute('select CWID, Name, Dept, Course, Count(Student_CWID) from HW11_instructors i join hw11_grades g on i.CWID = g.Instructor_CWID group by Course'):
            pt.add_row(row)

        print(pt)

    def majors_table(self): 
        '''creating majors table'''
        pt = PrettyTable(field_names = Major.pt_hdr)
        for major in self.majors.values(): 
            pt.add_row(major.pt_rows())
        print(pt)

    


def main():
    path ='C:/Users/kiera/OneDrive/Grad School Junk/SSW-810/Homework 9'
    stevens = Repository(path)
    



if __name__ == '__main__':
    main()

