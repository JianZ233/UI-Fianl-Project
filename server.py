from flask import Flask, render_template, request, jsonify, url_for, redirect, session
import random

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'nXK8vpGjZXPr9rAz5qY-1w'


current_id = 0
quiz_data = {
    "question1": {"question": "Halibut with creamy sauce", 
                  "answer": "Sauvignon Blanc", 
                  "image": "Halibut_with_cream_sauce.jpg", 
                  "explanation": "Explanation for question 1.",
                  "options": ["Sauvignon Blanc", "Chardonnay", "Pinot Grigio"]
                  },
    "question2": {"question": "Beef lasagna", 
                  "answer": "Chianti", 
                  "image": "Beef_lasagna.jpg", 
                  "explanation": "Explanation for question 2.",
                  "options": ["Sauvignon Blanc", "Chianti", "Cabernet Sauvignon"]
                  },
    "question3": {"question": "Pear goat cheese salad", 
                  "answer": "Sauvignon Blanc", 
                  "image": "Pear_goat_cheese_salad.jpg", 
                  "explanation": "Explanation for question 3.",
                  "options": ["Sauvignon Blanc", "Pinot Noir", "Rosé"]
                  },
    "question4": {"question": "Parmesan cheese and crackers", 
                  "answer": "Chianti Classico", 
                  "image": "Cheese_and_crackers.jpg", 
                  "explanation": "Explanation for question 4.",
                  "options": ["Chardonnay", "Prosecco", "Chianti Classico"]
                  },
    "question5": {"question": "salted caramel toffee bark", 
                  "answer": "Ruby Port", 
                  "image": "Salted_caramel_toffee_bark.jpg", 
                  "explanation": "Explanation for question 5.",
                  "options": ["Ruby Port", "Moscato d'Asti", "Late Harvest Riesling"]
                  },
    # Add more questions and answers here
}

# Define additional options, each will be a wine and descriptor
# descriptor should have dry, full body, etc.
additional_options = {
    "Chianti": {"explanation": "This pairs well with tomato-based sauces and the richness of beef in the lasagna."},
    "Cabernet Sauvignon": {"explanation": "Its bold flavors and tannins complement the savory richness."},
    "Pinot Grigio": {"explanation": "This lighter-bodied white wine can provide a refreshing contrast to the richness."},
    "Sauvignon Blanc": {"explanation": " Its crisp acidity and citrus notes can complement the fresh flavors of the salad, especially the pear."},
    "Pinot Noir": {"explanation": "Its light to medium body and red fruit flavors can complement the sweetness and creaminess."},
    "Rosé": {"explanation": "A dry rosé with fruity and floral notes can provide a refreshing contrast to the creaminess and sweetness."},
    "Chardonnay": {"explanation": "A full-bodied Chardonnay with oak aging can complement the nutty and salty flavors."},
    "Prosecco": {"explanation": "The crisp acidity and effervescence of Prosecco can contrast with the richness."},
    "Chianti Classico": {"explanation": "The acidity and fruitiness of Chianti Classico can cut through the richness."},
    "Ruby Port": {"explanation": "The rich, fruity flavors of Ruby Port can complement the sweetness of the toffee and caramel while contrasting with the saltiness."},
    "Moscato d'Asti": {"explanation": "The light, sweet, and slightly effervescent character of Moscato d'Asti can provide a delightful contrast to the richness and saltiness of the bark."},
    "Late Harvest Riesling": {"explanation": "The intense sweetness and honeyed notes of Late Harvest Riesling can complement the caramel and toffee flavors while balancing the saltiness."}
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
    session['total_questions'] = 5
    session['current_index'] = 0
    session['score'] = 0
    session['selected_questions'] = random.sample(list(quiz_data.values()), session['total_questions'])
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    if 'selected_questions' not in session or session['current_index'] >= session['total_questions']:
        return redirect(url_for('quiz_results'))
    
    current_question = session['selected_questions'][session['current_index']]
    correct_option = current_question['answer']
    options = [correct_option]  # Start with the correct answer

    while len(options) < 3:  #three options
        potential_option = random.choice(list(additional_options.keys()))
        if potential_option not in options:
            options.append(potential_option)
    random.shuffle(options)

    # Get explanations for each option
    options_with_explanations = [{'option': opt, 'explanation': additional_options[opt]['explanation']} for opt in options]

    return render_template('quiz.html', question=current_question, options=options_with_explanations)


    # questions = list(quiz_data.keys())

    # # Ensure there are enough questions available
    # if len(questions) < 10:
    #     return "Not enough questions available for the quiz."

    # # Randomly select 10 unique questions
    # selected_questions = []
    # while len(selected_questions) < 5:
    #     question = random.choice(questions)
    #     if question not in selected_questions:
    #         selected_questions.append(question)

    # # Generate random options for each selected question
    # random_options = {}
    # options = []
    # for question in selected_questions:
    #     correct_answer = quiz_data[question]
    #     c = correct_answer['answer']
    #     options = random.sample(additional_options, 2)
    #     options.append(c)
    #     random.shuffle(options)
    #     random_options[question] = options

    # # Select the current question from the selected_questions
    # current_question = selected_questions[0]

    # return render_template('quiz.html', current_question=quiz_data[current_question], current_options=random_options[current_question])

@app.route('/check-answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    selected_option = data['answer']
    correct_answer = session['selected_questions'][session['current_index']]['answer']
    
    if selected_option == correct_answer:
        session['score'] += 1
    
    session['current_index'] += 1
    if session['current_index'] >= session['total_questions']:
        return jsonify(endQuiz=True, correctAnswer=correct_answer)
    else:
        next_question = session['selected_questions'][session['current_index']]
        return jsonify(
            endQuiz=False,
            correctAnswer=correct_answer,
            question=next_question['question'],
            image=next_question['image'],
            options=[{'option': opt, 'explanation': additional_options[opt]['explanation']} for opt in next_question['options']]
        )

    data = request.get_json()
    selected_option = data['answer']
    correct_answer = session['selected_questions'][session['current_index']]['answer']
    
    if selected_option == correct_answer:
        session['score'] += 1
    
    session['current_index'] += 1
    if session['current_index'] >= session['total_questions']:
        return jsonify(endQuiz=True, correctAnswer=correct_answer)
    else:
        next_question = session['selected_questions'][session['current_index']]
        return jsonify(
            endQuiz=False,
            correctAnswer=correct_answer,
            question=next_question['question'],
            image=next_question['image'],
            options=[{'option': opt, 'explanation': additional_options[opt]['explanation']} for opt in next_question['options']]
        )
        
    # user_answer = request.form['answer']
    # correct_answer = request.form['correct_answer']
    # explanation = request.form['explanation']

    # is_correct = user_answer == correct_answer

    # return jsonify({'user_answer': user_answer, 'correct_answer': correct_answer, 'explanation': explanation, 'is_correct': is_correct})

@app.route('/quiz-results')
def quiz_results():
    score = session.get('score', 0)
    total = session.get('total_questions', 5)  # Ensure this matches the number of questions initially set
    # Clear the session 
    session.clear()
    return render_template('quiz_results.html', score=score, total=total)

@app.route('/wine-terms')
def wine_terms():
    return render_template('wine_terms.html')

@app.route('/spectrum')
def spectrum():
    return render_template('spectrum.html')
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