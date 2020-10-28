from sqlalchemy import (
    Table, MetaData, Column, Integer, String,
    ForeignKey)
from sqlalchemy.orm import mapper, relationship

from linvie.domain import model

metadata = MetaData()

people = Table(
    'people', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    # directed
    # participated
    Column('image', String(255))
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('year', String(4), nullable=False),
    Column('info', String(255)),
    Column('director', ForeignKey('people.id')),
    # genres
    Column('image', String(255)),
    Column('file', String(255))
)

movie_directed_table = Table(
    'movie_directed', metadata,
    Column('movie_id', ForeignKey('movies.id')),
    Column('person_id', ForeignKey('people.id'))
)
movie_participated_table = Table(
    'movie_participated', metadata,
    Column('movie_id', ForeignKey('movies.id')),
    Column('person_id', ForeignKey('people.id'))
)
genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    # movies
    Column('image', String(255))
)
movie_classication_table = Table(
    'movie_classication', metadata,
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)
users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)
favorite = Table(
    'favorite', metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id'))
)
comments = Table(
    'comments', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('comment', String(1024), nullable=False),
    Column('time', String(255), nullable=False)
)


def map_model_to_tables():
    mapper(model.People, people, properties={
        '_id': people.c.id,
        '_name': people.c.name,
        '_directed': relationship(model.Movie, secondary=movie_directed_table, back_populates='_directors'),
        '_participated': relationship(model.Movie, secondary=movie_participated_table, back_populates='_actors'),
        '_image': people.c.image

    })

    mapper(model.Movie, movies, properties={
        '_id': movies.c.id,
        '_name': movies.c.name,
        '_year': movies.c.year,
        '_info': movies.c.info,
        '_directors': relationship(model.People, secondary=movie_directed_table, back_populates='_directed'),
        '_actors': relationship(model.People, secondary=movie_participated_table, back_populates='_participated'),
        '_genres': relationship(model.Genre, secondary=movie_classication_table, back_populates="_movies"),
        '_comments': relationship(model.Comment),
        '_image': movies.c.image,
        '_file': movies.c.file
    })

    mapper(model.Genre, genres, properties={
        '_id': genres.c.id,
        '_name': genres.c.name,
        '_movies': relationship(model.Movie, secondary=movie_classication_table, back_populates='_genres'),
        '_image': genres.c.image
    })

    mapper(model.User, users, properties={
        '_id': users.c.id,
        '_username': users.c.username,
        '_password': users.c.password,
        '_comments': relationship(model.Comment, backref='_user'),
        '_favorite': relationship(model.Movie, secondary=favorite)
    })
    mapper(model.Comment, comments, properties={
        '_id': comments.c.id,
        '_user_id': comments.c.user_id,
        '_movie_id': comments.c.movie_id,
        '_comment': comments.c.comment,
        '_time': comments.c.time
    })
