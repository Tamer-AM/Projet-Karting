from flask import Flask, render_template, session, redirect, request, url_for
from SQL import create_account, check_account

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
    if request.method == 'GET':
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['new_username']
        password = request.form['new_password']
        if not username or not password:
            msg = "Veuiller mettre votre pseudnyme et mot de passe"
        else:
            msg = create_account(username, password)

        return render_template('joueur2.html', error=msg)
    
@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))
