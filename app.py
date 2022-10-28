from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db' # flask sqlite db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://knonbgucbylgdb:91620f58ea09dd7d85b9d24e4b7a26372ea08ee1bede0e8e3bbb3bfc139ec5fc@ec2-44-209-24-62.compute-1.amazonaws.com:5432/d57frogopfmo03' # heroku postgres db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise the db
db = SQLAlchemy(app)

# USEFUL COMMANDS
# heroku pg:psql to go into sql shell
# heroku pg:reset DATABASE to reset db
# heroku restart to reset server

# Create One to Many relationships and classes for Set, Message and FlashCard


# join table for many to many
student_club = db.Table('student_club',
                    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
                    )

# Create Student model
class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clubs = db.relationship('Club', secondary=student_club, backref='students')

    #create a function to return a string when we add something
    def __repr__(self):
        return '<Student %r>' % self.full_name

# Create Club model
class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String(50), nullable=False)
    club_code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sets = db.relationship('Set', backref='club')  # setup foreign key for sets
    messages = db.relationship('Message', backref='club')  # setup foreign key for messages
    # message_id foreign key

    #create a function to return a string when we add something
    def __repr__(self):
        return '<Club %r>' % self.club_name

# Create Set model
class Set(db.Model):
    __tablename__ = 'set'
    id = db.Column(db.Integer, primary_key=True)
    set_name = db.Column(db.String(50), nullable=False)
    private = db.Column(db.Boolean, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id')) # link set to club
    messages = db.relationship('Message', backref='set')  # setup foreign key for flashcards
    # flashcard_id foreign key

    #create a function to return a string when we add something
    def __repr__(self):
        return '<Set %r>' % self.set_name

# Create Flashcard model
class Flashcard(db.Model):
    __tablename__ = 'flashcard'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    set_id = db.Column(db.Integer, db.ForeignKey('set.id')) # link flashcard to set

    #create a function to return a string when we add something
    def __repr__(self):
        return '<Flashcard %r>' % self.question[:20]

# Create Message model
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, nullable=False) # link this to User?
    club_id = db.Column(db.Integer, db.ForeignKey('club.id')) # link message to club

    #create a function to return a string when we add something
    def __repr__(self):
        return '<Flashcard %r>' % self.content[:20]

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
        # create random instance of Club class
        new_club = Club(club_name="science", club_code="999")

        # store random string and url in db
        try:
            db.session.add(new_student)
            db.session.add(new_club)
            db.session.commit()
            return "Correctly added to db"
            # student_table = Student.query.all()
            # return student_table
        except:
            return "There was an error adding to the db"
    else:
        # below is just for testing purposes
        students = Student.query.order_by(Student.created_at)
        clubs = Club.query.order_by(Club.created_at)
        for x in students:
            print(x.full_name, x .user_name, x.email, x.password)
        for x in clubs:
            print(x.club_name, x .club_code)
        return "hey"
    

if __name__ == '__main__':
    app.run(debug = True)   # pragma: no cover
