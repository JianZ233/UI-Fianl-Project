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
                  "explanation": "With its roots deeply entrenched in Italian tradition, this red elixir harmonizes seamlessly with the robust tomato-based sauces and the succulent richness of beef enveloped within the layers of lasagna.",
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
    "Chianti": {"explanation": "Chianti's bold character and robust flavors of ripe red fruit and earthiness make it ideal for hearty dishes, but its strength may overshadow delicate flavors and might not pair well with light seafood or delicate salads."},
    "Cabernet Sauvignon": {"explanation": "Cabernet Sauvignon's full body and rich dark fruit flavors complement savory dishes, but its robust nature can overwhelm lighter fare, so it's not the best choice for delicate fish or subtle dishes."},
    "Pinot Grigio": {"explanation": "Pinot Grigio's crisp acidity and refreshing citrus notes offer versatility, pairing well with various dishes, yet its subtle flavors may be overshadowed by intensely flavored fare, such as heavily spiced dishes or very rich, creamy sauces."},
    "Sauvignon Blanc": {"explanation": "Sauvignon Blanc's zesty citrus aromas and vibrant acidity make it perfect for fresh salads and seafood, though its lightness may not stand up to heavier dishes like red meats or creamy pastas."},
    "Pinot Noir": {"explanation": "Pinot Noir's silky texture and elegant red fruit flavors pair well with dishes balancing sweetness and savory elements, but its medium body may lack the intensity for bolder flavors and might not be the best choice for heavily spiced or heavily sauced dishes."},
    "Rosé": {"explanation": "Rosé's delicate hue and fruity aromas offer a refreshing drinking experience, complementing light, summery fare, yet its delicate nature may be overshadowed by richer dishes or strong-flavored foods."},
    "Chardonnay": {"explanation": "Chardonnay's rich texture and vibrant flavors of ripe fruits and toasted oak make it perfect for creamy dishes, though its oak aging can overpower delicate flavors, so it's not the best choice for subtle seafood or light salads."},
    "Prosecco": {"explanation": "Prosecco's effervescence and fruity aromas provide a refreshing palate cleanse, ideal for light appetizers or as an aperitif, yet it may lack the complexity for more substantial dishes and may not pair well with heavily spiced foods or very rich dishes."},
    "Chianti Classico": {"explanation": "Chianti Classico's vibrant acidity and fruity flavors pair excellently with classic Italian cuisine, striking a perfect balance of acidity and richness, but it may not be the best choice for very spicy dishes or overly sweet desserts."},
    "Ruby Port": {"explanation": "Ruby Port's luscious sweetness and intense flavors make it a luxurious indulgence, perfect for pairing with rich desserts and savory cheeses, but it might overwhelm lighter dishes or delicate flavors."},
    "Moscato d'Asti": {"explanation": "Moscato d'Asti's delicate sweetness and floral aromas make it a delightful choice for pairing with fresh fruit, light desserts, or enjoying on its own, but it may not pair well with very savory or spicy dishes."},
    "Late Harvest Riesling": {"explanation": "Late Harvest Riesling's opulent sweetness and vibrant acidity make it a perfect match for rich desserts or pungent cheeses, but it might not be the best choice for very light or delicate dishes."}
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
    return render_template('quiz_start.html')
    # return redirect(url_for('quiz'))

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

    correct=False
    data = request.get_json()
    selected_option = data['answer']
    correct_answer = session['selected_questions'][session['current_index']]['answer']
    
    if selected_option == correct_answer:
        correct=True
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
            options=[{'option': opt, 'explanation': additional_options[opt]['explanation']} for opt in next_question['options']],
            correct=correct
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

@app.route('/pairings')
def pairings():
    return render_template('food-pairings.html')
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