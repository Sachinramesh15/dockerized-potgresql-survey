from fastapi import FastAPI, Request, HTTPException
import psycopg2

hostname = 'localhost'
database = 'new'
username = 'postgres'
pwd = 'sachcld15'
portid = 5432

app = FastAPI()

conn = psycopg2.connect(
    host=hostname,
    dbname=database,
    user=username,
    password=pwd,
    port=portid
)

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

CREATE_USER_TABLE = '''CREATE TABLE IF NOT EXISTS Users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL
);'''

INSERT_USER_TABLE = '''INSERT INTO Users (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING user_id;'''

CREATE_RESPONSES_TABLE = '''CREATE TABLE IF NOT EXISTS Responses (
    response_id SERIAL REFERENCES Users(user_id),
    answer1 VARCHAR(255) NOT NULL,
    answer2 VARCHAR(255) NOT NULL,
    answer3 VARCHAR(255) NOT NULL,
    answer4 VARCHAR(255) NOT NULL,
    answer5 VARCHAR(255) NOT NULL,
    answer6 VARCHAR(255) NOT NULL,
    answer7 VARCHAR(255) NOT NULL,
    answer8 VARCHAR(255) NOT NULL,
    answer9 VARCHAR(255) NOT NULL,
    answer10 VARCHAR(255) NOT NULL,
    answer11 VARCHAR(255) NOT NULL,
    answer12 VARCHAR(255) NOT NULL,
    answer13 VARCHAR(255) NOT NULL,
    answer14 VARCHAR(255) NOT NULL,
    answer15 VARCHAR(255) NOT NULL,
    PRIMARY KEY (response_id)
);'''

INSERT_RESPONSES_TABLE = '''INSERT INTO Responses (response_id, answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8, answer9, answer10, answer11, answer12, answer13, answer14, answer15) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

DELETE_RESPONSES = 'DELETE FROM Responses WHERE response_id = %s;'
DELETE_USER = 'DELETE FROM Users WHERE user_id = %s;'

USER_RESPONSES = '''SELECT user_id, CONCAT(first_name, ' ', last_name) AS name, answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8, answer9, answer10, answer11, answer12, answer13, answer14, answer15 
                    FROM Users JOIN Responses ON Users.user_id = Responses.response_id;'''

@app.post('/users')
async def create_user(request: Request):
    try:
        data = await request.json()
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']

        with conn:
            with conn.cursor() as curr:
                curr.execute(CREATE_USER_TABLE)
                curr.execute(INSERT_USER_TABLE, (first_name, last_name, email))
                user_id = curr.fetchone()[0]

        return {'id': user_id, 'message': f'User {first_name} {last_name} registered!'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in creating user: {str(e)}")

@app.post('/responses')
async def create_responses(request: Request):
    try:
        data = await request.json()
        user_id = data['user_id']
        answers = [data[f'answer{i}'] for i in range(1, 16)]

        with conn:
            with conn.cursor() as curr:
                curr.execute(CREATE_RESPONSES_TABLE)
                curr.execute(INSERT_RESPONSES_TABLE, (user_id, *answers))
        return {'message': 'Responses registered!'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in creating responses: {str(e)}")

@app.delete('/deleteuser')
async def delete_user(request: Request):
    try:
        data = await request.json()
        user_id = data['user_id']
        
        with conn:
            with conn.cursor() as curr:
                # Delete corresponding responses first
                curr.execute(DELETE_RESPONSES, (user_id,))
                # Delete the user
                curr.execute(DELETE_USER, (user_id,))
                if curr.rowcount == 0:
                    raise HTTPException(status_code=404, detail="User not found")

        return {'message': 'User and corresponding responses deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in deleting user: {str(e)}")

@app.get('/answers')
async def get_answers():
    try:
        with conn:
            with conn.cursor() as curr:
                curr.execute(USER_RESPONSES)
                combined_responses = curr.fetchall()
                
        return {'responses': combined_responses}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in fetching responses: {str(e)}")

@app.get('/questions')
def get_questions():
    return {'questions': questions}

@app.on_event("shutdown")
def shutdown():
    conn.close()
