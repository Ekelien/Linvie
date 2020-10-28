from flask import Blueprint, render_template, request, session, redirect, url_for

import linvie.adapters.AbstractRepository as repo
from linvie.blueprint.UserService import service
from linvie.form.comment_form import CommentForm
from linvie.form.search_form import SearchForm

movie_blueprint = Blueprint('movie_bp', __name__)


@movie_blueprint.route('/movie', methods=['GET', 'POST'])
def movie():
    search_form = SearchForm()
    comment_form = CommentForm()

    # get movie id and find movie
    movie_id = request.args.get('id')
    movie_found = repo.db.find_movie(movie_id)
    for comment in movie_found.comments:
        comment.user = repo.db.find_user_via_id(comment.user_id)

    # check if user login
    try:
        user = session['username']
        user = repo.db.get_user(user)
        if movie_found in user.favorite:
            user_like_movie = 1
        else:
            user_like_movie = 0
    except:
        user = None
        user_like_movie = 0

    return render_template(
        'MovieObject/movie.html',
        form=search_form,
        movie=movie_found,
        is_commenting=None,
        comment_form=comment_form,
        user=user,
        user_like_movie=user_like_movie
    )


@movie_blueprint.route('/comment', methods=['GET', 'POST'])
def comment():
    search_form = SearchForm()
    comment_form = CommentForm()

    # get movie id and find movie
    movie_id = request.args.get('id')
    movie_found = repo.db.find_movie(movie_id)
    for comment in movie_found.comments:
        comment.user = repo.db.find_user_via_id(comment.user_id)
    # if not login yet
    # check if user login
    try:
        user = session['username']
        user = repo.db.get_user(user)
        if movie_found in user.favorite:
            user_like_movie = 1
        else:
            user_like_movie = 0
    except:
        return redirect(url_for('user_bp.login'))

    if comment_form.validate_on_submit():
        print(comment_form.comment.data)
        service.add_comment(movie_id, session['username'], comment_form.comment.data, repo)

        return redirect(url_for('movie_bp.movie', id=movie_id))
    return render_template(
        'MovieObject/movie.html',
        form=search_form,
        movie=movie_found,
        is_commenting=True,
        comment_form=comment_form,
        user=user,
        user_like_movie=user_like_movie
    )


@movie_blueprint.route('/like')
def like():
    movie_id = request.args.get('id')
    user = session['username']
    service.like(movie_id, user, repo)
    return redirect(url_for('movie_bp.movie', id=movie_id))


@movie_blueprint.route('/dislike')
def dislike():
    movie_id = request.args.get('id')
    user = session['username']
    service.dislike(movie_id, user, repo)
    return redirect(url_for('movie_bp.movie', id=movie_id))
