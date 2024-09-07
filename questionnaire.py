from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Dict
import psycopg2


app = FastAPI()

DATABASE_URL = "postgresql://postgres:sachcld15@localhost:5432/questionnaire"

class User(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr

class Response(BaseModel):
    id: int
    user_id: int
    answer1: str
    answer2: str
    answer3: str
    answer4: str
    answer5: str
    answer6: str
    answer7: str
    answer8: str
    answer9: str
    answer10: str
    answer11: str
    answer12: str
    answer13: str
    answer14: str
    answer15: str


questions = {
    1: 'How many hours a day do you spend on your smartphone?',
    2: 'What genre of movies do you enjoy the most?',
    3: 'How often do you exercise in a week?',
    4: 'What is your dream vacation destination?',
    5: 'How do you stay informed about current events?',
    6: 'What is your favorite type of cuisine?',
    7: 'What is your favorite sport?',
    8: 'Which team do you support in the IPL?',
    9: 'What is your favorite hobby?',
    10: 'What was your favorite subject in school?',
    11: 'What is your long-term career goal?',
    12: 'What skill would you most like to learn or improve?',
    13: 'How often do you travel for leisure?',
    14: 'What is your favorite car brand?',
    15: 'What is your age group?'
}

@app.post("/submit_survey/", response_model=Dict[str, str])
def submit_survey(user: User, responses: List[Response]):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # Insert user
        user_query = "INSERT INTO users (firstname, lastname, email) VALUES (%s, %s, %s) RETURNING id"
        cur.execute(user_query, (user.firstname, user.lastname, user.email))
        user_id = cur.fetchone()[0]

        # Insert responses
        for response in responses:
            response_query = "INSERT INTO responses (user_id,answer1, answer2,answer3 ,answer4 ,answer5 ,answer6 ,answer7,answer8,answer9 ,answer10 ,answer11 ,answer12 ,answer13, answer14, answer15) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(response_query, (user_id, response.answer1,response.answer2,response.answer3,response.answer4,response.answer5,response.answer6,response.answer7,response.answer8,response.answer9,response.answer10,response.answer11,response.answer12,response.answer13,response.answer14,response.answer15,))

        conn.commit()
        conn.close()

        return {"message": "Survey submitted successfully!"}
    except: raise HTTPException(status_code=400, detail="Error:survey submission failed.")

@app.get("/questions/", response_model=Dict[int, str])
def get_questions():
    return questions

@app.get("/")
def read_root():
    return {"message": "Welcome to the Survey API"}
