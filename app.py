from flask import Flask, request, flash, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

@app.route('/')
def start_survey():
    """ Landing page for start of survey """

    return render_template('survey.html',
        survey_title=surveys.satisfaction_survey.title,
        instructions=surveys.satisfaction_survey.instructions)


@app.route('/questions/<question>')
def ask_question(question):
    """ Display form for survey question """

    if len(surveys.satisfaction_survey.questions) == session['questions_answered']:
        return redirect('/thank-you')
    elif int(question) != session['questions_answered']:
        flash("Naughty naughty, don't do that.")
        return redirect(f"/questions/{session['questions_answered']}")

    question_instance = surveys.satisfaction_survey.questions[int(question)]

    return render_template('question.html',
        question=question_instance.question,
        choices=question_instance.choices)


@app.route('/answer', methods=["POST"])
def get_answer():
    """ Save response to reponses list and redirect to next question """
    
    responses = session['responses']
    responses.append(request.form['selection'])
    index = len(session['responses'])

    session['questions_answered'] = index

    return redirect(f"/questions/{index}")


@app.route('/thank-you')
def show_thank_you():
    """ Display thank you page """

    return render_template('thank-you.html')


@app.route('/reset-survey', methods=["POST"])
def reset_session():
    """ Resets session variables """

    session['questions_answered'] = 0
    session['responses'] = []

    return redirect('/questions/0')




# TODO: make requirements.txt file
