from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS




app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login =LoginManager(app)
cors = CORS(app)

login.login_view='/signin'
login.login_message="Don't forget to login."

from app.blueprints.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app.blueprints.main import bp as main_bp
app.register_blueprint(main_bp)

from app.blueprints.social import bp as social_bp
app.register_blueprint(social_bp)

 