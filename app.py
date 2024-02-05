from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
boggle_game = Boggle()

@app.route('/')
def boggle_home():
    """Display boggle board"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    numplays = session.get('numplays', 0)

    return render_template('base.html', board=board, highscore=highscore, numplays=numplays)

@app.route('/verify-word')
def verify_word():
    """Check and verify if a word is in words.txt"""
    word = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board, word)
    
    return jsonify({'result': res})

@app.route('/post-score', methods=['POST'])
def post_score():
    """Get and update score if previous high score surpassed, and update numplays"""
    cur_score = request.json['score']
    highscore = session.get('highscore', 0)
    numplays = session.get('numplays', 0)

    session['numplays'] = numplays + 1
    session['highscore'] = max(cur_score, highscore)

    return jsonify(brokeRecord = cur_score > highscore)