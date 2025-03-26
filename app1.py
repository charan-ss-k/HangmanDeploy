import random
from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def choose_word():
    words = ["python", "developer", "hangman", "challenge", "programming", "education"]
    return random.choice(words)

def display_word(word, guessed_letters):
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)

def init_game():
    session['word'] = choose_word()
    session['guessed_letters'] = []
    session['attempts'] = 6

@app.route('/', methods=['GET'])
def index():
    init_game()
    word = session['word']
    guessed_letters = set(session.get('guessed_letters', []))
    attempts = session.get('attempts', 6)
    current_display = display_word(word, guessed_letters)
    message = ""
    game_over = False

    return render_template("index.html",
                           current_display=current_display,
                           guessed_letters=sorted(guessed_letters),
                           attempts=attempts,
                           message=message,
                           game_over=game_over)

@app.route('/start', methods=['GET'])
def start():
    return render_template("start.html")

@app.route('/guess', methods=['POST'])
def make_guess():
    data = request.get_json()
    guess = data.get("guess", "").lower().strip()
    word = session.get('word')
    guessed_letters = set(session.get('guessed_letters', []))
    attempts = session.get('attempts', 6)
    message = ""

    if not guess or len(guess) != 1 or not guess.isalpha():
        message = "Please enter a valid single letter."
    elif guess in guessed_letters:
        message = f"You already guessed '{guess}'."
    else:
        guessed_letters.add(guess)
        session['guessed_letters'] = list(guessed_letters)
        if guess not in word:
            attempts -= 1
            session['attempts'] = attempts
            message = f"Wrong guess! Attempts left: {attempts}"
        else:
            message = "Good guess!"

    current_display = display_word(word, guessed_letters)

    if all(letter in guessed_letters for letter in word):
        message = f"Congratulations! You guessed the word: {word}"
        game_over = True
    elif attempts <= 0:
        message = f"Game over! The word was: {word}"
        game_over = True
    else:
        game_over = False

    image_url = url_for('static', filename=f"images/hangman-{attempts}.png")
    return {
        "current_display": current_display,
        "guessed_letters": sorted(guessed_letters),
        "attempts": attempts,
        "message": message,
        "game_over": game_over,
        "image_url": image_url
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)