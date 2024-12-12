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
            return render_template("index.html")
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
    
@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))
