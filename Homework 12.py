from flask import Flask, render_template
import sqlite3

db_file = 'C:/Users/kiera/OneDrive/Grad School Junk/SSW-810/homework 12/Homework 12'


app = Flask(__name__)

@app.route("/instructors")

def instructors():
    query = '''select CWID, Name, Dept, Course, Count(Student_CWID) from HW11_instructors i join hw11_grades g on i.CWID = g.Instructor_CWID group by Course'''

    db = sqlite3.connect(db_file)
    results = db.execute(query)

    data = [{'cwid':cwid, 'name': name, 'dept':dept, 'course': course, 'count':count} for cwid, name, dept, course, count in results]

    db.close()

    return render_template('instructor_table.html', title= 'instructor summary', table_title = 'number of students per class', instructors = data)

app.run(debug= True)
    


