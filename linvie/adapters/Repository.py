import random
import string
from difflib import SequenceMatcher

from flask import _app_ctx_stack
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from linvie.adapters.AbstractRepository import AbstractRepository
from linvie.domain import model


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self.scm = SessionContextManager(session_factory)

    def close_session(self):
        self.scm.close_current_session()

    def reset_session(self):
        self.scm.reset_session()

    def find(self, keyword: str):
        keyword = keyword.strip()
        match, similar = [], []

        movies = self.scm.session.query(model.Movie).all()
        people = self.scm.session.query(model.People).all()
        for lis in [movies, people]:
            for item in lis:
                similarity = SequenceMatcher(None, item.name.lower(), keyword.lower()).ratio()
                if similarity == 1:  # found
                    match.append(item)
                elif similarity >= 0.7:
                    similar.append(item)
                elif keyword.lower() in item.name.lower():
                    similar.append(item)
        return match, similar

    def movie_filter(self, genre: list = None, start_year: int = None, end_year: int = None):
        pass

    def random_movie(self, genre=[], number=12):
        match = []
        i = 0
        movies = self.scm.session.query(model.Movie).all()
        if genre == []:
            while i < number:
                movie = random.choice(movies)
                if movie not in match:
                    match.append(movie)
                    i += 1
            return match
        while i < number:
            random_num = random.randrange(0, len(genre))
            movie_list = self.scm.session.query(model.Genre).filter(
                model.Genre._name == genre[random_num]._name).one().movies
            movie = random.choice(movie_list)
            if movie not in match:
                match.append(movie)
                i += 1
        return match

    def first_n_movie(self, number=4):
        movies = []
        for i in range(number):
            movies.append(self.scm.session.query(model.Movie).filter(model.Movie._id == i).one())
        return movies

    def find_movie(self, movie_id):
        try:
            return self.scm.session.query(model.Movie).filter(model.Movie._id == movie_id).one()
        except NoResultFound:
            return None

    def find_people(self, people_id):
        try:
            return self.scm.session.query(model.People).filter(model.People._id == people_id).one()
        except NoResultFound:
            return None

    def find_genre(self, genre_id):
        try:
            return self.scm.session.query(model.Genre).filter(model.Genre._id == genre_id).one()
        except NoResultFound:
            return None

    def sorted_dictionary(self, keyword):
        '''
        keyword should be: 'actor','director','genre'
        '''
        return_dict = {}
        for letter in string.ascii_uppercase:
            return_dict[letter] = []
        return_dict["#"] = []
        if keyword == 'actor':
            temp = [people for people in self.scm.session.query(model.People).all() if people.is_actor()]
        elif keyword == 'director':
            temp = [people for people in self.scm.session.query(model.People).all() if people.is_director()]
        elif keyword == 'genre':
            temp = self.scm.session.query(model.Genre).all()
        else:
            raise TypeError
        for item in temp:
            try:
                return_dict[item.name[0].upper()].append(item)
            except KeyError:
                return_dict["#"].append(item)
        return return_dict

    def genre_movie_dictionary(self, genre):
        return_dict = {}
        for letter in string.ascii_uppercase:
            return_dict[letter] = []
        return_dict["#"] = []
        temp = self.scm.session.query(model.Genre).filter(model.Genre._id == genre._id).one().movies
        for item in temp:
            try:
                return_dict[item.name[0].upper()].append(item)
            except KeyError:
                return_dict["#"].append(item)
        return return_dict

    def get_user(self, username) -> model.User:
        try:
            return self.scm.session.query(model.User).filter(model.User._username == username).one()
        except NoResultFound:
            return None

    def add_user(self, user):
        self.scm.session.add(user)
        self.scm.commit()

    def find_user_via_id(self, user_id):
        return self.scm.session.query(model.User).filter(model.User._id == user_id).one()

    def generate_user_id(self):
        return len(self.scm.session.query(model.User).all())

    def username_available(self, username):
        if self.get_user(username):
            return False
        return True

    def get_comment(self, comment_id) -> model.Comment:
        return self.scm.session.query(model.Comment).filter(model.Comment._id == comment_id).one()

    def add_comment(self, comment):
        self.scm.session.add(comment)
        self.scm.commit()

    def generate_comment_id(self):
        return len(self.scm.session.query(model.Comment).all())

    def like(self, username, movie_id):
        self.get_user(username).like(self.find_movie(movie_id))
        self.scm.commit()

    def dislike(self, username, movie_id):
        self.get_user(username).dislike(self.find_movie(movie_id))
        self.scm.commit()
