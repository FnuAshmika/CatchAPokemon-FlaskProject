from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable= False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120),nullable= False)
    timestamp= db.Column(db.DateTime, default=datetime.utcnow)
    pokemons = db.relationship('PokeCatch', backref='owner', lazy='dynamic')

    def __repr__(self):
        return f'User: {self.username}'
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

class PokeCatch(db.Model):
    __tablename__ = 'poke_catch'
    id = db.Column(db.Integer, primary_key=True)
    poke = db.Column(db.String(140))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('pokecatches', lazy=True))

    def __repr__(self):
        return f'<PokeCatch {self.poke}>'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()