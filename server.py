# app.py

from flask import Flask, render_template, request, jsonify, url_for, redirect

app = Flask(__name__, static_url_path='/static')

current_id = 0
data = {
    # Data goes in here
}

@app.route('/')
def index():
    return render_template('home.html')

# @app.route('/learn')
# def learn():
#     return

# @app.route('/quiz')
# def quiz():
#     return

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