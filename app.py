from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from flask import Flask, request, jsonify, request, json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
import psycopg2
from flask_marshmallow import Marshmallow

app = Flask(__name__)
cors = CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db' # flask sqlite db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://knonbgucbylgdb:91620f58ea09dd7d85b9d24e4b7a26372ea08ee1bede0e8e3bbb3bfc139ec5fc@ec2-44-209-24-62.compute-1.amazonaws.com:5432/d57frogopfmo03' # heroku postgres db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise the db
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config['JWT_SECRET_KEY'] = 'Remember to change me'  # Config JWT secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(
    hours=3)  # specifies token lifespan
jwt = JWTManager(app)

conn = psycopg2.connect(database="d57frogopfmo03",
                        host="ec2-44-209-24-62.compute-1.amazonaws.com",
                        user="knonbgucbylgdb",
                        password="91620f58ea09dd7d85b9d24e4b7a26372ea08ee1bede0e8e3bbb3bfc139ec5fc",
                        port="5432")
cursor = conn.cursor()

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

class StudentClubSchema(ma.Schema):
    class Meta:
        fields = ('student_id', 'students.name', 'club_id', 'clubs.name')
student_club_schema = StudentClubSchema()
students_clubs_schema = StudentClubSchema(many=True)

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

    def __init__(self, full_name, user_name, email, password):
        self.full_name = full_name
        self.user_name = user_name
        self.email = email
        self.password = password

    #create a function to return a string when we add something
    def __repr__(self):
        return '<Student %r>' % self.id     # pragma: no cover

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'full_name', 'user_name', 'email', 'password', 'created_at')
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

# Create Club model
class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String(50), nullable=False)
    club_code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sets = db.relationship('Set', backref='club')  # setup foreign key for sets
    messages = db.relationship('Message', backref='club', cascade="delete, merge, save-update")  # setup foreign key for messages

    def __init__(self, club_name, club_code):
        self.club_name = club_name
        self.club_code = club_code

    #create a function to return a string when we add something
    def __repr__(self):
        return '<Club %r>' % self.club_name     # pragma: no cover

class ClubSchema(ma.Schema):
    class Meta:
        fields = ('id', 'club_name', 'club_code', 'created_at')
club_schema = ClubSchema()
clubs_schema = ClubSchema(many=True)

# Create Set model
class Set(db.Model):
    __tablename__ = 'set'
    id = db.Column(db.Integer, primary_key=True)
    set_name = db.Column(db.String(50), nullable=False)
    private = db.Column(db.Boolean, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    # best_time = db.Column(db.Integer, nullable=False)
    # top_user = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id')) # link set to club
    flashcards = db.relationship('Flashcard', backref='set')  # setup foreign key for flashcards

    #create a function to return a string when we add something
    def __repr__(self):
        return '<Set %r>' % self.set_name       # pragma: no cover

class SetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'set_name', 'private', 'likes', 'created_at', 'club_id', 'club.club_name')
set_schema = SetSchema()
sets_schema = SetSchema(many=True)

# Create Flashcard model
class Flashcard(db.Model):
    __tablename__ = 'flashcard'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    set_id = db.Column(db.Integer, db.ForeignKey('set.id')) # link flashcard to set

    def __init__(self, question, answer, set_id):
        self.question = question
        self.answer = answer
        self.set_id = set_id

    #create a function to return a string when we add something
    def __repr__(self):
        return '<Flashcard %r>' % self.question[:20]        # pragma: no cover

class FlashcardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'question', 'answer', 'created_at', 'set_id', 'set.set_name')
flashcard_schema = FlashcardSchema()
flashcards_schema = FlashcardSchema(many=True)

# Create Message model
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, nullable=False) # link this to User? // change to student_id
    club_id = db.Column(db.Integer, db.ForeignKey('club.id')) # link message to club

    #create a function to return a string when we add something
    def __repr__(self):
        return '<Flashcard %r>' % self.content[:20]         # pragma: no cover

class MessageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content', 'created_at', 'club_id', 'club.club_name')
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

@app.route('/')
def index():
    return ("<h1 style=\"color:#B0E0E6;\">Welcome to the myStudyClub server</h1>"
    "<h2 style=\"color:#468499;\">The following GET endpoints currently exist:</h2>"
    "<h3>/students</h3><h3>/students/:id</h3>"
    "<h3>/clubs</h3><h3>/clubs/:id</h3>"
    "<h3>/studentclubs</h3><h3>/studentclubs/:id</h3>"
    "<h3>/sets</h3><h3>/sets/:id</h3>"
    "<h3>/messages</h3><h3>/messages/:id</h3>"
    "<h3>/flashcards</h3><h3>/flashcards/:set_id</h3>"
    "<h2 style=\"color:#468499;\">The following POST endpoints currently exist:</h2>"
    "<h3>/students</h3>"
    "<h3>/flashcards</h3>"
    "<h2 style=\"color:#468499;\">The following PATCH endpoints currently exist:</h2>"
    "<h3>/flashcards/:id</h3>"
    "<h2 style=\"color:#468499;\">The following DELETE endpoints currently exist:</h2>"
    "<h3>/flashcards/:id</h3>"
    )

@app.route('/studentclubs')
def studentclubs():
    cursor.execute("SELECT * FROM student_club;")
    rows = cursor.fetchall()
    return jsonify(rows), 200

