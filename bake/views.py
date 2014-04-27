from flask import render_template, flash, redirect, session, url_for, request, make_response
from bake import bake, db, models
from forms import LoginForm, SignupForm, AddTask, DeleteTask
from models import User, List
from hashlib import md5
import time

@bake.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bake.errorhandler(500)
def double_entry(e):
    return render_template('500.html'), 500


@bake.route("/", methods=['GET', 'POST'])
def home():
	form = AddTask()
	delete = DeleteTask()

	if 'email' not in session:
		return redirect(url_for('login')) 

	user = User.query.filter_by(email = session['email']).first()

	if request.method == 'POST':
		if request.form['push'] == 'Add Task':
			if form.validate_on_submit():
				item = models.List(task = form.newtask.data, person = user)
				db.session.add(item)
				db.session.commit()
				temp = models.List.query.filter_by(person = user)
				return render_template('index.html', form = form, tasklist = temp)

			else:
				temp = models.List.query.filter_by(person = user)
				form.email.errors.append("Error")
				return render_template('index.html', form = form, tasklist = temp)
		else:
			instance = models.List.query.filter_by(id=int(request.form['push'])).first()
			db.session.delete(instance)
			db.session.commit()

			temp = models.List.query.filter_by(person = user)
			return render_template('index.html', form = form, tasklist = temp)

	elif request.method == 'GET':
		user = User.query.filter_by(email = session['email']).first() 
		temp = models.List.query.filter_by(person = user)

		return render_template('index.html', form = form, tasklist = temp)

@bake.route("/signup", methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	if request.method == 'POST':
		if form.validate_on_submit():
			if form.password.data == form.repassword.data:
				item = models.User(email = form.email.data, password = form.password.data)
				db.session.add(item)
				db.session.commit()

				session['email'] = item.email
				return redirect(url_for('home'))

			else:
				return "Password Mismatch"

		else:
			form.email.errors.append("Error")
			return render_template('signup.html', form = form)

	elif request.method == 'GET':
		return render_template('signup.html', form = form)

@bake.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if request.method == 'POST':
		if form.email.data.lower() not in session:
			if form.validate_on_submit():
				user = User.query.filter_by(email = form.email.data.lower()).first()            
				if user and user.check_password(form.password.data):
					session['email'] = user.email
					return redirect(url_for('home'))
				else:
					form.email.errors.append("Invalid e-mail or password")
					return render_template('login.html', form=form)            
	elif request.method == 'GET':
		return render_template('login.html', form=form)

@bake.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    session.pop('email', None)
    return redirect(url_for('login'))

@bake.route("/about")
def about():
	return "About page"
