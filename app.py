from flask import Flask, request, flash, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def start_survey():

    return render_template('survey.html',
        survey_title=surveys.satisfaction_survey.title,
        instructions=surveys.satisfaction_survey.instructions)


@app.route('/questions/<question>')
def ask_question(question):

    question_instance = surveys.satisfaction_survey.questions[int(question)]

    return render_template('question.html',
        question=question_instance.question,
        choices=question_instance.choices)

@app.route('/answer', methods=["POST"])
def get_answer():
    
    responses.append(request.form['selection'])
    index = len(responses)

    return redirect(f"/questions/{index}")



# TODO: make requirements.txt file
