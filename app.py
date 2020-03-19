from flask import Flask, request, flash, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start_survey():
    """ Landing page for start of survey """
    session['questions_answered'] = 0

    return render_template('survey.html',
        survey_title=surveys.satisfaction_survey.title,
        instructions=surveys.satisfaction_survey.instructions)


@app.route('/questions/<question>')
def ask_question(question):
    """ Display form for survey question """

    if len(surveys.satisfaction_survey.questions) == session['questions_answered']:
        return redirect('/thank-you')

    question_instance = surveys.satisfaction_survey.questions[int(question)]

    return render_template('question.html',
        question=question_instance.question,
        choices=question_instance.choices)

@app.route('/answer', methods=["POST"])
def get_answer():
    """ Save response to reponses list and redirect to next question """
    responses.append(request.form['selection'])
    index = len(responses)

    session['questions_answered'] = index

    return redirect(f"/questions/{index}")

@app.route('/thank-you')
def show_thank_you():
    """ Display thank you page """
    return render_template('thank-you.html')

# TODO: make requirements.txt file
