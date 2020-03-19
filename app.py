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

