"""Models for authentication app"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users table"""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    
    feedback = db.relationship("Feedback",backref="users",cascade="all, delete-orphan")
    
    @classmethod
    def register(cls,username,password):
        """Register and create user w/hashed password"""

        hash_pass = bcrypt.generate_password_hash(password)

        hash_pass_utf8 = hash_pass.decode("utf8")

        return cls(username=username, password=hash_pass_utf8)
    
    @classmethod
    def authenticate(cls,username,password):
        """Validate user login attempt"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
    
class Feedback(db.Model):
    """Feedback table"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    username = db.Column(db.Text,
                         db.ForeignKey("users.username"),
                         nullable=False)