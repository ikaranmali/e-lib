#!/usr/bin/python3

#---- Import Operating System Library for Os Feature-----------#
import os

# Using Flask Library for webserver---------
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
##postgress
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3306/elib"
app.config['SECRET_KEY'] = "random string"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

class Rtrn(db.Model):
    __tablename__ = "b_return"
    id = db.Column(db.Integer, primary_key=True)
    St_Name = db.Column(db.String(150), nullable=False)
    Bo_title = db.Column(db.String(150), nullable=False)
    # Date = db.Column(db.DATE, default=datetime.now())
    token_no = db.Column(db.String(15), nullable=False)
    due_date = db.Column(db.String(12))
    bdate = db.Column(db.String(12))
    charges = db.Column(db.Integer)

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(150), nullable=False)
    Edition = db.Column(db.String(150), nullable=False)
    Publication = db.Column(db.String(150), nullable=False)
    Author = db.Column(db.String(50))

class Borrow(db.Model):
    __tablename__ = "borrow"
    id = db.Column(db.Integer, primary_key=True)
    S_Name = db.Column(db.String(150), nullable=False)
    B_title = db.Column(db.String(150), nullable=False)
    B_Ed = db.Column(db.String(150), nullable=False)
    B_Pub = db.Column(db.String(150), nullable=False)
    # Date = db.Column(db.DATE, default=datetime.now())
    token_no = db.Column(db.String(15), nullable=False)
    due = db.Column(db.String(12))
    bdate = db.Column(db.String(12))

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Department = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(13), nullable=False)
    gender = db.Column(db.String(7))
    date = db.Column(db.DATE, default=datetime.now())

@app.route("/", methods=['GET'])
def index():
    students = Borrow.query.all()
    return render_template("intro.html", students=students)

@app.route("/insert", methods=['GET', 'POST'])
def insert():
    if request.method == "POST":

        name = request.form.get("name")
        Dpt = request.form.get("dpt")
        Cnt = request.form.get("cnt")
        gend = request.form.get("gender")

        # Creat new record
        stud = Student(Name = name, Department=Dpt, contact=Cnt, gender=gend)
        db.session.add(stud)
        db.session.commit()

    students = Student.query.all()
    return render_template("insert_new_student.html", students=students)

@app.route("/find", methods=['GET', 'POST'])
def find():
    if request.method == "POST":
        student_name = request.form.get("sname")
        book_name = request.form.get("bname")

        book_name_list = []
        issue_date_list = []
        due_date_list = []


        bp = db.session.query(Borrow.B_title,Borrow.bdate,Borrow.due,Borrow.S_Name,Borrow.id,Borrow.token_no).filter_by(S_Name=str(student_name))
        # sp = db.session.query(Student.id,Student.Name,Student.contact,Student.Department).filter_by(Name=str(student_name))
        # print("*********************************")  
        # print((student_name),str(book_name))   
        
        # book_name_list.clear()
        # issue_date_list.clear()
        # due_date_list.clear()

        # for x in sp:
        #     for y in bp:
        #         print("Book details",y,"Student details",x)
        #         if (str(student_name) == x[1]):
        #             # return render_template("find.html",
        #             #     St_id= x[0],St_Name=x[1],St_contact=x[2],St_department=x[3],
        #             #     book_title= y[0],issue_date = y[1],due_date=y[2])
                   
        #             book_name_list.append(y[0])
        #             issue_date_list.append(y[1])
        #             due_date_list.append(y[2])
        # return render_template("find.html",book_title=book_name_list,issue_date_list=issue_date_list,due_date_list=due_date_list,St_id=x[0],St_Name=x[1],St_contact=x[2],St_department=x[3])
        return render_template("find.html",bp=bp)
        
    return render_template("find.html")


@app.route("/book", methods=['GET', 'POST'])
def book():
    if request.method == "POST":

        title = request.form.get("bt")
        edition = request.form.get("be")
        publication = request.form.get("bp")
        author = request.form.get("ba")

        # Creat new record
        stud = Book(Title = title, Edition=edition, Publication=publication, Author=author)
        db.session.add(stud)
        db.session.commit()

    cla = Book.query.all()
    return render_template("book.html", cla=cla)

@app.route("/borrow_book", methods=['GET', 'POST'])
def borrow():
    if request.method == "POST":

        name = request.form.get("sm")
        bt = request.form.get("bt")
        vn = request.form.get("vn")
        da = request.form.get("date")
        bda = request.form.get("bdate")
        be = request.form.get("be")
        bp = request.form.get("bp")
        
        # Creat new record
        stud = Borrow(S_Name = name, B_title = bt, token_no = vn, due = da, bdate=bda,B_Ed = be, B_Pub = bp)
        db.session.add(stud)
        db.session.commit()
        students = Borrow.query.all()
        return render_template("intro.html", students=students)

    c = db.session.query(Student.Name).all()
    book_i = Book.query.all()
    bt = db.session.query(Book.Title).all()
    be = db.session.query(Book.Edition).all()
    bp = db.session.query(Book.Publication).all()
    return render_template("borrow.html",book_info=book_i,c=c,b=bt,e=be,p=bp)
    
@app.route("/return_book", methods=['GET', 'POST'])
def rtrn():
    if request.method == "POST":

        name = request.form.get("sm")
        BT = request.form.get("bt")
        VN = request.form.get("vn")
        DA = request.form.get("ch")
        DD = request.form.get("dd")
        bDD = request.form.get("bdd")

        # Creat new record
        stud = Rtrn(St_Name = name, Bo_title=BT, token_no=VN, charges=DA, due_date = DD,bdate=bDD)
        db.session.add(stud)
        db.session.commit()

    students = Rtrn.query.all()
    c = db.session.query(Borrow.S_Name).all()
    b = db.session.query(Borrow.B_title).all()
    return render_template("return.html", c=c, b=b, students=students)

if __name__ == "__main__":
    app.run(debug=True,host="127.0.0.1")