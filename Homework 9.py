import unittest 
from collections import defaultdict
from prettytable import PrettyTable
import os


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


class Student: 
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course = dict() # course is key, grade is value
        self.labels = ['CWID', 'Name', ' Major', 'Courses']

    def add_courses(self, course, grade):
        '''adding courses to student'''
        self.course[course] = grade
    
    def pt_rows(self):
        '''creating row for pretty table- give a list'''
        return [self.cwid, self.name, self.major, sorted(self.course.keys())]



class Instructors:

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

        self.get_students(os.path.join(path, 'students.txt'))
        self.get_instructors(os.path.join(path, 'instructors.txt'))
        self.get_grades(os.path.join(path, 'grades.txt'))

        if ptables:
            print('Student Summary')
            self.student_table()
        
            print('Instructor Summary')
            self.instructor_table()
    
    def get_students(self, path):
        '''get students'''
        for cwid, name, major in file_reader(path, 3, False, '\t'):
            if cwid in self.students: 
                print('warning, student already in database')
            self.students[cwid] = Student(cwid, name, major)
    
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


    def student_table(self):
        '''creating a pretty table for students'''
        pt = PrettyTable(field_names = ['CWID', 'Name', 'major', 'Completed Courses'])
        for student in self.students.values():
            pt.add_row(student.pt_rows())
        print(pt)
        

    def instructor_table(self):
        '''creating instructor table'''
        pt = PrettyTable(field_names =['CWID', 'Name', 'Department', 'Course', 'Students'])
        for instructor in self.instructors.values():
            for row in instructor.pt_rows():
                pt.add_row(row)

        print(pt)
        return pt


def main():
    path ='C:/Users/kiera/OneDrive/Grad School Junk/SSW-810/Homework 9'
    stevens = Repository(path)
    

class RepositoryTest(unittest.TestCase):
    '''write unittest for two students and two instructors'''

    def test_files(self):
        path ='C:/Users/kiera/OneDrive/Grad School Junk/SSW-810/Homework 9'
        test = Repository(path)
       

        self.assertEqual(test.students['10103'].course['CS 501'], 'B')
        self.assertEqual(test.students['10115'].course['CS 545'], 'A')
        self.assertEqual(test.instructors['98765'].course['SSW 567'], 4)
        self.assertEqual(test.instructors['98764'].course['SSW 564'], 3)
        

    


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
