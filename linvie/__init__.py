from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import linvie.adapters.AbstractRepository as repo
from linvie.adapters.ORM import map_model_to_tables, metadata
from linvie.adapters.Repository import SqlAlchemyRepository


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object("config.Config")

    # create repo

    if test_config:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        database_uri = app.config['TEST_SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)
        clear_mappers()
        map_model_to_tables()

    else:
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)
        map_model_to_tables()

    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
    repo.db = SqlAlchemyRepository(session_factory)

    with app.app_context():
        from .blueprint import home
        from linvie.blueprint.General import index
        from linvie.blueprint.MovieObject import people
        from linvie.blueprint.MovieObject import movie
        from linvie.blueprint.UserService import User
        from linvie.blueprint.MovieObject import genre
        app.register_blueprint(home.home_blueprint)
        app.register_blueprint(people.people_blueprint)
        app.register_blueprint(movie.movie_blueprint)
        app.register_blueprint(index.index_blueprint)
        app.register_blueprint(User.user_blueprint)
        app.register_blueprint(genre.genre_blueprint)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.db, SqlAlchemyRepository):
                repo.db.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.db, SqlAlchemyRepository):
                repo.db.close_session()

    return app
