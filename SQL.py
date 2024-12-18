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

def update_score_if_record(username, new_time):
    connection = get_db()
    sql = connection.cursor()

    # Retrieve the user's ID
    sql.execute("SELECT numero FROM COMPTE WHERE pseudonyme = ?", (username,))
    user = sql.fetchone()
    if not user:
        return "Utilisateur introuvable."

    user_id = user["numero"]

    # Check if the user already has a score
    sql.execute("SELECT meilleur_temps FROM SCORE WHERE id_compte= ?", (user_id,))
    score = sql.fetchone()

    if score:
        current_best_time = float(score["meilleur_temps"])
        if new_time < current_best_time:  # Update only if the new time is better
            sql.execute("UPDATE SCORE SET meilleur_temps = ? WHERE id_compte = ?", (new_time, user_id))
            connection.commit()
            return "Nouveau record! Félicitations."
        else:
            return "Le temps n'est pas un record."
    else:
        # Insert a new score record if none exists
        sql.execute("INSERT INTO SCORE (id_compte, meilleur_temps) VALUES (?, ?)", (user_id, new_time))
        connection.commit()
        return "Nouveau record! Félicitations."
    

def get_score(username):
    connection = get_db()
    sql = connection.cursor()
    sql.execute("SELECT numero FROM COMPTE WHERE pseudonyme = ?", (username,))
    user = sql.fetchone()
    user_id = user["numero"]
    sql.execute("SELECT meilleur_temps FROM SCORE WHERE id_compte= ?", (user_id,))
    score = sql.fetchone()
    if score:
        user_score = score["meilleur_temps"]
        sql.execute("SELECT id_compte, meilleur_temps FROM SCORE ORDER BY meilleur_temps ASC")
        all_scores = sql.fetchall()
        rank = 0
        for i, elem in enumerate(all_scores):
            if int(elem[0]) == int(user_id):
                rank = i+1
                break
        return user_score, rank
    return False


def get_top_5():
    connection = get_db()
    sql = connection.cursor()
    sql.execute("SELECT COMPTE.pseudonyme, SCORE.meilleur_temps FROM SCORE JOIN COMPTE ON SCORE.id_compte = COMPTE.numero ORDER BY SCORE.meilleur_temps ASC LIMIT 5;")
    result = sql.fetchall()
    return result