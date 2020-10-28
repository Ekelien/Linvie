import time


class TimeStamp(object):

    @staticmethod
    def current_time():
        time_tuple = time.localtime()
        return time.strftime("%d/%m/%Y", time_tuple)


# 'Abstract' Super Class
class Linvie:
    @property
    def ID(self):
        return self._id

    @ID.setter
    def ID(self, other):
        self._id = other

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, other):
        if other == "" or type(other) is not str:
            raise TypeError
        else:
            self._name = other

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, other):
        if other == None:
            self._image = ""
        else:
            self._image = other

    @property
    def type(self) -> list:
        raise NotImplementedError

    @property
    def href(self) -> str:
        raise NotImplementedError


class Movie(Linvie):
    def __init__(self, ID, title, year, info="", image="", file=""):
        self.ID = ID
        self.name = title
        self.year = year
        self.info = info
        self.image = image
        self.file = file
        self.directors = []
        self.actors = []
        self.genres = []
        self.comments = []

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, other):
        if int(other) > 1900:
            self._year = other
        else:
            raise ValueError

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, other):
        self._info = other.strip()

    @property
    def directors(self):
        return self._directors[0]

    @directors.setter
    def directors(self, other):
        self._directors = other

    @property
    def actors(self):
        return self._actors

    @actors.setter
    def actors(self, other):
        self._actors = other

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, other):
        self._genres = other

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, other):
        self._comments = other

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, other):
        self._file = other

    def add_actor(self, actor):
        if actor not in self.actors:
            self.actors.append(actor)

    @property
    def type(self):
        return ['Movie']

    @property
    def href(self):
        return 'movie'

    def remove_actor(self, actor):
        if actor in self.actors:
            self.actors.remove(actor)

    def add_genre(self, genre):
        if type(genre) is Genre and genre not in self.genres:
            self.genres.append(genre)

    def remove_genre(self, genre):
        if type(genre) is Genre and genre in self.genres:
            self.genres.remove(genre)

    def add_comment(self, review):
        self.comments.append(review)

    def set_director(self, other):
        self.directors = [other]

    def __repr__(self):
        return f"<Movie {self.name}>"

    def __eq__(self, other):
        try:
            return self.name + self.year == other.name + other.year
        except:
            return False

    def __lt__(self, other):
        return self.name + str(self.year) < other.name + str(other.year)


class Genre(Linvie):
    def __init__(self, ID, name, image=""):
        self.ID = ID
        self.name = name
        self.image = image
        self.movies = []

    @property
    def movies(self):
        return self._movies

    @movies.setter
    def movies(self, other):
        self._movies = other

    @property
    def type(self):
        return ["Genre"]

    @property
    def href(self):
        return "genre"

    def add_movie(self, other):
        self.movies.append(other)

    def __repr__(self):
        return f"<Genre {self.name}>"

    def __eq__(self, other):
        try:
            return self.name == other.name
        except:
            return False

    def __lt__(self, other):
        return self.name < other.name


class People(Linvie):
    def __init__(self, ID, name, image=""):
        self.ID = ID
        self.name = name
        self.image = image

        self.participated = []
        self.directed = []

    @property
    def directed(self):
        return self._directed

    @directed.setter
    def directed(self, other):
        self._directed = other

    @property
    def participated(self):
        return self._participated

    @participated.setter
    def participated(self, other):
        self._participated = other

    @property
    def type(self):
        temp = []
        if len(self.participated) != 0:
            temp.append('Actor')
        if len(self.directed) != 0:
            temp.append('Director')
        return temp

    @property
    def href(self):
        return 'people'

    # occupation
    def is_actor(self):
        return 'Actor' in self.type

    def is_director(self):
        return 'Director' in self.type

    def participate(self, movie):
        if type(movie) is Movie and movie not in self.participated:
            self.participated.append(movie)

    def direct(self, movie):
        if type(movie) is Movie and movie not in self.directed:
            self.directed.append(movie)

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        try:
            return self.name == other.name
        except:
            return False

    def __repr__(self):
        return f"<{self.name} - {self.type}>"


class User:
    def __init__(self, ID, username, password):
        self.ID = ID
        self.username = username
        self.password = password
        self.comments = []
        self.favorite = []

    @property
    def ID(self):
        return self._id

    @ID.setter
    def ID(self, other):
        self._id = other

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, other):
        self._username = other.strip().lower()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, other):
        if type(other) is str:
            self._password = other

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, other):
        self._comments = other

    def __repr__(self):
        return f"<User {self.username}>"

    def __eq__(self, other):
        try:
            return self.username == other.username
        except:
            return False

    def __lt__(self, other):
        if type(other) is User:
            return self.username < other.username

    def __hash__(self):
        return hash(self.username)

    @property
    def favorite(self):
        return self._favorite

    @favorite.setter
    def favorite(self, other):
        self._favorite = other

    def like(self, movie):
        if movie not in self._favorite:
            self._favorite.append(movie)

    def dislike(self, movie):
        if movie in self._favorite:
            self._favorite.remove(movie)

    def add_comment(self, review):
        if review not in self.comments:
            self.comments.append(review)

    @property
    def preference(self):
        pref = []
        for movie in self.favorite:
            for gen in movie.genres:
                if gen not in pref:
                    pref.append(gen)
        return pref


class Comment:
    def __init__(self, ID, user_id, movie_id, comment, datatime=TimeStamp.current_time()):
        self.ID = ID
        self.user_id = user_id
        self.movie_id = movie_id
        self.comment = comment
        self.time = datatime
        self.user = None

    @property
    def ID(self):
        return self._id

    @ID.setter
    def ID(self, other):
        self._id = other

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, other):
        self._user_id = other

    @property
    def movie_id(self):
        return self._movie_id

    @movie_id.setter
    def movie_id(self, other):
        self._movie_id = other

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, other):
        self._comment = other.strip()

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, other):
        self._time = other

    def renew(self, new_comment):
        self.comment = new_comment
        self.time = TimeStamp.current_time()

    def __eq__(self, other):
        try:
            return self.comment == other.comment
        except:
            return False
