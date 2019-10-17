"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from instagram import getfollowedby, getname
import hashlib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://aracne_user:1234aracne@db.aracne-projekt.tk:5432/aracne_db'
#'sqlite:///test.db'
#'postgresql://user:password@hostname/database_name'

db = SQLAlchemy(app)

class User(db.Model):
	""" Create user table"""
	__tablename__ = 'users'
	username = db.Column('username',db.String(255), primary_key=True)
	password = db.Column('password',db.String(255))

	"""def __init__(self, username, password):
		self.username = username
		self.password = password"""

	def __repr__(self):
		return "<User(name='{}', password='{}')>"\
                .format(self.username, self.password)


@app.route('/', methods=['GET', 'POST'])
def home():
	""" Session control"""
	if not session.get('logged_in'):
		return render_template('inicio.html')
	else:
		if request.method == 'POST':
			username = getname(request.form['username'])
			return render_template('inicio.html', data=getfollowedby(username))
		return render_template('inicio.html')

@app.route('/bd', methods=['GET', 'POST'])
def bd():
	if not session.get('logged_in'):
		return render_template('bd.html')
	else:
		if request.method == 'POST':
			username = getname(request.form['username'])
			return render_template('bd.html', data=getfollowedby(username))
		return render_template('bd.html')

@app.route('/diagrama', methods=['GET', 'POST'])
def diagrama():
	if not session.get('logged_in'):
		return render_template('diagrama.html')
	else:
		if request.method == 'POST':
			username = getname(request.form['username'])
			return render_template('diagrama.html', data=getfollowedby(username))
		return render_template('diagrama.html')

@app.route('/dns', methods=['GET', 'POST'])
def dns():
	if not session.get('logged_in'):
		return render_template('dns.html')
	else:
		if request.method == 'POST':
			username = getname(request.form['username'])
			return render_template('dns.html', data=getfollowedby(username))
		return render_template('dns.html')

@app.route('/servidor', methods=['GET', 'POST'])
def servidor():
	if not session.get('logged_in'):
		return render_template('servidor.html')
	else:
		if request.method == 'POST':
			username = getname(request.form['username'])
			return render_template('servidor.html', data=getfollowedby(username))
		return render_template('servidor.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Login Form"""
	if request.method == 'GET':
		return render_template('login.html')
	else:
		name = request.form['username']
		m = hashlib.sha256()
		m.update(request.form['password'].encode('utf-8'))
		passw = m.hexdigest()
		try:
			data = User.query.filter_by(username=name, password=passw).first()
			if data is not None:
				session['logged_in'] = True
				return redirect(url_for('home'))
			else:
				return 'Dont Login'
		except:
			return "Dont Login"

@app.route('/register/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	if request.method == 'POST':
		m = hashlib.sha256()
		m.update(request.form['password'].encode('utf-8'))
		new_pass = m.hexdigest() 
		new_user = User(username=request.form['username'], password=new_pass)
		db.session.add(new_user)
		db.session.commit()
		return render_template('login.html')
	return render_template('register.html')

@app.route("/logout")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return redirect(url_for('home'))


if __name__ == '__main__':
	app.debug = True
	db.create_all()
	app.secret_key = "123"
	app.run(host='0.0.0.0')
	