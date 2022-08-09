from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import copy

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["moves"] = 0
        session["history"] = list()
        session["winner"] = None
        
    return render_template("game.html", game=session["board"], turn=session["turn"], moves=session["moves"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    if session["winner"] == None:
            
        # Update history
        old = copy.deepcopy(session["board"]) 
        session["history"].append(old)

        # for i in range(len(session["history"])):
        #     print(f'This is history {session["history"][i]} at index {i}')

        session["board"][row][col] = session["turn"]

        # Update moves
        session["moves"] = session["moves"] + 1
        # print(f'This is move {session["moves"]}')

        # Check for winner
        # Check first cell of first row and first line, and first column, and diagonal top left to bottom right
        if session["board"][0][0] and (session["board"][0][0] == session["board"][0][1] and session["board"][0][0] == session["board"][0][2]) or (session["board"][0][0] == session["board"][1][0] and session["board"][0][0] == session["board"][2][0]) or (session["board"][0][0] == session["board"][1][1] and session["board"][0][0] == session["board"][2][2]):
            session["winner"] = session["board"][0][0]
        # Check first cell of second row and second line 
        elif session["board"][1][0] and (session["board"][1][0] == session["board"][1][1] and session["board"][1][0] == session["board"][1][2]):
            session["winner"] = session["board"][1][0]
        # Check first cell of third row and third line, and diagonal bottom left to top right
        elif session["board"][2][0] and (session["board"][2][0] == session["board"][2][1] and session["board"][2][0] == session["board"][2][2]) or (session["board"][2][0] == session["board"][1][1] and session["board"][2][0] == session["board"][0][2]):
            session["winner"] = session["board"][2][0]
        # Check second cell of first row and secpond column
        elif session["board"][0][1] and (session["board"][0][1] == session["board"][1][1] and session["board"][0][1] == session["board"][2][1]):
            session["winner"] = session["board"][0][1]
        # Check third cell of first row and third column
        elif session["board"][0][2] and (session["board"][0][2] == session["board"][1][2] and session["board"][0][2] == session["board"][2][2]):
            session["winner"] = session["board"][0][2]
        
        # If there is a winner
        if session["winner"] != None:
            return render_template("game.html", winner=session["winner"], game=session["board"], gameover=True)

        # Tie if we are out of moves
        elif session["moves"] == 9:   
            return render_template("game.html", tie=True, game=session["board"], moves=session["moves"])

        # Alternate turns
        else:
            if session["turn"] == "X":
                session["turn"] = "O"
            else:
                session["turn"] = "X"
            return redirect(url_for("index"))
    else:
        return render_template("game.html", winner=session["winner"], game=session["board"], gameover=True)

@app.route("/back")    
def back():
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"

    session["moves"] = session["moves"] - 1
    # print(f'This is move {session["moves"]} from back func')

    session["board"] = session["history"][session["moves"]]
    # print(f'This is history from back func {session["history"][session["moves"]]}')

    # for i in range(len(session["history"])):
    #     print(f'This is history {session["history"][i]} at index {i} before pop method')
    
    session["history"].pop(session["moves"])

    # for i in range(len(session["history"])):
    #     print(f'This is history {session["history"][i]} at index {i} after pop method')
    
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))