from app import Student, Flashcard

def test_profile_route(api):
    response = api.get("/profile")
    assert response.status == "200 OK"
    assert "Karlos" and "Hello! I'm a full stack developer that loves Python and React" in response.text

def test_index_route(api):
    response = api.get("/")
    assert response.status == "200 OK"
    assert "<h1 style=\"color:#B0E0E6;\">Welcome to the myStudyClub server</h1>"
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
    "<h3>/flashcards/:id</h3>" in response.text

def test_students_route(api):
    response = api.get("/students")
    assert response.status_code == 200
def test_student_clubs_route(api):
    response = api.get("/studentclubs")
    assert response.status_code == 200
def test_clubs_route(api):
    response = api.get("/clubs")
    assert response.status_code == 200
def test_sets_route(api):
    response = api.get("/sets")
    assert response.status_code == 200
def test_messages_route(api):
    response = api.get("/messages")
    assert response.status_code == 200
def test_flashcards_route(api):
    response = api.get("/flashcards")
    assert response.status_code == 200

def test_student_route(api):
    response = api.get("/students/1")
    assert response.status_code == 200
def test_student_club_route(api):
    response = api.get("/studentclubs/1")
    assert response.status_code == 200
def test_club_route(api):
    response = api.get('/clubs/1')
    assert response.status_code == 200
def test_set_route(api):
    response = api.get("/sets/1")
    assert response.status_code == 200
def test_message_route(api):
    response = api.get("/messages/1")
    assert response.status_code == 200
def test_flashcard_route(api):
    response = api.get("/flashcards/1")
    assert response.status_code == 200

def test_new_student_route(api):
    response = api.post("/students")
    assert response.status_code == 400

    data = {
        "full_name": "karl",
        "user_name": "karldudley",
        "email": "karldudley@gmail.com",
        "password": "test123"
    }

    response = api.post("/students", json=data)

    assert response.status_code == 201

def test_new_flashcard_route(api):
    response = api.post("/flashcards")
    assert response.status_code == 400

    data = {
        "question": "what is the capital of spain",
        "answer": "madrid",
        "set_id": 2,
    }

    response = api.post("/flashcards", json=data)

    assert response.status_code == 201


def test_new_student():
    student = Student('karl', 'karldudley', 'karl@example.com', 'test123')
    assert student.email == 'karl@example.com'
    assert student.password == 'test123'

def test_new_flashcard():
    fc = Flashcard('What is the capital of Spain', 'Madrid', 5)
    assert fc.question == 'What is the capital of Spain'
    assert fc.answer == 'Madrid'
    assert fc.set_id == 5
