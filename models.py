from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.Text,
        nullable=False
    )
    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png"
    )
    
    @classmethod
    def signup(cls, username, email, password, image_url):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Station(db.Model):
    __tablename__ = "stations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.Text,
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    @classmethod
    def charger(cls, name, user_id):
        charger = Station(
            name=name,
            user_id=user_id 
        )

        db.session.add(charger)
    
        return charger


def connect_db(app):
    db.app = app
    db.init_app(app)