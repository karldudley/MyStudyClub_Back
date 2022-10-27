from flask import Flask

app = Flask(__name__)

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
