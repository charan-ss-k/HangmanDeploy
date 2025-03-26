from flask import Flask, session, redirect, url_for, request, render_template
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def choose_word(difficulty):
    easy_words = ["cat", "dog", "book", "fish", "home", "tree", "bird", "game", "play", "jump"]
    hard_words = ["python", "developer", "algorithm", "programming", "javascript", "database", "framework", "encryption"]
    return random.choice(easy_words if difficulty == 'easy' else hard_words)

def display_word(word, guessed_letters):
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)

def init_game(difficulty):
    session['word'] = choose_word(difficulty)
    session['guessed_letters'] = []
    session['attempts'] = 8 if difficulty == 'easy' else 6
    session['difficulty'] = difficulty

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/game/<difficulty>')
def game(difficulty):
    if difficulty not in ['easy', 'hard']:
        return redirect(url_for('welcome'))
    
    init_game(difficulty)
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
                         game_over=game_over,
                         difficulty=difficulty)

@app.route('/guess', methods=['POST'])
def make_guess():
    data = request.get_json()
    guess = data.get("guess", "").lower().strip()
    word = session.get('word')
    guessed_letters = set(session.get('guessed_letters', []))
    attempts = session.get('attempts', 6)
    difficulty = session.get('difficulty', 'easy')
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

@app.route('/app1')
def app1():
    return redirect('/app1')

@app.route('/app2')
def app2():
    return redirect('/app2')

if __name__ == '__main__':
    app.run(debug=True, port=3000)