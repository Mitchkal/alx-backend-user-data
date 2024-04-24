#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base
from user import User


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        saves user to database and returns User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()

        return (new_user)

    def find_user_by(self, **kwargs) -> User:
        """
        find user by arbitrary arguments and returns
        first row with user
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user

        except NoResultFound:
            raise NoResultFound

        except InvalidRequestError as e:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        locates a uset and updates their attributes
        as passed in arguments
        """
        user = self.find_user_by(id=user_id)

        for key, val in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, val)
            else:
                raise ValueError(f"Invalid user attribute: {key}")

        self._session.commit()
