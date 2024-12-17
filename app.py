from flask import Flask, render_template, session, redirect, request, url_for
from SQL import create_account, check_account, update_score_if_record, get_score, get_top_5
import subprocess
import time


app = Flask(__name__)
app.secret_key = "e^31!+c1#5t)g1riwa6xq&)zt4xo5h6evpxr7r_xsu_n*r#s3f"

@app.route("/")
def index():
    if session.get("logged_in"):
        return render_template("index.html")
    else:
        return redirect(url_for('login'))

@app.route("/jouer")
def jouer():
    if session.get("logged_in"):
        return render_template("jouer.html")
    else:
        return redirect(url_for('login'))

@app.route("/joueur2")
def joueur2():
    if session.get("logged_in"):
        pseudo = session.get("username")
        return render_template("joueur2.html", pseudo=pseudo)
    else:
        return redirect(url_for('login'))

@app.route("/infos")
def infos():
    if session.get("logged_in"):
        return render_template("infos.html")
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        current_id = check_account(username, password)
        if not username or not password:
            error = "Veuiller mettre votre pseudnyme et mot de passe"
        elif current_id:
            session['logged_in'] = True
            session['user_id'] = current_id
            session['username'] = username
            return render_template("index.html", pseudo=username)
        else:
            error = "Pseudonyme ou mot de passe incorrecte"
    if session.get('logged_in'):
        return render_template("index.html")
    else:
        return render_template('login.html', error=error)
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return redirect(url_for('login'))
    else:
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm-password']

        if not username or not password:
            msg = "Veuiller mettre votre pseudnyme et mot de passe"
        elif password != confirm:
            msg = "Passwords don't match"
        else:
            msg = create_account(username, password)

        return render_template('login.html', error=msg)
    
@app.route('/player2_login', methods=['GET', 'POST'])
def player2_login():
    error=""
    if request.method == 'GET':
        return redirect(url_for('login'))
    else:
        username_p1 = session['username'] 
        username = request.form['username']
        password = request.form['password']
        player2_id = check_account(username, password)

        if player2_id:
            session['player2_id'] = player2_id
            session['player2_username'] = username
            return redirect(url_for('joueur2'))
        else:
            error = "Player 2 username or password incorrect"
            return render_template('joueur2.html', error=error)

@app.route('/player2_signup', methods=['GET', 'POST'])
def player2_signup():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'GET':
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['new_username']
        password = request.form['new_password']
        if not username or not password:
            msg = "Veuiller mettre votre pseudnyme et mot de passe"
            return render_template('joueur2.html', error=msg, pseudo_p2=username)
        else:
            msg = create_account(username, password)
            session['player2_username'] = username
        return redirect(url_for('joueur2'))
    
@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

@app.route('/player2_logout', methods=['POST'])
def player2_logout():
    session.pop('player2_id', None)
    session.pop('player2_username', None)
    return redirect(url_for('joueur2'))

@app.route('/play')
def play_game():
    try:
        process = subprocess.Popen(['python', 'game_files/karting PC.py'])
        start_time = time.perf_counter()  # High-resolution timer
        # Wait for the game to finish before redirecting
        while process.poll() is None:
            time.sleep(0.1)  # Check every 0.1 second for better responsiveness
        if process.returncode == 0:
            elapsed_time = time.perf_counter() - start_time
            formatted_time = "{:.3f}".format(elapsed_time)  # Format to 3 decimal places
            msg = update_score_if_record(session['username'], elapsed_time)  # Use float, not string for comparison
            return render_template('resultat.html', score=formatted_time, msg=msg)
        return render_template('jouer.html')
    except Exception as e:
        return f"Error occurred while starting the game: {e}"
    

@app.route('/records')
def records():
    global username
    username = session['username'] 
    score_user = "{:.3f}".format(get_score(username)[0])
    rang_user = get_score(username)[1]
    top5 = get_top_5()
    username1, score1 = top5[0][0], "{:.3f}".format(top5[0][1])
    username2, score2 = top5[1][0], "{:.3f}".format(top5[1][1])
    username3, score3 = top5[2][0], "{:.3f}".format(top5[2][1])
    username4, score4 = top5[3][0], "{:.3f}".format(top5[3][1])
    username5, score5 = top5[4][0], "{:.3f}".format(top5[4][1])
    return render_template('records.html', username=username, score=score_user, rang=rang_user, user1=username1, score1 = score1, user2=username2, score2 = score2, user3=username3, score3 = score3, user4=username4, score4 = score4, user5=username5, score5 = score5)

