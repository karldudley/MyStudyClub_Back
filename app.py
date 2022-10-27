from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lkounzrgikkdge:10b8b7b4da003cc528748ffd5dbcbe9987af8f7526a5a766be2a77ad097c194d@ec2-52-23-131-232.compute-1.amazonaws.com:5432/d8lp0toh40kf2b' # heroku postgres db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

if __name__ == '__main__':
    app.run(debug = True)   # pragma: no cover
