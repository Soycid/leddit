from flask import *
from leddit import app,bcrypt
from leddit.models import User,Post
from leddit.helper_functions import salt_password
from leddit import db
from flask_login import login_user, current_user, logout_user, login_required



	
@app.route('/')
def index():
	posts = Post.query.all()
	return render_template('index.html', posts =posts)

@app.route('/signup', methods=['GET','POST'])
def signup():
	if current_user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		_username = request.form['username']
		_email = request.form['email']
		_password = request.form['password']
		_confirm_password = request.form['confirm_password']
		salted_pass = salt_password(_password)
		hashed_pass = bcrypt.generate_password_hash(salted_pass)
		try:
			if _confirm_password == _password:
				new_user = User(username=_username,email=_email,password=hashed_pass)
				db.session.add(new_user)
				db.session.commit()
				flash('Your account has been created!','success')
				return redirect(url_for('login'))
			else:
				flash('Passwords do not match','failure')
				print("passwords dont match.")
				return redirect('/signup')
	

		except:
			flash('There was an error creating your account. The username or email may already be in use','failure')
			print("There was an error creating your account.")
			return redirect('/signup')
		return redirect('/')
	
	return render_template('auth/reg.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		_username = request.form['username']
		_password = request.form['password']
		salted_pass = salt_password(_password)
		hashed_pass = bcrypt.generate_password_hash(salted_pass)
		user = User.query.filter_by(username=_username).first()
		if user and bcrypt.check_password_hash(user.password, salted_pass):
			login_user(user)
			print('user logged in')
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect('/')
		else:
			flash('Login Unsuccesful','danger')
	return render_template('auth/login.html')

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/')
	
@app.route('/l/<string:sub>')
def post(sub):
	posts = Post.query.filter_by(sub = sub).all()
	return render_template('sub.html', posts=posts, sub = sub)

@app.route('/createpost', methods=['GET','POST'])
@login_required
def createpost():
	if request.method == 'POST':
		_title = request.form['title']
		_sub = request.form['sub']
		_body = request.form['body']
		
		try:
			new_post = Post(title = _title, sub = _sub, body = _body, author = current_user)
			db.session.add(new_post)
			db.session.commit()
			flash('Your account has been created!','success')
			return redirect(url_for('login'))
		except:
			flash('There was an error submitting your post','failure')
			print("There was an error submitting your post.")
			return redirect('/')	
	
	
	
	
	
		flash('Your post has been created!','success')
		return redirect('/')
	return render_template('auth/post.html')
	
	
