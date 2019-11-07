from flask import Flask, render_template, session, request
import random
import os
import pickle
import time
import webbrowser

#Global variables
#=================
number = random.randint(0,1000)
time_taken = 0.0
#=================

FNAME = "data/scores.pickle"


app = Flask(__name__)


#==================================================================================================================================
@app.route("/game")

def display_score():
    score = number
   
    session["start"] = time.perf_counter()
        
    session["score"] = score
    return render_template(
        "score.html", the_hiddenNumber=number, the_title="Guess The Number",the_hint = ""
    )
#==================================================================================================================================


#==================================================================================================================================
@app.route ("/checkGuess", methods=["POST"])
def check_guess():
    inputNumber = request.form["inputNumberPlayer"]
    inputNumber = int(inputNumber)

    # less than
    if inputNumber < number:
         return render_template(
        "score.html", the_hiddenNumber=number, the_title="Guess The Number",the_hint= "The number is higher"
        )

    # greater than
    elif inputNumber > number:
        return render_template(
        "score.html", the_hiddenNumber=number, the_title="Guess The Number",the_hint= "The number is lower"
        )
    
    #win
    else:
        session["end"] = time.perf_counter()
        time_taken = round(session["end"] - session["start"], 2)
        session["score"] = time_taken
        converted = time_taken
        msg = "You win. You took " + str(converted) + " seconds to find the number. Enter in your name to save your score" 
        return render_template(
        "recordName.html", the_hiddenNumber=number, the_title="Guess The Number",the_hint= msg,the_score = time_taken
        )
        
   
#==================================================================================================================================
 


#==================================================================================================================================
@app.route("/recordhighscore", methods=["POST"])
def store_score():
    score = session["score"]
    player_name = request.form["player"]

    if not os.path.exists(FNAME):
        data = []
    else:
        with open(FNAME, "rb") as pf:
            data = pickle.load(pf)
    data.append((score, player_name))  ## RACE CONDITION.
    with open(FNAME, "wb") as pf:
        pickle.dump(data, pf)

    webbrowser.open_new_tab('http://localhost:5000/showhighscores')
    return "Your highscore has been recorded."
#==================================================================================================================================


#==================================================================================================================================
@app.route("/showhighscores")
def show_scores():
    with open(FNAME, "rb") as pf:
        data = pickle.load(pf)
    return render_template(
        "winners.html",
        the_title="Here are the High Scores",
        the_data=sorted(data, reverse=True),
    )
#==================================================================================================================================


app.secret_key = (
    " wen'0ut93u4t0934ut93u4t09 3u4t9 u3   40tuq349tun34#-9tu3#4#vetu #    -4"
)

app.run(debug=True)
