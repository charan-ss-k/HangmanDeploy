from flask import Flask, session, redirect, request, render_template, url_for, send_from_directory
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')  # Better to use environment variable

# Ensure paths are correct for Vercel
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')

# Create static/images directory if it doesn't exist
os.makedirs(IMAGES_DIR, exist_ok=True)

PROGRAMMING_WORDS = ["python", "developer", "algorithm", "programming", "javascript", "database", "framework", "encryption"]
ENGLISH_WORDS = ["cat", "dog", "book", "fish", "home", "tree", "bird", "game", "play", "jump", "happy", "world", "smile"]

def choose_word(game_mode):
    return random.choice(PROGRAMMING_WORDS if game_mode == 'app1' else ENGLISH_WORDS)

def display_word(word, guessed_letters):
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)

def init_game(game_mode):
    session['word'] = choose_word(game_mode)
    session['guessed_letters'] = []
    session['attempts'] = 6
    session['game_mode'] = game_mode

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/app1')
def programming_game():
    init_game('app1')
    return render_template("index.html",
                         current_display=display_word(session['word'], set()),
                         guessed_letters=[],
                         attempts=6,
                         message="",
                         game_over=False,
                         game_mode='Programming Words')

@app.route('/app2')
def english_game():
    init_game('app2')
    return render_template("index.html",
                         current_display=display_word(session['word'], set()),
                         guessed_letters=[],
                         attempts=6,
                         message="",
                         game_over=False,
                         game_mode='English Words')

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

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)