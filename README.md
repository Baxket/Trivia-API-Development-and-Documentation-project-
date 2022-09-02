# The Trivia App of Udacity 

This is an API development and documentation project project for udacity students to test their skills learnt in the course of the fullstack nanodegree program. What this API does is to play a quiz game where users can add a quiz question and answer to the database categorizing them, search for any question with their answer and also play a quiz based on categories. After this app I hava accomplished how to build well formatted API endpoints and test it. 
This project adheres to the PEP8 style guidelines.


## API Reference

### Getting Started

- Base URL: This app is ran locally and therefore not hosted as a base url.  The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration and the fronend app is hosted at the  `http://127.0.0.1:3000/`.
- Authentication: This version of the application does not require authentication or API keys.

#### Pre-requisites and Local Development

To run this project, you must first have Python3, pip, and node installed on your local machine. The following are steps to begin with in the backend and frontend folder respectfully;

#### 1. Backend

##### Setting up the Backend
 
1. **Python** - First, install the lastest version of python on your machine.

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized.
To create a virtual follow these steps;

- **On Windows**: 
```bash
python -m venv <myenv> 
```
Next, 
```bash
myenv\Scripts\activate
```

- **On Linux**: 
```bash
$ pip install virtualenv
```
Next, 
```bash
$ virtualenv virtualenv_name
```
Next,
```bash
$ virtualenv -p /usr/bin/python3 virtualenv_name
```
Next,
```bash
$ source virtualenv_name/bin/activate
```

3.**PIP Dependencies** - After creating your virtual environment and activating it, install the required dependencies in the requirements.txt by navigating to the `/backend` directory and run this command;
```bash
pip install -r requirements.txt

```

##### Set up the database

First install Postgresql if you don't have. 

In the model.py file edit the database format by entering your database name, password and port

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```
Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```
##### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

Set your flask apps, debug and environment.

- **For Windows**
```bash
set  FLASK_APP=flaskr
set FLASK_DEBUG=1
set FLASK_ENV=development
```
- **For Linux**
```bash
export FLASK_APP=flaskr
export FLASK_DEBUG=True
export FLASK_ENV=development

```
To run the server, execute:

```bash
flask run --reload
```
The `--reload` flag will detect file changes and restart the server automatically.  

#### 2. Frontend

##### Setting up the Frontend

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected. We recommend that you **stand up the backend first**.


##### Installing Dependencies

1. **Installing Node and NPM**
   You must install Nodejs and Node Package Manager (NPM) if you haven't.

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal in the `frontend` directory and run:

```bash
npm install
```

> _tip_: `npm i`is shorthand for `npm install``

##### Required Tasks

- **Running Your Frontend in Dev Mode**

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

###  Game Play Mechanics

Currently, when a user plays the game they play up to five questions of the chosen category. If there are fewer than five questions in a category, the game will end when there are no more questions in that category.



### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 405: method is not allowed
- 404: Resource Not Found
- 422: Not Processable 


### Endpoints 
#### GET /categories
- General:
    - This fetches a dictionary of categories from the database
    - Request Arguments: None
    - Returns a list of categories objects in which the keys are the ids and the value is the corresponding string of the category, success value, and total number of categories
- Sample: `curl http://127.0.0.1:5000/categories`

```json
 {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

#### GET /questions
- General:
    - This fetches a dictionary of questions from the database
    - Request Arguments: None
    - Returns a list of category objects in which the keys are the ids and the value is the corresponding string of the category, a list of questions with their answer, category, difficulty, and id, success value, and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

```json
 {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "trivia",
      "category": 3,
      "difficulty": 3,
      "id": 58,
      "question": "what is the name of the app"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
    }
  ],
  "success": true,
  "total_questions": 17
}
```

#### DELETE /questions/{question_id}
- General:
    - This deletes a question from the database 
    - Request Arguments: question_id
    - Deletes the question of the given ID if it exists. Returns success value, and a message. 
- sample: `curl -X DELETE http://127.0.0.1:5000/question/11`
```json
{
  "message": "Successfully deleted",
  "success": true
}

```

#### POST /questions
- General:
    - This adds questions to the database
    - Request Arguments: question, answer, difficulty, and category
    - Creates a new question using the submitted question, answer, difficulty and category. Returns a success value, and a message.
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d "{\"question\":\"what is the name of this app\", \"answer\":\"Trivia app\", \"difficulty\":\"5\", \"category\":\"3\"}"`
```json
{
  "message": "Successfully added",
  "success": true
}
```

#### POST /questions/search
- General:
    - This searches through the database for questions that match the search term.
    - Request Arguments: Search term
    - Returns a list of questions with their answer, category, difficulty, and id, total number of questions, and current Category based on the search term.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d "{\"searchTerm\":\"what is the name of this app\"}"`
```json
{
  "currentCategory": 0,
  "questions": [
    {
      "answer": "Trivia app",
      "category": 3,
      "difficulty": 5,
      "id": 59,
      "question": "what is the name of this app"
    }
  ],
  "success": true,
  "totalQuestions": 1
}
```

#### GET /categories/{category_id}/questions
- General:
    - This gets every questions under a category
    - Request Arguments: category_id
    - Returns a list of questions with their answer, category, difficulty, and id, success value, a total number of questions, and the current Category.
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`

```json
 {
  "currentCategory": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```


#### POST /quizzes
- General:
    - This randomly gets questions from the quiz based on categories or all.
    - The questions fetched is not in the previous questions.
    - Request Arguments: prevous questions and quiz category
    - Fetches a new question using the category, and previous questions. 
    - Returns a list of questions with their answer, category, difficulty, and id, success value, and total number of questions
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d "{\"previous_questions\":[\"9\"], \"quiz_category\":{ \"type\":\"Science\", \"id\":\"1\" } }"`
```json
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true,
  "totalQuestions": 3
}
```
## Testing

This tests the whole API endpoints for success and failures to make sure the app will run correctly. 

To deploy the tests, navigate to the backend folder and run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
## Deploymane: N/A

## Authors

Yours truly, Richard Ablorh.

## Acknowledgements

Coach Caryn and the whole team of Udacity.



