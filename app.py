from flask import Flask, request, flash, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

@app.route('/')
def select_survey():
    """ Landing page for selecting a survey """

    session['survey_id'] = None

    return render_template('survey-select.html',
        survey_titles=surveys.surveys.keys())

@app.route('/start')
def start_survey():
    """ Survey start page """

    session['survey_id'] = request.args['survey_id']
    current_survey = surveys.surveys[session['survey_id']]

    return render_template('survey.html',
        survey_title=current_survey.title,
        instructions=current_survey.instructions)


@app.route('/questions/<question>')
def ask_question(question):
    """ Display form for survey question """

    current_survey = surveys.surveys[session['survey_id']]

    if len(current_survey.questions) == session['questions_answered']:
        return redirect('/thank-you')
    elif int(question) != session['questions_answered']:
        flash("Naughty naughty, don't do that.")
        return redirect(f"/questions/{session['questions_answered']}")

    question_instance = current_survey.questions[int(question)]

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
