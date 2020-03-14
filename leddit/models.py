from leddit import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), nullable =False, unique=True)
	email = db.Column(db.String(120),nullable=False,unique=True)
	password = db.Column(db.String(120),nullable=False,unique=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	posts = db.relationship('Post', backref='author', lazy = True)
	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable =False)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	sub = db.Column(db.String(32), nullable =False)
	upvotes = db.Column(db.Integer, nullable =False, default = 1)
	body = db.Column(db.Text, nullable =False)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}', '{self.sub}')"