@app.route('/studentclubs/<id>')
def studentclub(id):
    # cursor.execute(f"SELECT * FROM student_club WHERE student_id={id};")
    # rows = cursor.fetchall()
    # return clubs, 200
    student = Student.query.get(id)
    clubs = student.clubs
    res = clubs_schema.dump(clubs)
    return jsonify(res), 200

@app.route('/students', methods=["POST", "GET"])
def students():
    if request.method == "POST":
        full_name = request.json['full_name']
        user_name = request.json['user_name']
        email = request.json['email']
        password = request.json['password']
        new_student = Student(full_name, user_name, email, password)
        db.session.add(new_student)
        db.session.commit()
        return student_schema.jsonify(new_student), 201
    else:
        data = Student.query.all()
        res = students_schema.dump(data)
        return jsonify(res), 200

@app.route('/students/<id>', methods=["PATCH", "GET"])
def student(id):
    if request.method == "PATCH":
        club_code = request.json['club_code']
        existing_club = Club.query.get(club_code)
        student = Student.query.get(id)
        student.clubs.append(existing_club)
        db.session.commit()
        return "Student successfully added to club"
    else:
        data = Student.query.get(id)
        res = student_schema.dump(data)
        return res, 200

@app.route('/clubs', methods=["POST", "GET"])
def clubs():
    if request.method == "POST":
        club_name = request.json['title']
        club_code = request.json['code']
        new_club = Club(club_name, club_code)
        student_id = request.json['student_id']
        student = Student.query.get(student_id)
        student.clubs.append(new_club)
        db.session.add(new_club)
        db.session.commit()
        return club_schema.jsonify(new_club), 201
    else:
        data = Club.query.all()
        res = clubs_schema.dump(data)
        return jsonify(res), 200

@app.route('/clubs/<id>', methods=["GET", "DELETE"])
def club(id):
    if request.method == "DELETE":
        db.session.query(Club).filter(Club.id == id).delete()
        db.session.commit()
        return f"Successfully deleted club with the id {id}."
    else:
        data = Club.query.get(id)
        res = club_schema.dump(data)
        return res, 200

@app.route('/sets')
def sets():
    data = Set.query.all()
    res = sets_schema.dump(data)
    return jsonify(res), 200

@app.route('/sets/<id>')
def set(id):
    data = Set.query.filter_by(club_id=id)
    res = sets_schema.dump(data)
    return jsonify(res), 200

@app.route('/flashcards', methods=["GET", "POST"])
def flashcards():
    if request.method == "POST":
        question = request.json['question']
        answer = request.json['answer']
        set_id = request.json['set_id']
        new_flashcard = Flashcard(question, answer, set_id)
        db.session.add(new_flashcard)
        db.session.commit()
        return flashcard_schema.jsonify(new_flashcard), 201
    else:
        data = Flashcard.query.all()
        res = flashcards_schema.dump(data)
        return jsonify(res), 200

@app.route('/flashcards/<id>', methods=["GET", "PATCH", "DELETE"])
def update_flashcard(id):
    if request.method == "PATCH":
        db.session.query(Flashcard).filter(Flashcard.id == id).update(request.json)
        db.session.commit()
        return request.json, 200
    elif request.method == "DELETE":
        db.session.query(Flashcard).filter(Flashcard.id == id).delete()
        db.session.commit()
        return f"Successfully delete flashcard with the id {id}."
    else:
        data = Flashcard.query.filter_by(set_id=id)
        res = flashcards_schema.dump(data)
        return jsonify(res), 200

@app.route('/messages')
def messages():
    data = Message.query.all()
    res = messages_schema.dump(data)
    return jsonify(res), 200

@app.route('/messages/<id>')
def message(id):
    data = Message.query.get(id)
    res = message_schema.dump(data)
    return res, 200

# The function below is to guarantee token won't expire when user is logged in.The function takes as an argument, the response from the /profile API call.

@app.after_request  # Ensures that the refresh_expiring_jts runs after a request has been made to the protected PROFILE endpoint
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]  # current timestamp for user
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(
            now + timedelta(minutes=30))  # 30 minutes away
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity)
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


@app.route('/token', methods=['POST'])
def create_token():
    em = request.json.get('email', None)
    pw = request.json.get('password', None)
    # Change this later => compare with database user details
    stud = Student.query.filter_by(email=em).first()
    if (not stud):
        return {'message': 'Wrong email or password'}, 401
    if (not stud.password == pw):
        return {'message': 'Wrong email or password'}, 401
        
    # create access token for particular email if login is confirmed
    access_token = create_access_token(identity=em)
    response = {'access_token': access_token, 'student_id': stud.id}
    return response, 200


@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200

@app.route('/profile')
# @jwt_required()  # prevent unauthenticated users from making requests to the API
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
        new_student = Student(full_name="harry", user_name="harrykane", email="harry@example.com", password="spurs4ever")
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
            return "There was an error adding to the db"            # pragma: no cover
    else:
        # below is just for testing purposes
        students = Student.query.order_by(Student.created_at)
        clubs = Club.query.order_by(Club.created_at)
        sets = Set.query.order_by(Set.created_at)
        messages = Message.query.order_by(Message.created_at)
        flashcards = Flashcard.query.order_by(Flashcard.created_at)
        for x in students:
            print(x.full_name, x.user_name, x.email, x.password)
        for x in clubs:
            print(x.club_name, x.club_code)
        for x in sets:
            print(x.set_name, x.private)
        for x in messages:
            print(x.content)
        for x in flashcards:
            print(x.question, x.answer)
        return "hey"        # pragma: no cover
    

if __name__ == '__main__':
    app.run(debug = True)   # pragma: no cover
