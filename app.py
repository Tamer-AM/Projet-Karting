from flask import Flask, render_template, session, redirect

app = Flask(__name__)
app.secret_key = "e^31!+c1#5t)g1riwa6xq&)zt4xo5h6evpxr7r_xsu_n*r#s3f"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/jouer")
def jouer():
    return render_template("jouer.html")

@app.route("/infos")
def infos():
    return render_template("infos.html")