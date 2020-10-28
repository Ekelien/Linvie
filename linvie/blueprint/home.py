from flask import Blueprint, render_template, session

import linvie.adapters.AbstractRepository as repo
from linvie.form.search_form import SearchForm

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/')
def start():
    return render_template(
        'General/start.html'
    )


@home_blueprint.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    # check if user login
    try:
        user = session['username']
        user = repo.db.get_user(user)

    except:
        user = None

    if form.validate_on_submit():
        keyword = form.keyword.data

        match, similar = repo.db.find(keyword)
        return render_template(
            'General/search.html',
            match=match,
            similar=similar,
            form=form
        )
    if user:
        return render_template(
            'General/home.html',
            MovieList2=repo.db.random_movie(user.preference),
            MovieList1=repo.db.first_n_movie(),
            form=form
        )
    return render_template(
        'General/home.html',
        MovieList2=repo.db.random_movie(),
        MovieList1=repo.db.first_n_movie(),
        form=form
    )
