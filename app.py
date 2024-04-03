from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

# @app.route('/')
# def show_start_page():
#     """Show start page for survey."""
#     return render_template("start.html", survey=satisfaction_survey)
@app.route('/', methods=["GET", "POST"])
def show_start_page():
    """Clear the session of responses."""
    session["responses"] = []
    return render_template("start.html", survey=satisfaction_survey)


@app.route('/questions/<int:qid>')
def show_question(qid):
    """Display current question."""
    responses = session.get("responses", [])
    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/thankyou")
    if len(responses) != qid:
        flash("Trying to access an invalid question!", "error")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)



@app.route('/answer', methods=["POST"])
def handle_answer():
    responses = session["responses"]
    choice = request.form['answer']
    responses.append(choice)
    session["responses"] = responses
    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect("/thankyou")


@app.route('/thankyou')
def thank_you():
    return render_template("thankyou.html")
