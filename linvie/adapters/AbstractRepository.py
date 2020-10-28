import string
from abc import ABC, abstractmethod

db = None


class AbstractRepository(ABC):
    @abstractmethod
    def find(self, keyword: str):
        '''
        General finding via keyword
        :param keyword: str
        :return: match: list, similar: list
        '''
        raise NotImplementedError

    @abstractmethod
    def movie_filter(self, genre: list = None, start_year: int = None, end_year: int = None):
        '''
        Advanced search
        :param genre:
        :param start_year:
        :param end_year:
        :return: match: list
        '''
        raise NotImplementedError

    @abstractmethod
    def random_movie(self, genre=[], number=12):
        '''
        Randomly pick movies based on given genre list
        :param genre:
        :param number:
        :return:
        '''
        raise NotImplementedError

    @abstractmethod
    def first_n_movie(self, number=4):
        '''
        Get first several movies based on id
        :param number:
        :return:
        '''
        raise NotImplementedError

    @abstractmethod
    def find_movie(self, movie_id):
        raise NotImplementedError

    @abstractmethod
    def find_people(self, people_id):
        raise NotImplementedError

    @abstractmethod
    def find_genre(self, genre_id):
        raise NotImplementedError

    @abstractmethod
    def sorted_dictionary(self, keyword):
        raise NotImplementedError

    @abstractmethod
    def genre_movie_dictionary(self, genre):
        raise NotImplementedError

    @abstractmethod
    def get_user(self, username):
        raise NotImplementedError

    @abstractmethod
    def add_user(self, user):
        raise NotImplementedError

    @abstractmethod
    def generate_user_id(self):
        raise NotImplementedError

    @abstractmethod
    def username_available(self, username):
        raise NotImplementedError

    @abstractmethod
    def get_comment(self, comment_id):
        raise NotImplementedError

    @abstractmethod
    def add_comment(self, comment):
        raise NotImplementedError

    @abstractmethod
    def generate_comment_id(self):
        raise NotImplementedError

    @abstractmethod
    def like(self, user_id, movie_id):
        raise NotImplementedError

    @abstractmethod
    def dislike(self, user_id, movie_id):
        raise NotImplementedError

    @staticmethod
    def search_index():
        alphabet = list(string.ascii_uppercase)
        alphabet.append("#")
        return alphabet
