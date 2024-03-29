"""Authentication exercise app"""

from flask import Flask, session, request, redirect, render_template, flash, get_flashed_messages
from models import db, connect_db, User, Feedback
from forms import RegisterForm,LoginForm,FeedbackForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///secret_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)

"""Routes for Users"""
@app.route("/")
def home_redirect():
    """Redirect to register page"""

    return redirect("/register")

@app.route("/register",methods=["GET","POST"])
def register():
    """Register form"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password)

        newUser = User(username=user.username,password=user.password,email=email,first_name=first_name,last_name=last_name)
        db.session.add(newUser)
        db.session.commit()
        return redirect(f"/users/{user.username}")
    else:
        return render_template("register_form.html",form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    """Login form"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username,password=password)
        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Bad username/password"]

    return render_template("login_form.html",form=form)
        
@app.route("/users/<username>")
def user_info(username):
    """User information"""
    if "username" not in session:
        raise Unauthorized()
    else:
        user = User.query.get_or_404(username)
        feedback = Feedback.query.filter_by(username=user.username)
        return render_template("user_info.html",feedback=feedback,username=user.username,email=user.email,first_name=user.first_name,last_name=user.last_name)

@app.route("/logout")
def logout():
    """Log a user out"""

    session.pop("username")

    return redirect("/")

@app.route("/users/<username>/delete",methods=["POST"])
def delete_user(username):
    """Remove user from the database"""

    if "username" not in session:
        raise Unauthorized()
    else:
        user = User.query.get_or_404(username)
        user_name = user.username
        
        db.session.delete(user)
        db.session.commit()

        flash(f"{user_name} deleted.")

        return redirect("/")
    
"""Routes for Feedback"""
@app.route("/users/<username>/feedback/add",methods=["GET","POST"])
def add_feedback(username):
    """Add new feedback"""

    if "username" not in session:
        raise Unauthorized()
    else:
        form = FeedbackForm()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            user = username

            newFeedback = Feedback(title=title,content=content,username=user)

            db.session.add(newFeedback)
            db.session.commit()

            return redirect(f"/users/{user}")
        else:
            return render_template("feedback_form.html",form=form)
    
@app.route("/feedback/<int:feedbackid>/update",methods=["GET","POST"])
def update_feedback(feedbackid):
    """Update users feedback"""

    if "username" not in session:
        return Unauthorized()       
    else:
        feedback = Feedback.query.get_or_404(feedbackid)
        form = FeedbackForm(obj=feedback)

        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            
            db.session.commit()
            flash("Feedback updated")

            return redirect(f"/users/{feedback.username}")
        else:
            return render_template("feedback_form.html",form=form)
    
@app.route("/feedback/<int:feedbackid>/delete",methods=["POST"])
def delete_feedback(feedbackid):
    """Delete feedback"""

    if"username" not in session:
        return Unauthorized()
    else:
        feedback = Feedback.query.get_or_404(feedbackid)
        
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted")
        return redirect(f"/users/{feedback.username}")