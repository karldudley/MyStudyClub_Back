from urllib import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lkounzrgikkdge:10b8b7b4da003cc528748ffd5dbcbe9987af8f7526a5a766be2a77ad097c194d@ec2-52-23-131-232.compute-1.amazonaws.com:5432/d8lp0toh40kf2b' # heroku postgres db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise the db
db = SQLAlchemy(app)

#Config JWT secret key
app.config['JWT_SECRET_KEY'] = 'Remember to change me'
jwt = JWTManager(app)


# Create user model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #create a function to return a string when we add something
    def __repr__(self):
        return '<User %r>' % self.id

@app.route('/')
def index():
    return "Welcome to the myStudyClub Server!"

@app.route('/token', methods=['POST'])
def create_token():
	email = request.json.get('email', None)
	password = request.json.get('password', None)
	#Change this later to compare with database
	if email != 'test' or password != 'test':
		return{'msg': 'wrong email or password'}, 401
	
	access_token = create_access_token(identity=email)
	response = {'access_token': access_token}
	return response


@app.route('/profile')
def my_profile():
    response_body = {
        "name": "Karlos",
        "about" :"Hello! I'm a full stack developer that loves Python and React"
    }
    return response_body

@app.route('/testdb')
def testdb():
    user_table = User.query.all()
    # for url in table:
    #     print(url.url)
    # table = "test"
    return user_table

if __name__ == '__main__':
    app.run(debug = True)   # pragma: no cover
