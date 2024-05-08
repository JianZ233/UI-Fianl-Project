from flask import Flask, render_template, request, jsonify, url_for, redirect, session
import random

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'nXK8vpGjZXPr9rAz5qY-1w'


current_id = 0
quiz_data = {
    "question1": {"question": "Halibut with Creamy Sauce", 
                  "answer": "Chardonnay - white, full-bodied, dry", 
                  "image": "Halibut_with_cream_sauce.jpg", 
                  "explanation": "Explanation for question 1.",
                  "options": ["Sauvignon Blanc - white, light-bodied, dry", "Chardonnay - white, full-bodied, dry", "Pinot Grigio - white, light-bodied, dry"]
                  },
    "question2": {"question": "Beef Lasagna", 
                  "answer": "Shiraz - red, full-bodied, dry", 
                  "image": "Beef_lasagna.jpg", 
                  "explanation": "With its roots deeply entrenched in Italian tradition, this red elixir harmonizes seamlessly with the robust tomato-based sauces and the succulent richness of beef enveloped within the layers of lasagna.",
                  "options": ["Sauvignon Blanc - white, light-bodied, dry", "Shiraz - red, full-bodied, dry", "Pinot Noir - red, light-bodied, dry"]
                  },
    "question3": {"question": "Pear Goat Cheese Salad", 
                  "answer": "Sauvignon Blanc - white, light-bodied, dry", 
                  "image": "Pear_goat_cheese_salad.jpg", 
                  "explanation": "Explanation for question 3.",
                  "options": ["Riesling - white, sweet, aromatic", "Pinot Noir - red, light-bodied, dry", "Sauvignon Blanc - white, light-bodied, dry"]
                  },
    "question4": {"question": "Mushroom Risotto", 
                  "answer": "Pinot Noir - red, light-bodied, dry", 
                  "image": "image-1719.webp", 
                  "explanation": "Explanation for question 4.",
                  "options": ["Chardonnay - white, full-bodied, dry", "Pinot Noir - red, light-bodied, dry", "Vin Santo - white, full-bodied, sweet"]
                  },
    "question5": {"question": "Fruit Pizza Cookies", 
                  "answer": "Vin Santo - white, full-bodied, sweet", 
                  "image": "fruit_based_desserts.jpg", 
                  "explanation": "Explanation for question 5.",
                  "options": ["Vin Santo - white, full-bodied, sweet", "Pinot Grigio - white, light-bodied, dry", "Riesling - white, sweet, aromatic"]
                  },
    # Add more questions and answers here
}

answer_data = {
    "Chardonnay - white, full-bodied, dry": "Chardonnay pairs well because its citrusy notes and subtle oakiness complement the creamy sauce and delicate flavor of the flaky fish, unlike Pinot Grigio and Sauvignon Blanc, which pair better with lighter dishes.",
    "Shiraz - red, full-bodied, dry": "Shiraz harmonizes seamlessly with the robust tomato-based sauces and the herbaceous richness of beef. The dark fruit flavours and peppery spice profile of the Shiraz compliments the herbs and spiciness of the dish best out of the 3.",
    "Sauvignon Blanc - white, light-bodied, dry": "Sauvignon Blanc's crisp acidity and fruity aromas complement the sweetness of pears and the tanginess of goat cheese, creating a refreshing and balanced flavor profile. The Riesling would have been too sweet and the Pinot Noir pair better with red meat.",
    "Pinot Noir - red, light-bodied, dry": "Pinot Noir pairs well with the earthy flavors of mushrooms and the creamy texture of risotto. Its light body and bright acidity complement the dish without overpowering it, whereas Vin Santo would have been too sweet and Chardonnay too heavy.",
    "Vin Santo - white, full-bodied, sweet": "Vin Santo's fruit-like sweetness and nutty undertones complement the fruit pizza cookies, providing a delightful contrast and enhancing the dessert's overall enjoyment. Whereas, Pinot Grigio and Riesling would have been too light for the sweet and rich dessert."
}

