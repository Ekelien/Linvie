from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from linvie.adapters import AbstractRepository as repo
from linvie.adapters.ORM import map_model_to_tables
from linvie.adapters.Repository import SqlAlchemyRepository
from linvie.domain.model import User, Comment

engine = create_engine('sqlite:///test.db', echo=False)
clear_mappers()
map_model_to_tables()
session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
repo.db = SqlAlchemyRepository(session_factory)


def test_find():
    movie, s = repo.db.find('Iron Man')
    movie = movie[0]
    m, s = repo.db.find('iron man')
    assert movie == m[0]
    m, s = repo.db.find('ion man')
    assert movie in s


def test_random_movie():
    genre = [repo.db.find_genre(0)]
    ml = repo.db.random_movie(genre=genre)
    for movie in ml:
        assert genre[0] in movie.genres


def test_find_movie_name():
    match, similar = repo.db.find("shiranui")
    assert repo.db.find_movie(0) in match


def test_find_movie_name_similar():
    match, similar = repo.db.find("shirani")
    assert repo.db.find_movie(0) in similar


def test_user():
    user = User(100, 'nini', 'nana')
    repo.db.add_user(user)
    user1 = repo.db.get_user('nini')
    assert user1 == user
    try:
        repo.db.add_user(user)
    except:
        assert True
    repo.db.scm.session.delete(user)
    repo.db.scm.session.commit()


def test_comment_read():
    comment = repo.db.get_comment(0)
    assert comment.comment == "fantastic"
    assert comment.user_id == 0
    assert repo.db.find_movie(0) == repo.db.find_movie(comment.movie_id)


def test_add_comment():
    comment = Comment(repo.db.generate_comment_id(), 0, 0, 'ahhh')
    assert repo.db.generate_comment_id() == 1
    repo.db.add_comment(comment)
    comment = repo.db.get_comment(1)
    assert comment.comment == "ahhh"
    assert comment.user_id == 0
    repo.db.scm.session.delete(comment)
    repo.db.scm.session.commit()
