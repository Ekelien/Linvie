from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from linvie.adapters import AbstractRepository as repo
from linvie.adapters.ORM import map_model_to_tables
from linvie.adapters.Repository import SqlAlchemyRepository
from linvie.blueprint.UserService import service

engine = create_engine('sqlite:///test.db', echo=False)
clear_mappers()
map_model_to_tables()
session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
repo.db = SqlAlchemyRepository(session_factory)


def test_get_user():
    user = service.get_user('ekelien', repo)
    assert user.username == 'ekelien'
    assert len(user.favorite) == 3


def test_add_user():
    service.add_user('haly', '6666', repo)
    user = service.get_user('haly', repo)
    assert user.username == 'haly'
    repo.db.scm.session.delete(user)
    repo.db.scm.session.commit()


def test_add_user_with_exist_name():
    try:
        service.add_user('ekelien', 'momomomomo', repo)
        assert False
    except:
        assert True


def test_like_a_movie():
    service.add_user('haly', '6666', repo)
    user = service.get_user('haly', repo)
    service.like('0', 'haly', repo)
    assert len(user.favorite) == 1
    assert user.favorite[0].ID == 0
    repo.db.scm.session.delete(user)
    repo.db.scm.session.commit()


def test_dislike_a_movie():
    service.add_user('haly', '6666', repo)
    user = service.get_user('haly', repo)
    service.like('0', 'haly', repo)
    assert len(user.favorite) == 1
    assert user.favorite[0].ID == 0
    service.dislike('0', 'haly', repo)
    assert len(user.favorite) == 0
    repo.db.scm.session.delete(user)
    repo.db.scm.session.commit()