# Define additional options, each will be a wine and descriptor
# descriptor should have dry, full body, etc.
additional_options = {
    "Chardonnay - white, full-bodied, dry": {"explanation": "Full-bodied white wine that is smooth and subtly oaked, usually with notes of vanilla and butter."},
    "Cabernet Sauvignon - red, full-bodied, dry": {"explanation": "Cabernet Sauvignon's full body and rich dark fruit flavors complement savory dishes, but its robust nature can overwhelm lighter fare, so it's not the best choice for delicate fish or subtle dishes."},
    "Pinot Grigio - white, light-bodied, dry": {"explanation": "Light-bodied, dry, white wine usually crisp, with citrus fruit, apples and a hint of spice. Best with lighter and fresher flavors."},
    "Sauvignon Blanc - white, light-bodied, dry": {"explanation": "Light, crisply dry, herbal, and fragrant white wine, that usually has a mellow color and a high acidity to add to its sense of refreshment."},
    "Pinot Noir - red, light-bodied, dry": {"explanation": "Light-bodied red wine that is dry, with bright acidity and has complex flavors that include cherry, raspberry, mushroom and forest floor, plus vanilla and baking spice when aged in French oak. Best with mushrooms and roasted meats."},
    "Shiraz - red, full-bodied, dry": {"explanation": "Full, red, rich, bold with aromatic notes of smoke, pepper spice, plum, leather, licorice, chocolate, and black fruit. Best with red meat."},
    "Merlot - red, full-bodied, dry": {"explanation": "Full and dry red wine that usually has a fruit-forward, velvety, rich, and oaky taste. Best with roasted vegetables or lean beef."},
    "Ruby Port - red, full-bodied, sweet": {"explanation": "A red wine traditionally enjoyed as a dessert wine with notes of plum, chocolate, raisin, black cherry. Best with savory desserts or stinky cheeses."},
    "Vin Santo - white, full-bodied, sweet": {"explanation": "A full-bodied, typically very sweet white dessert wine with aromas of hazelnut, caramel, honey, tropical fruit, perfume and dried apricot. Best with fruit based desserts."},
    "Riesling - white, sweet, aromatic": {"explanation": "This light-bodied, sweet, aromatic white wine offers primary fruit aromas of orchard fruits like nectarine, apricot, honey-crisp apple, and pear. Best with spicy foods and creamy sauces."}
}

wines={
    'Chardonnay':{
        'wine_name':'Chardonnay',
        'wine_type':'White',
        'wine_desc':'Full-bodied and dry white wine that is <b>creamy, smooth and subtly oaked</b>, usually with notes of vanilla and butter.'
    },
    'Cabernet Sauvignon':{
        'wine_name':'Cabernet Sauvignon',
        'wine_type':'Red',
        'wine_desc':'Full and dry red wine that is <b>rich and acidic</b>. It tends to showcase currants, cherry, and brambly berry liqueur, and, if it\'s been aged in new oak, aromas, and flavors of vanilla and chocolate.'
    },
    'Sauvignon Blanc':{
        'wine_name':'Sauvignon Blanc',
        'wine_type':'White',
        'wine_desc':'<b>Light, crisply dry, herbal, and fragrant</b> white wine, that usually has a mellow color and a <b>high acidity</b> to add to its sense of refreshment.'
    },
    'Lambrusco di Sorbara':{
        'wine_name':'Lambrusco di Sorbara',
        'wine_type':'Red',
        'wine_desc': 'A <b>light and floral red wine</b> that is dry but has aromas of orange blossom, mandarin orange, cherries, violets, and watermelon.'
    },
    'Vin Santo':{
        'wine_name':'Vin Santo',
        'wine_type':'White',
        'wine_desc':'A full-bodied, typically very sweet white dessert wine, <b>almost fruit-like</b>, with aromas of hazelnut, caramel, honey, tropical fruit, perfume and dried apricot.'
    },
    'Dornfelder':{
        'wine_name':'Dornfelder',
        'wine_type':'Red',
        'wine_desc':'A full-bodied, sweet red wine that is <b>heavy and rich</b>, with delicious flavor of cherries, red berries and plums.'    
    },
    'Riesling':{
        'wine_name':'Riesling',
        'wine_type':'White',
        'wine_desc':'This <b>sweet, light, and refreshing</b> white wine offers primary aromas of orchard fruits like nectarine, apricot, honey-crisp apple, and pear.'
    },
    'Ruby Port':{
        'wine_name':'Ruby Port',
        'wine_type':'Red',
        'wine_desc':'A red wine traditionally enjoyed as a dessert wine, that is <b>savoury and tangy</b>, with notes of plum, chocolate, raisin, black cherry.'
    },
    'Pinot Noir':{
        'wine_name':'Pinot Noir',
        'wine_type':'Red',
        'wine_desc':' Light-bodied red wine that is dry, with bright acidity and has complex flavors that include cherry, raspberry, mushroom and forest floor, plus vanilla and baking spice when aged in French oak. <b> Best with mushrooms and roasted meats </b>'
    },
    'Pinot Grigio':{
        'wine_name':'Pinot Grigio',
        'wine_type':'White',
        'wine_desc':'Light-bodied, dry, white wine usually crisp, with citrus fruit, apples and a hint of spice. <b> Best with lighter and fresher flavors </b>'
    },
    'Merlot':{
        'wine_name':'Merlot',
        'wine_type': 'Red',
        'wine_desc':'Full and dry red wine that usually has a fruit-forward, velvety, rich, and oaky taste. <b> Best with roasted vegetables or lean beed </b>'
    },
    'Shiraz':{
        'wine_name':'Shiraz',
        'wine_type': 'Red',
        'wine_desc': 'A <b>full-bodied, dry, and rich red wine</b> with aromatic notes of smoke, pepper spice, plum, leather, licorice, chocolate, and black fruit.'
    }

}

