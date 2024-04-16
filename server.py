from flask import Flask, render_template, request, jsonify, url_for, redirect
import random

app = Flask(__name__, static_url_path='/static')

current_id = 0
quiz_data = {
    "question1": "answer1",
    "question2": "answer2",
    "question3": "answer3",
    "question4": "answer4",
    "question5": "answer5",
    "question6": "answer6",
    "question7": "answer7",
    "question8": "answer8",
    "question9": "answer9",
    "question10": "answer10"
    # Add more questions and answers here
}

# Define additional options
additional_options = {
    "option1",
    "option2",
    "option3",
    "option4",
    "option5",
    "option6",
    "option7",
    "option8",
    "option9",
    "option10"
    # Add more options here
}

@app.route('/')
def index():
    return render_template('home.html')

# @app.route('/learn')
# def learn():
#     return

@app.route('/quiz-start')
def quiz_start():
    return render_template('quiz_start.html')

@app.route('/quiz')
def quiz():
     
    questions = list(quiz_data.keys())

    # Ensure there are enough questions available
    if len(questions) < 10:
        return "Not enough questions available for the quiz."

    # Randomly select 10 unique questions
    selected_questions = []
    while len(selected_questions) < 5:
        question = random.choice(questions)
        if question not in selected_questions:
            selected_questions.append(question)

    # Generate random options for each selected question
    random_options = {}
    for question in selected_questions:
        correct_answer = quiz_data[question]
        options = [correct_answer] + random.sample(additional_options, 2)
        random.shuffle(options)
        random_options[question] = options

    # Select the current question from the selected_questions
    current_question = selected_questions[0]

    return render_template('quiz.html', current_question=current_question, current_options=random_options[current_question])

@app.route('/quiz-results')
def quiz_results():
    return render_template('quiz_results.html')


@app.route('/wine-terms')
def wine_terms():
    return render_template('wine_terms.html')
 
@app.route('/food-pairings')
def wine_terms():
    return render_template('food_pairings.html')
 

if __name__ == '__main__':
    app.run(debug=True)