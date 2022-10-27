from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lkounzrgikkdge:10b8b7b4da003cc528748ffd5dbcbe9987af8f7526a5a766be2a77ad097c194d@ec2-52-23-131-232.compute-1.amazonaws.com:5432/d8lp0toh40kf2b' # heroku postgres db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise the db
db = SQLAlchemy(app)

# Create user model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #create a function to return a string when we add something
    def __repr__(self):
        return '<User %r>' % self.id

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

@app.route('/testdb')
def testdb():
    # create random instance of User class
    new_user = User(full_name="karl", user_name="karldudley", email="karl@example.com", password="test123")

    # store random string and url in db
    try:
        db.session.add(new_user)
        db.session.commit()
        # user_table = User.query.all()
        # return user_table
    except:
        return "There was an error adding to the db"
    

if __name__ == '__main__':
    app.run(debug = True)   # pragma: no cover