wines_food={
    'Chardonnay':{
        'wine_name':'Chardonnay',
        'wine_type':'White',
        'wine_desc':'Full-bodied and dry white wine that is creamy, so <b>pairs best with creamy dishes, mild proteins, and sweet-savoury tastes.</b>'
    },
    'Cabernet Sauvignon':{
        'wine_name':'Cabernet Sauvignon',
        'wine_type':'Red',
        'wine_desc':'Full and dry red wine that is <b>rich and acidic, so pairs best with richer and heartier foods.</b>'
    },
    'Sauvignon Blanc':{
        'wine_name':'Sauvignon Blanc',
        'wine_type':'White',
        'wine_desc':'Light, crisply dry, and <b>herbal</b> white wine with <b>high acidity</b>, making it refreshing and <b>pair best with tangy vegetables and less creamy, milder flavors.</b>'
    },
    'Lambrusco di Sorbara':{
        'wine_name':'Lambrusco di Sorbara',
        'wine_type':'Red',
        'wine_desc': 'A light and floral red wine that is dry but has aromas of orange blossom, mandarin orange, cherries, violets, and watermelon. <b>Best with creamier dishes or cured meats </b>'
    },
    'Vin Santo':{
        'wine_name':'Vin Santo',
        'wine_type':'White',
        'wine_desc':'A full-bodied, typically very sweet white dessert wine with aromas of hazelnut, caramel, honey, tropical fruit, perfume and dried apricot. <b>Best with fruit based desserts </b>'
    },
    'Dornfelder':{
        'wine_name':'Dornfelder',
        'wine_type':'Red',
        'wine_desc':'A sweet red wine with delicious flavor of cherries, red berries and plums.<b> Best with meat-based dishes </b>'    
    },
    'Riesling':{
        'wine_name':'Riesling',
        'wine_type':'White',
        'wine_desc':'This sweet, light, aromatic white wine <b>pairs best with similarly sweet and lighter, acidic vegetables.</b>'
    },
    'Ruby Port':{
        'wine_name':'Ruby Port',
        'wine_type':'Red',
        'wine_desc':'A red wine traditionally enjoyed as a dessert wine with notes of plum, chocolate, raisin, black cherry. <b> Best with savory desserts or stinky cheeses </b>'
    },
    'Pinot Noir':{
        'wine_name':'Pinot Noir',
        'wine_type':'Red',
        'wine_desc':' Light-bodied red wine that is dry, with bright acidity. <b> Best with mushrooms, roasted meats, and flaky seafood.</b>'
    },
    'Pinot Grigio':{
        'wine_name':'Pinot Grigio',
        'wine_type':'White',
        'wine_desc':'Light-bodied, dry, white wine usually crisp, so <b> pairs best with lighter and fresher seafood.</b>'
    },
    'Merlot':{
        'wine_name':'Merlot',
        'wine_type': 'Red',
        'wine_desc':'Full and dry red wine that usually has a fruit-forward, velvety, rich, and oaky taste. <b> Best with lean red meats and rich, creamy flavors.</b>'
    },
    'Shiraz':{
        'wine_name':'Shiraz',
        'wine_type': 'Red',
        'wine_desc': 'A full-bodied, dry, and rich red wine that <b>pairs best with red meat and tangy sauces.</b>'
    }

}


