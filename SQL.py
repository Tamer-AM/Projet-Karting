import sqlite3
from flask import g

db_file = "C:/Users/Tamer/OneDrive/Desktop/Karting/DB.db"

# Variables globales pour stocker le pseudonyme, le mot de passe et le temps
pseudo = None
mdp = None
meilleur_temps = None
position = None

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(db_file)
        g.db.row_factory = sqlite3.Row
    return g.db

def create_account(username, password):
    global pseudo, mdp, meilleur_temps
    pseudo = username
    mdp = password
    connection = get_db()
    sql = connection.cursor()
    sql.execute("SELECT COUNT(*) FROM COMPTE WHERE pseudonyme = ?", (pseudo,))
    result = sql.fetchone()
    if result[0] > 0:  # Si le pseudonyme existe déjà
        pseudo = None
        mdp = None
        return "Pseudonyme déjà existant. Veuillez choisir un autre pseudonyme."
    inser_compte = "INSERT INTO COMPTE (pseudonyme, mot_de_passe) VALUES (?, ?)"
    sql.execute(inser_compte, (username, password))
    connection.commit()
    return "Compte créé avec succès"

def check_account(username, password):
    global pseudo, mdp, meilleur_temps, position
    pseudo = username
    mdp = password
    connection = get_db()
    sql = connection.cursor()
    sql.execute("SELECT COUNT(*) FROM COMPTE WHERE pseudonyme = ? AND mot_de_passe = ?", (pseudo, mdp))
    result = sql.fetchone()
    if result[0] == 0:  # Si le pseudonyme ou le mot de passe est incorrect
        pseudo = None
        mdp = None
        return False
    return True