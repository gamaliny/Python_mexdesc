﻿#Pour utiliser Flask, rediriger vers une autre route et afficher un template
from flask import Flask
#Pour connecter à la BDD
from flask_sqlalchemy import SQLAlchemy
#gestion des paramètres de l'utilisateur connecté
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
#gestion des utilisateurs
from flask_admin import Admin


app = Flask(__name__)

app.config.from_pyfile('config.py')

Bootstrap(app)
db = SQLAlchemy(app)
admin = Admin(app)
login = LoginManager(app)
login.init_app(app)

from views import *	

if __name__ == "__main__":
	app.run()