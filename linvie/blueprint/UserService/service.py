from werkzeug.security import generate_password_hash, check_password_hash

from linvie.domain.model import Comment, User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(username: str, password: str, repo):
    # Check that the given username is available.
    user = repo.db.get_user(username)
    if user is not None:
        raise NameNotUniqueException
    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)

    # Create and store the new User, with password encrypted.
    user = User(repo.db.generate_user_id(), username, password_hash)
    repo.db.add_user(user)


def get_user(username: str, repo):
    user = repo.db.get_user(username)
    if user is None:
        raise UnknownUserException

    return user


def authenticate_user(username: str, password: str, repo):
    authenticated = False

    user = repo.db.get_user(username)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


def get_comment(comment_id, repo):
    return repo.db.get_comment(comment_id)


def add_comment(movie_id, username, comment_text, repo):
    comment = Comment(repo.db.generate_comment_id(), get_user(username, repo).ID, movie_id, comment_text)
    repo.db.add_comment(comment)


def like(movie_id, username, repo):
    repo.db.like(username, movie_id)


def dislike(movie_id, username, repo):
    repo.db.dislike(username, movie_id)
