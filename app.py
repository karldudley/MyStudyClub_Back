from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db' # flask sqlite db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://knonbgucbylgdb:91620f58ea09dd7d85b9d24e4b7a26372ea08ee1bede0e8e3bbb3bfc139ec5fc@ec2-44-209-24-62.compute-1.amazonaws.com:5432/d57frogopfmo03' # heroku postgres db
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise the db
db = SQLAlchemy(app)

# Create Student model
class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #create a function to return a string when we add something
    def __repr__(self):
        return '<Student %r>' % self.id

@app.route('/')
def index():
    return "Welcome to the myStudyClub Server!"

@app.route('/profile')
def my_profile():
    response_body = {
        "name": "Karlos",
        "about" :"Hello! I'm a full stack developer that loves Python and React"
    }
    print(response_body)
    return response_body

@app.route('/testdb', methods=["POST", "GET"])
def testdb():
    if request.method == "POST":
        # create random instance of Student class
        new_student = Student(full_name="karl", user_name="karldudley", email="karl@example.com", password="test123")

        # store random string and url in db
        try:
            db.session.add(new_student)
            db.session.commit()
            return "Correctly added to db"
            # student_table = Student.query.all()
            # return student_table
        except:
            return "There was an error adding to the db"
    else:
        students = Student.query.order_by(Student.created_at)
        for x in students:
            print(x.full_name, x .user_name, x.email, x.password)
        return "hey"
    

if __name__ == '__main__':
    app.run(debug = True)   # pragma: no cover
