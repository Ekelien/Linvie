from flask import Blueprint, render_template, request

import linvie.adapters.AbstractRepository as repo
from linvie.form.search_form import SearchForm

genre_blueprint = Blueprint('genre_bp', __name__)


@genre_blueprint.route('/genre', methods=['GET', 'POST'])
def genre():
    form = SearchForm()
    genre_id = request.args.get('id')
    return render_template(
        "General/index.html",
        form=form,
        alphabet=repo.db.search_index(),
        dictionary=repo.db.genre_movie_dictionary(genre=repo.db.find_genre(genre_id))
    )
