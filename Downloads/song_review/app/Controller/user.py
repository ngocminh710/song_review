from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request,session
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.Model.models import User
from app.Controller.forms import RegistrationForm,LoginForm

# Configure Blueprint.
authentication_blueprint = Blueprint(
    'authentication', __name__, url_prefix='/authentication')
authentication_blueprint.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None
    if form.validate_on_submit():
        # Successful POST, i.e. the user name and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            u = User(username=form.user_name.data, 
                    password=form.password.data,
                    email = form.email.data,
                    fname = form.FirstName.data,
                    lname = form.LastName.data,
                    )
            db.session.add(u)
            db.session.commit()
            # All is well, redirect the user to the login page.
            return redirect(url_for('authentication.login'))
        except:
            user_name_not_unique = 'please supply another username'

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'authentication/register.html',
        form=form,
        user_name_error_message=user_name_not_unique,
        handler_url=url_for('authentication.register'),
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    password_does_not_match_user_name = None
    if form.validate_on_submit():
        # Successful POST, i.e. the user name and password have passed validation checking.
        # Use the service layer to lookup the user.
        try:
            userin = form.user_name.data
            passwordin = form.password.data
            # Authenticate user.
            user = User.query.filter_by(username=userin).first()
            if not user or (not (user.password==passwordin)): 
                user_name_not_recognised = 'Please check your login details and try again.'
                return redirect(url_for('authentication.login'))
            # Initialise session and redirect the user to the home page.
            session.clear()
            session['user_name'] = user.username
            return redirect(url_for('routes.home'))
        except:
            return redirect(url_for('authentication.login'))

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'authentication/credentials.html',
        user_name_error_message=user_name_not_recognised,
        password_error_message=password_does_not_match_user_name,
        form=form,
    )



@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.index'))


from functools import wraps
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication.login'))
        return view(**kwargs)
    return wrapped_view