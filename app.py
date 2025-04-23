from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load the ground truth data
data = pd.read_csv('q_and_answer.csv')
images = data['Image_Name'].tolist()
random.shuffle(images)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET','POST'])
def start():
    session['correct_answers'] = 0
    session['wrong_answers'] = 0
    session['current_question'] = 0
    session['images'] = images.copy()
    return redirect(url_for('question'))

@app.route('/question')
def question():
    if 'current_question' not in session or session['current_question'] >= len(session['images']):
        return redirect(url_for('final'))
    
    image_name = session['images'][session['current_question']]
    return render_template('question.html', image_name=image_name)

@app.route('/answer', methods=['POST'])
def answer():
    user_answer = request.form['answer']
    # current image
    idx = session['current_question']
    image_name = session['images'][idx]
    # ground truth & reasoning
    row = data.loc[data['Image_Name'] == image_name].iloc[0]
    correct_answer = row['Real_or_AI']
    reasoning = row['Reasoning']
    # store for result page
    session['last_answer'] = user_answer
    session['last_reasoning'] = reasoning
    # tally
    if user_answer == correct_answer:
        session['correct_answers'] += 1
    else:
        session['wrong_answers'] += 1
    session['current_question'] += 1
    return redirect(url_for('result'))

@app.route('/result')
def result():
    if session.get('current_question', 0) > len(session.get('images', [])):
        return redirect(url_for('final'))
    image_name = session['images'][session['current_question'] - 1]

    # compute stats
    correct = session.get('correct_answers', 0)
    wrong   = session.get('wrong_answers',   0)
    total   = correct + wrong
    accuracy = round(correct / total * 100, 2) if total else 0

    return render_template('result.html',
        image_name=image_name,
        user_answer=session.get('last_answer'),
        reasoning=session.get('last_reasoning'),
        correct=correct,
        wrong=wrong,
        accuracy=accuracy,
        remaining=len(session['images']) - session['current_question']
    )
@app.route('/final')
def final():
    correct = session.get('correct_answers', 0)
    wrong   = session.get('wrong_answers',   0)
    return render_template('final.html', correct=correct, wrong=wrong)

if __name__ == '__main__':
    app.run(debug=True)