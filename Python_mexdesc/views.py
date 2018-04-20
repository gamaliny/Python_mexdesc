import string
import random
from run import app
from run import login
from run import db
from run import mail
from models import Account
from models import LoginForm
from models import NewUserForm
#Pour utiliser Flask, rediriger vers une autre route et afficher un template
from flask import Flask, url_for, redirect, render_template
#Pour les champs du formulaire de connexion, login, pswd et se souvenir du mot de passe
from flask_sqlalchemy import SQLAlchemy
#Pour comparer le mot de passe crypté dans la BDD et convertir en version crypté celui entré
from werkzeug.security import check_password_hash, generate_password_hash
#gestion des paramètres de l'utilisateur connecté
from flask_login import login_user, logout_user, login_required, current_user

from flask_mail import Message

@login.user_loader
def load_user(user_id): 
	return Account.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if (current_user.is_authenticated == True):
		return redirect(url_for('home'))
		
	form = LoginForm()
	if form.validate_on_submit():
		user = Account.query.filter_by(email = form.email.data).first()
		if user:
			if check_password_hash(user.pswd, form.password.data):
				login_user(user)
				return redirect(url_for('home'))
		return  'Invalid username or password'
	return render_template('login.twig', form=form, title='Sign in')
	
@app.route('/home')
@login_required
def home():
	return render_template('menu.twig', title='Home')

@app.route("/search_a_translation")
@login_required
def search_translation():
	return render_template('search_translation.twig')

@app.route("/translate_word")
@login_required
def translate_word():
	return render_template('translate_word.twig')
	
@app.route("/untranslated_words")
@login_required
def untranslated_words():
	return render_template('untranslated_words.twig')
	
@app.route("/import_words_PDF")
@login_required
def import_words_PDF():
	return render_template('import_words_PDF.twig')
	
@app.route("/add_words_from_PDF")
@login_required
def add_words_from_PDF():
	return render_template('add_words_from_PDF.twig')

@app.route("/admin/account/edit/", methods=['GET', 'POST'])
@login_required
def edit_user():
	item = Item.query.get(id)
	user = Account.query.get(item)  
	form = AccountForm(obj=user) 
	if form.validate_on_submit():
		return redirect('/admin/account')
	return redirect(url_for('/admin/account/edit/'))
	
@app.route("/admin/account/add_user", methods=['GET', 'POST'])
@login_required
def add_user():
	form = NewUserForm()
	if form.validate_on_submit():
		password = password_generator()
		hash_password = generate_password_hash(password)
		new_user = Account(email=form.email.data, pswd=hash_password, isAdmin=form.isAdmin.data)
		db.session.add(new_user)
		db.session.commit()
		msg = Message('Account details for Maya translator website', sender = 'gamaliny@gmail.com', body='Your login is :'+ form.email.data +' adress and your password is '+password, recipients = [form.email.data])
		mail.send(msg)
		return 'New user has been created, the password has been send to his/her email '
		#Mettre en popup
	return render_template('add_user.twig', form= form)

@app.route("/scan_OCR")
def scan_OCR():
	return render_template('upload_PDF.twig')	

@app.route("/settings")
@login_required
def settings():
	#return redirect("/admin/account/edit/?id="+current_user.get_id())
	return render_template('settings.twig')
	
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

def password_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
