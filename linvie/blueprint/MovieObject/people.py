from flask import Blueprint, render_template, request

import linvie.adapters.AbstractRepository as repo
from linvie.form.search_form import SearchForm

people_blueprint = Blueprint('people_bp', __name__)


@people_blueprint.route('/people')
def people():
    form = SearchForm()
    people_id = request.args.get('id')
    person = repo.db.find_people(people_id)

    return render_template(
        'MovieObject/people.html',
        form=form,
        people=person
    )