red_spectrum = {
    'type': 'red_spectrum',
    'title': 'Red Wines',
    'labeltop': 'Full',
    'labelright':'Sweet',
    'labelbottom':'Light',
    'labelleft':'Dry',
    'topright': wines['Dornfelder'],
    'topleft': wines['Cabernet Sauvignon'],
    'bottomright': wines['Ruby Port'],
    'bottomleft': wines['Lambrusco di Sorbara'],
    'imgtopright': 'dornfelder.jpg',
    'imgtopleft': 'Cabernet Sauvignon.png',
    'imgbottomright': 'Ruby Port.jpg',
    'imgbottomleft': 'lambrusco.jpg',
    'hrefback': '/wine-terms?section=redwhite-buffer',
    'back': '< Spectrum Overview',
    'hrefnext': '/wine-terms?section=white-spectrum',
    'next': 'White Wine Spectrum >'
}

white_spectrum = {
    'type': 'white_spectrum',
    'title': 'White Wines',
    'labeltop': 'Full',
    'labelright':'Sweet',
    'labelbottom':'Light',
    'labelleft':'Dry',
    'topright': wines['Vin Santo'],
    'topleft': wines['Chardonnay'],
    'bottomright': wines['Riesling'],
    'bottomleft': wines['Sauvignon Blanc'],
    'imgtopright': 'vinsanto.jpg',
    'imgtopleft': 'Chardonnay.jpeg',
    'imgbottomright': 'Riesling.jpeg',
    'imgbottomleft': 'Sauvignon Blanc.png',
    'hrefback': '/wine-terms?section=red-spectrum',
    'back': '< Red Wine Spectrum',
    'hrefnext': '/wine-terms?section=fullspectrum',
    'next': 'Full Spectrum >'
}

basic_spectrum = {
    'type': 'basic_spectrum',
    'title': 'Basic Spectrum',
    'labeltop': 'Full',
    'labelright':'Sweet',
    'labelbottom':'Light',
    'labelleft':'Dry',
    'topright': wines['Vin Santo'],
    'topright2': wines['Dornfelder'],
    'topleft': wines['Chardonnay'],
    'topleft2': wines['Cabernet Sauvignon'],
    'bottomright': wines['Riesling'],
    'bottomright2': wines['Ruby Port'],
    'bottomleft': wines['Sauvignon Blanc'],
    'bottomleft2': wines['Lambrusco di Sorbara'],
    'imgtopright': 'redwhite1.jpg',
    'imgtopleft': 'redwhite3.jpg',
    'imgbottomright': 'redwhite2.jpeg',
    'imgbottomleft': 'redwhite4.jpg',
    'hrefback': '/wine-terms?section=white-spectrum',
    'back': '< White Wine Spectrum',
    'hrefnext': '/food-pairings-summary',
    'next': 'Learn about food pairings >'
}

seafood = {
    'title': 'Seafood',
    'labeltop': 'Creamy',
    'labelright':'Flaky',
    'labelbottom':'Acidic',
    'labelleft':'Not Flaky',
    'topright': wines_food['Chardonnay'],
    'topleft': wines_food['Sauvignon Blanc'],
    'bottomright2': wines_food['Pinot Noir'],
    'bottomleft': wines_food['Pinot Grigio'],
    'imgtopright': 'seafood_moreflaky_creamy.jpg',
    'imgtopleft': 'seafood_lessflaky_creamy.jpg',
    'imgbottomright': 'seafood_moreflaky_acidic.jpg',
    'imgbottomleft': 'seafood_lessflaky_acidic.jpg',
    'hrefnext': '/food-pairings?section=meat',
    'next': 'Meat pairings >'
}

