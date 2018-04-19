#du fichier login importer la variable db et admin
from run import db
from run import app
from run import admin
#Pour les champs du formulaire de connexion, login, pswd et se souvenir du mot de passe
from wtforms import StringField, PasswordField, BooleanField 	
#Pour le formulaire de connexion
from flask_wtf import FlaskForm
#Pour obliger de remplir les champs ayant une certaine taille de value
from wtforms.validators import InputRequired, Email, Length
#Pour connecter à la BDD
from flask_login import UserMixin
#Pour gérer les utilisateurs
from flask_admin.contrib.sqla import ModelView


class Account(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60))
	pswd = db.Column(db.String(60))
	isAdmin = db.Column(db.Boolean)
	
#class SettingsView(ModelView):
	#form_columns = ['email', 'isAdmin']
	
class AccountSettings(ModelView):
	column_exclude_list = ['pswd' ]
	form_columns = ['email', 'isAdmin']
	
class LoginForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=2, max=20)])
	remember = BooleanField('remember me')
	
class NewUserForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
	isAdmin = BooleanField('Administrator')

#Faire trois types de vues un pour la gestion des utilisateurs
admin.add_view(AccountSettings(Account, db.session))
#Pour les paramètres
#Pour la gestion des traductions
#admin.add_view(AccountSettings(Account, db.session))
