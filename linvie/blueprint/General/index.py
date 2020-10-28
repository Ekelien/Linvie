from flask import Blueprint, render_template, request

import linvie.adapters.AbstractRepository as repo
from linvie.form.search_form import SearchForm

index_blueprint = Blueprint('index_bp', __name__)


@index_blueprint.route("/index")
def index():
    form = SearchForm()
    keyword = request.args.get('keyword')
    return render_template(
        "General/index.html",
        form=form,
        alphabet=repo.db.search_index(),
        dictionary=repo.db.sorted_dictionary(keyword=keyword)
    )
