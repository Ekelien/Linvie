from functools import wraps

from flask import Blueprint, redirect, url_for, render_template, session

import linvie.adapters.AbstractRepository as repo
from linvie.blueprint.UserService import service
from linvie.form.login_form import LoginForm
from linvie.form.registration_form import RegistrationForm

user_blueprint = Blueprint(
    'user_bp', __name__, url_prefix='/user'
)


@user_blueprint.route('/check', methods=['GET', 'POST'])
def check():
    try:
        if session['username']:
            return redirect(url_for('user_bp.user_home'))
        else:
            return redirect(url_for('user_bp.login'))
    except:
        return redirect(url_for('user_bp.login'))


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_not_unique = None
    if form.validate_on_submit():
        try:
            service.add_user(form.username.data, form.password.data, repo)

            # All is well, redirect the user to the login page.
            return redirect(url_for('user_bp.login'))
        except service.NameNotUniqueException:
            username_not_unique = 'Your username is already taken - please supply another'

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'User/register.html',
        title='Register',
        form=form,
        username_error_message=username_not_unique,
        handler_url=url_for('user_bp.register'),
    )


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_not_recognised = None
    password_does_not_match_username = None

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to lookup the user.
        try:
            user = service.get_user(form.username.data, repo)

            # Authenticate user.
            service.authenticate_user(user.username, form.password.data, repo)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = user.username
            return redirect(url_for('home_bp.home'))

        except service.UnknownUserException:
            # Username not known to the system, set a suitable error message.
            username_not_recognised = 'Username not recognised - please supply another'

        except service.AuthenticationException:
            # User failed, set a suitable error message.
            password_does_not_match_username = 'Password does not match supplied username - please check and try again'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'User/login.html',
        title='Login',
        username_error_message=username_not_recognised,
        password_error_message=password_does_not_match_username,
        form=form
    )


@user_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


@user_blueprint.route('/user_home')
def user_home():
    user = service.get_user(session['username'], repo)
    return render_template(
        'User/home.html',
        user=service.get_user(session['username'], repo)
    )


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('user_bp.login'))
        return view(**kwargs)

    return wrapped_view