meat = {
    'title': 'Meat',
    'labeltop': 'Creamy',
    'labelright':'Bloody',
    'labelbottom':'Acidic',
    'labelleft':'Less Bloody',
    'topright': wines_food['Merlot'],
    'topleft': wines_food['Chardonnay'],
    'bottomright': wines_food['Shiraz'],
    'bottomright2': wines_food['Cabernet Sauvignon'],
    'bottomleft': wines_food['Sauvignon Blanc'],
    'imgtopright': 'meat_red_creamy.jpg',
    'imgtopleft': 'meat_white_creamy.jpg',
    'imgbottomright': 'meat_red_acidic.jpg',
    'imgbottomleft': 'meat_white_acidic.jpg',
    'hrefback': '/food-pairings?section=seafood',
    'back': '< Seafood pairings',
    'hrefnext': '/food-pairings?section=vegetables',
    'next': 'Vegetable pairings >'
}

vegetables = {
    'title': 'Vegetables',
    'labeltop': 'Creamy',
    'labelright':'Sweet',
    'labelbottom':'Acidic',
    'labelleft':'Spicy',
    'topright': wines_food['Chardonnay'],
    'topleft': wines_food['Pinot Noir'],
    'bottomright': wines_food['Riesling'],
    'bottomleft': wines_food['Sauvignon Blanc'],
    'imgtopright': 'vegetable_sweet_creamy.jpg',
    'imgtopleft': 'vegetable_spicy_creamy.jpg',
    'imgbottomright': 'vegetable_sweet_acidic.jpg',
    'imgbottomleft': 'vegetable_spicy_acidic.jpg',
    'hrefback': '/food-pairings?section=meat',
    'back': '< Meat pairings',
    'hrefnext': '/quiz-start',
    'next': 'Explored all the food types? Take the quiz >'
}

@app.route('/')
def index():
    return render_template('home.html')

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
    options = current_question['options'][:] # Start with the correct answer

    random.shuffle(options)

    # Get explanations for each option
    options_with_explanations = [{'option': opt, 'explanation': additional_options[opt]['explanation']} for opt in options]

    return render_template('quiz.html', question=current_question, options=options_with_explanations)

@app.route('/check-answer', methods=['POST'])
def check_answer():

    correct=False
    data = request.get_json()
    selected_option = data['answer']
    correct_answer = session['selected_questions'][session['current_index']]['answer']
    
    print("correct:", correct_answer)
    print("Selected:", selected_option)
    
    if selected_option == correct_answer:
        correct=True
        session['score'] += 1

    print("correct bool: ", correct)
    
    session['current_index'] += 1
    if session['current_index'] >= session['total_questions']:
        return jsonify(endQuiz=True, correctAnswer=correct_answer, correct=correct, explanation = answer_data[correct_answer])
    else:
        next_question = session['selected_questions'][session['current_index']]
        return jsonify(
            endQuiz=False,
            correctAnswer=correct_answer,
            question=next_question['question'],
            image=next_question['image'],
            options=[{'option': opt, 'explanation': additional_options[opt]['explanation']} for opt in next_question['options']],
            correct=correct,
            explanation = answer_data[correct_answer]
        )

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

@app.route('/food-pairings-summary')
def food_pairings_summary():
    return render_template('food_pairings_summary.html')

@app.route('/food-pairings')
def food_pairings():
    return render_template('food_pairings.html')

@app.route('/redwhite-buffer')
def redwhite_buffer():
    return render_template('redwhite_buffer.html')

@app.route('/fullspectrum')
def spec_trans():
    return render_template('spectrum_transition.html')

@app.route('/red-spectrum')
def redspec():
    return render_template('spectrum.html', data=red_spectrum)

@app.route('/white-spectrum')
def whitespec():
    return render_template('spectrum.html', data=white_spectrum)

@app.route('/basicspectrum')
def spectrum():
    return render_template('spectrum.html', data=basic_spectrum)

@app.route('/seafood')
def seafoodspec():
    return render_template('spectrum.html', data=seafood)

@app.route('/meat')
def meatspec():
    return render_template('spectrum.html', data=meat)

@app.route('/vegetables')
def vegspec():
    return render_template('spectrum.html', data=vegetables)

@app.route('/body')
def body():
    return render_template('body.html')

@app.route('/dryness')
def dryness():
    return render_template('dryness.html')

@app.route('/wine_types')
def wine_types():
    return render_template('wine_types.html')


if __name__ == '__main__':
    app.run(debug=True)