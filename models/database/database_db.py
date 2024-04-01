#!/usr/bin/python3
"""
Contains the class DBStorage
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import os


class DBStorage:
    """
    DBStorage class to interact with MySQL database using SQLAlchemy.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes a new instance of DBStorage.
        """
        user = os.environ.get('SOLYSIS_MYSQL_USER')
        password = os.environ.get('SOLYSIS_MYSQL_PWD')
        host = os.environ.get('SOLYSIS_MYSQL_HOST', 'localhost')
        db = os.environ.get('SOLYSIS_MYSQL_DB')

        if user is None or password is None or db is None:
            raise ValueError("MySQL credentials are not provided")

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, password, host, db),
            pool_pre_ping=True)

        if os.environ.get('SOLYSIS_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session all objects depending on the class name (argument cls).
        If cls=None, query all types of objects (User, Post).
        Returns a dictionary: key = <class-name>.<object-id>, value = object.
        """
        objects = {}
        if cls is not None:
            query_result = self.__session.query(cls).all()
            for obj in query_result:
                key = "{}.{}".format(cls.__name__, obj.id)
                objects[key] = obj
        else:
            all_classes = [User, Post, SocialMediaPost]  # Import classes here
            for cls in all_classes:
                query_result = self.__session.query(cls).all()
                for obj in query_result:
                    key = "{}.{}".format(cls.__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """
        Add the object to the current database session (self.__session).
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session (self.__session).
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database and create the current database session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
