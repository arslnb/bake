from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, validators, ValidationError, PasswordField, RadioField
from wtforms.validators import Required
from models import db, User

class LoginForm(Form):
	email = TextField("email", validators = [Required()])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])

class AddTask(Form):
	newtask = TextField("newtask", validators = [Required()])

class DeleteTask(Form):
	pass

class SignupForm(Form):
	email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])
	repassword = PasswordField('Repeat Password', [validators.Required("Please enter password again.")])

	def get_id(self):
		return unicode(self.id)	
	
	def __repr__(self):
		return '<Name %r>' % (self.name)
