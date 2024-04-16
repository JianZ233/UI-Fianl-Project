from flask import Flask, render_template, request, jsonify, url_for, redirect
import random

app = Flask(__name__, static_url_path='/static')

current_id = 0
quiz_data = {
    "question1": {"question": "Halibut with creamy sauce", "answer": "RED WINE", "image": "Halibut_with_cream_sauce.jpg", "explanation": "Explanation for question 1."},
    "question2": {"question": "Halibut with creamy sauce", "answer": "RED WINE", "image": "Halibut_with_cream_sauce.jpg", "explanation": "Explanation for question 1."},
    "question3": {"question": "Halibut with creamy sauce", "answer": "RED WINE", "image": "Halibut_with_cream_sauce.jpg", "explanation": "Explanation for question 1."},
    "question4": {"question": "Halibut with creamy sauce", "answer": "RED WINE", "image": "Halibut_with_cream_sauce.jpg", "explanation": "Explanation for question 1."},
    "question5": {"question": "Halibut with creamy sauce", "answer": "RED WINE", "image": "Halibut_with_cream_sauce.jpg", "explanation": "Explanation for question 1."},
    "question6": {"question": "Halibut with creamy sauce", "answer": "RED WINE", "image": "Halibut_with_cream_sauce.jpg", "explanation": "Explanation for question 1."},
    "question7": {"question": "Halibut with creamy sauce", "answer": "RED WINE", "image": "Halibut_with_cream_sauce.jpg", "explanation": "Explanation for question 1."},
    "question8": {"question": "Halibut with creamy sauce", "answer": "RED WINE", "image": "Halibut_with_cream_sauce.jpg", "explanation": "Explanation for question 1."},
    "question9": {"question": "Halibut with creamy sauce", "answer": "RED WINE", "image": "Halibut_with_cream_sauce.jpg", "explanation": "Explanation for question 1."},
    "question10": {"question": "Halibut with creamy sauce", "answer": "RED WINE", "image": "Halibut_with_cream_sauce.jpg", "explanation": "because red wine"}
    # Add more questions and answers here
}

# Define additional options, each will be a wine and descriptor
# descriptor should have dry, full body, etc.
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
    options = []
    for question in selected_questions:
        correct_answer = quiz_data[question]
        c = correct_answer['answer']
        options = random.sample(additional_options, 2)
        options.append(c)
        random.shuffle(options)
        random_options[question] = options

    # Select the current question from the selected_questions
    current_question = selected_questions[0]

    return render_template('quiz.html', current_question=quiz_data[current_question], current_options=random_options[current_question])

@app.route('/check-answer', methods=['POST'])
def check_answer():
    user_answer = request.form['answer']
    correct_answer = request.form['correct_answer']
    explanation = request.form['explanation']

    is_correct = user_answer == correct_answer

    return jsonify({'user_answer': user_answer, 'correct_answer': correct_answer, 'explanation': explanation, 'is_correct': is_correct})

@app.route('/quiz-results')
def quiz_results():
    return render_template('quiz_results.html')

# # check navbar in examples from lecture
# @app.route('/terms')
# def terms():
#     return
 
# @app.route('/types')
# def types():

#     return

# @app.route('/pairings')
# def types():

#     return

if __name__ == '__main__':
    app.run(debug=True)