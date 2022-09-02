from asyncio.windows_events import NULL
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify,json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
   

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request 
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response 

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        try:

           categories = Category.query.all()
           data = {}
           for category in categories:
              data[category.id] = category.type
   
           formatted_categories = [ category.format() for category in categories]
           return jsonify({
               
               'success':True,
               'categories': data,
               'total_categories':len(formatted_categories)
           })

        except:
            abort(404)
     





    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        try:

          page = request.args.get('page',1,type=int)# creates the pages
          start = (page-1)*10
          end = start + 10

          questions = Question.query.all()# fetch all the questions
          formatted_questions = [question.format() for question in questions] # formats qustions into a dictionary
          if len(formatted_questions[start:end]) == 0:
                #give error if no question if found
                abort(404)
                
          categories = Category.query.all()# get all categories
          data = {}
          for category in categories:
             data[category.id] = category.type # format categories into a dictionary
  
  
          return jsonify({
              'success':True,
              'questions': formatted_questions[start:end],
              'total_questions':len(formatted_questions),
              'categories': data,
              
             
          })

        except:
            abort(404)


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
          question = Question.query.filter_by(id=id).one_or_none()# fetch the questions based on category

          if question is None:#give error if no question if found
                abort(422)
          else:
            question.delete()
            
            return jsonify({
                'success':True,
                'message':"Successfully deleted"
            })

          
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():

        # get the requested argumnents     
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)

        try:

          if(question is None or 
             answer is None or 
             difficulty is None or
              category is None): #give error if argumnets are not given
                abort(404)

         
          if((question != "" and question.isspace()==False) or 
            ( answer != "" and answer.isspace()==False)): #give error if arguments has only space or nothing
            #add a new question
              new_question = Question(
                  question=question,
                  answer=answer,
                  difficulty=difficulty,
                  category=category)
              new_question.insert()
              return jsonify({
                  "success":True,
                  "message":"Successfully added"
              })   
          else:
            abort(422)     

        except:
            abort(405)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            page = request.args.get('page',1,type=int)
            start = (page-1)*10
            end = start + 10
            body = request.get_json()
            search_term = body.get('searchTerm',None)

            #give error if arguments has only space or nothing
            
            if(search_term is None or search_term.isspace() or search_term=="" ):
                abort(404)
            
            result = Question.query.filter(Question.question.ilike('%'+ search_term +'%')) # search from database
            formatted_questions = [question.format() for question in result]
            return jsonify({
                'success':True,
                'questions':formatted_questions[start:end],
                'totalQuestions':len(formatted_questions),
                'currentCategory':NULL
            })



        except:
            abort(404)
        

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def category_questions(id):
        try:
            category_questions = Question.query.filter_by(category=id).all()# get category questions
            current_category = Category.query.filter_by(id=id).one_or_none()# get current category name
            formatted_questions = [question.format() for question in category_questions]
            return jsonify({
                'success':True,
                'questions':formatted_questions,
                'total_questions':len(formatted_questions),
                'currentCategory':current_category.type
                
            })


        except:
            abort(404)




    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes',methods=['POST'])
    def quizzes():
        try:
          
          body = request.get_json()
          previousQuestions=body.get('previous_questions',None)
          quiz_category=body.get('quiz_category',None)
        
         
          json_str = json.dumps(quiz_category)
          category_json = json.loads(json_str)
         
         
          if category_json['id'] == 0:#this checks whether the selected category is all
            #this queries all questions that are not in the previous list;
                  total_questions = Question.query.count()
                  excluded_questions = Question.query.filter(Question.id.not_in(previousQuestions))
                                   
                  rand = random.randrange(0, excluded_questions.count()) #sets the random range
                
                  question = excluded_questions[rand]#get a random row from the fetched query with the random range
                  return jsonify({
                  'success':True,
                  'question':question.format(),
                  'totalQuestions':total_questions 
                    })
               
                        
          else:
                
                
              #gets the category from the database
              category = Category.query.filter(and_(Category.type==category_json['type'], Category.id == category_json['id'] )).first()
              
              if(category):
                 #   this queries all questions that are not in the previous list and are in the specified category;
                   questions = Question.query.filter(and_(Question.category==category_json['id'], Question.id.not_in(previousQuestions)))
                   total_questions = Question.query.filter(Question.category == category_json['id']).count()
               
                   # i did this because some categories has less than 5 questions which is less than the questions per play
                   # so if there are more questions, you return a question
                   if(questions.all() ):
                         
                  
                           rand = random.randrange(0, questions.count()) 
                           question = questions[rand]               
                           return jsonify({
                               'success':True,
                               'question':question.format(),
                               'totalQuestions':questions.count()
                           })

                   else:
                        # but if there are no more questions, you return a None for the front end to give you the score thats
                        #  if only the category questions are less than 5
                   
                      return jsonify({
                           'success':True,
                           'question':None,
                           'totalQuestions':questions.count()
                       })
            
                  
                    
          

        except:# if the category does not exist return error
            abort(422)



    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    #errors
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success":False,
            "error":404,
            "message":"Not found"
        }),404
    
    @app.errorhandler(422)
    def cannot_proccess(error):
        return jsonify({
            "success":False,
            "error":422,
            "message":"Cannot be processed"
        }),422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success":False,
            "error":405,
            "message":"method is not allowed"
        }),405

    return app

