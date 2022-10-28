import json
from os import access
from tkinter.messagebox import RETRY
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lkounzrgikkdge:10b8b7b4da003cc528748ffd5dbcbe9987af8f7526a5a766be2a77ad097c194d@ec2-52-23-131-232.compute-1.amazonaws.com:5432/d8lp0toh40kf2b' # heroku postgres db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # Initialise the db

app.config['JWT_SECRET_KEY'] = 'Remember to change me' #Config JWT secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=3) #specifies token lifespan
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

#The function below is to guarantee token won't expire when user is logged in.The function takes as an argument, the response from the /profile API call.
@app.after_request #Ensures that the refresh_expiring_jts runs after a request has been made to the protected PROFILE endpoint
def refresh_expiring_jwts(response):
	try:
		exp_timestamp = get_jwt()["exp"] #current timestamp for user
		now = datetime.now(timezone.utc)
		target_timestamp = datetime.timestamp(now + timedelta(minutes=30)) #30 minutes away
		if target_timestamp > exp_timestamp:
			access_token = create_access_token(identity=get_jwt_identity)
			data = response.get_json()
			if type(data) is dict:
				data["access_token"] = access_token
				response.data=json.dumps(data)
		return response
	except (RuntimeError, KeyError):
		# Case where there is not a valid JWT. Just return the original response
		return response

@app.route('/token', methods=['POST'])
def create_token():
	email = request.json.get('email', None)
	password = request.json.get('password', None)
	#Change this later => compare with database user details
	if email != 'test' or password != 'test':
		return{'message': 'Wrong email or password'}, 401 #unauthorized Error
	#create access token for particular email if login is confirmed
	access_token = create_access_token(identity=email)
	response = {'access_token': access_token}
	return response, 200

@app.route('/logout', methods=['POST'])
def logout():
	response = jsonify({"message": "logout successful"})
	unset_jwt_cookies(response)
	return response, 200

@app.route('/profile')
@jwt_required() #prevent unauthenticated users from making requests to the API
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
