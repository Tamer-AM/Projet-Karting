Projet Karting Raspberry Pi



Cette archive contient le code source et les ressources pour le projet de karting sur Raspberry Pi, qui intègre une interface web développée avec Flask et un jeu de karting construit avec Pygame. Vous trouverez ci-dessous une description détaillée de la structure des dossiers, du contenu des fichiers et des fonctionnalités.



Vue d'ensemble du projet
Le projet se compose d'une application web utilisant Flask et d'un jeu de karting décliné en trois versions différentes avec Pygame. Les joueurs peuvent interagir avec le jeu via un clavier ou un capteur Grove 3-Axis Accelerometer.

Versions du jeu :

-Solo (Capteur de mouvement) : Utilise le capteur Grove 3-Axis Accelerometer pour contrôler le kart.
-Solo (Clavier) : Permet de contrôler le kart avec un clavier.
-Deux joueurs : Combinaison de deux contrôles : le capteur pour le Joueur 1 et le clavier pour le Joueur 2.

Fonctionnalités du site web :
Inscription et connexion des utilisateurs : Les utilisateurs doivent créer un compte et se connecter pour accéder au site web.
Tableau des records : Affiche le meilleur temps et le rang de l'utilisateur connecté, et le meilleur temps des top 5 utilisateurs.
Informations : Explique les commandes pour jouer avec un clavier ou un capteur.
Lancement du jeu intégré : Les jeux peuvent être lancés directement depuis le site web.

--------------------------------------------------------------------------------------------------------------------------
Structure des dossiers:

karting/  
│  
├── app.py  
│   - L'application principale Flask qui gère les routes, les interactions avec la base de données et le lancement des jeux.  
│  
├── sql.py  
│   - Contient les fonctions SQL pour interagir avec la base de données (DB.db).  
│  
├── game_files/  
│   ├── karting PC.py  
│   ├── karting v2.2.py  
│   ├── main.py  
│   ├── Images/  
│   │   - Contient les ressources pour le jeu Pygame.  
│   └── build/  
│       - Inclut les fichiers nécessaires à l'exécution du jeu Pygame.  
│  
├── static/  
│   ├── style.css  
│   │   - La feuille de style principale du site web.  
│   ├── images/  
│   │   - Contient les images du site web (logos, icônes, etc.).  
│   └── sounds/  
│       - Contient les sons utilisés dans le site web.  
│  
├── templates/  
│   ├── index.html  
│   ├── infos.html  
│   ├── jouer.html  
│   ├── joueur2.html  
│   ├── login.html  
│   ├── records.html  
│   └── resultat.html  
│       - Tous les fichiers HTML gérés par Flask via la fonction `render_template`.  
│  
├── DB.db  
│   - La base de données SQLite contenant les tables suivantes :  
│     - **COMPTE** (Clé primaire : numero) : pseudonyme (TEXT), mot_de_passe (TEXT).  
│     - **SCORE** (Clé primaire : numero) : id_compte (clé étrangère), meilleur_temps.  
│  
└── README.md  
    - Ce fichier descriptif.  


Raspberry/  
│  
├── raspberry.py  

--------------------------------------------------------------------------------------------------------------------------
Instructions:


Exécution du site web :
Ouvrez un terminal dans le dossier principal et exécutez la commande :
flask run  


Lancement du jeu :
Le jeu peut être lancé directement via le site web. Par défaut, la version PC du jeu est configurée dans app.py, dans la fonction  play_game()  avec la commande suivante:

process = subprocess.Popen(['python', 'game_files/karting PC.py'])  

Si vous souhaitez lancer la version pour Raspberry Pi, modifiez le chemin vers game_files/main.py.


Version Raspberry :
    Pour jouer avec la version Raspberry Pi :

    -Exécutez le fichier raspberry.py sur le Raspberry Pi
    -Assurez-vous d'avoir configuré l'adresse IP correcte dans le fichier raspberry.py (voir la section Prérequis dans ce fichier pour plus de détails).
    -Une fois le serveur Raspberry démarré, vous pouvez lancer les parties via le site web (plus d'informations dans la partie qui suit).



--------------------------------------------------------------------------------------------------------------------------
Prérequis

Pour la version Raspberry:
    Matériel:
        Un Raspberry Pi (pour les tests du capteur).
        Un capteur Grove 3-Axis Accelerometer (I2C).

    Logiciel:
        Python 3.x
        Flask
        Pygame
        Bibliothèque Grove (installée sur le Raspberry Pi).

    Configuration requise :
        Les données sont enregistrées par le Raspberry Pi via le capteur, puis envoyées au PC via une logique client-serveur :
        -Serveur : Raspberry Pi.
        -Client : Utilisateur (ordinateur/PC).
        
        Instructions pour la configuration :
        Modifier l'adresse IP :
            Dans le fichier Raspberry (indiquez ici le nom du fichier : {{name here}}), remplacez l'IP par celle de la machine utilisée (PC).
            
        Exécuter le code :
            Lancez le script sur le Raspberry Pi avant de démarrer les parties.
        Puis C'est prêt !


Pour la version PC:
    Logiciel:
        Python 3.x
        Flask
        Pygame


--------------------------------------------------------------------------------------------------------------------------
Auteurs:
    -Tamer AL MASRI
    -Yanis KHELOUFI
    -Antoine RENAUD

Groupe 9