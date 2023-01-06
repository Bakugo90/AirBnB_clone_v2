#!/usr/bin/python3
"""databases storage file"""


from sqlalchemy import create_engine
from os import getenv
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy.orm import scoped_session


class DBStorage:
    """database class"""
    __engine = None
    __session = None

    def __init__(self):
        """initialisation function"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(getenv(HBNB_MYSQL_USER),
                                              getenv(HBNB_MYSQL_PWD),
                                              getenv(HBNB_MYSQL_HOST),
                                              getenv(HBNB_MYSQL_DB)),
                                      pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """all methods"""
        cls_dict = {}
        if cls == None:
            objs = self.__session.query(User).all()
            objs.extend(self.__session.query(State).all())
               .extend(self.__session.query(City).all())
               .extend(self.__session.query(Amenity).all())
               .extend(self.__session.query(Place).all())
               .extend(self.__session.query(Review).all())
            for obj in objs:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                cls_dict[key] = obj
        else:
            obj = self.__session.query(eval(cls)):
            key = "{}.{}".format(type(obj).__name__, obj.id)
            cls_dict[key] = obj
        return cls_dict

    def new(self, obj):
        """create new instances"""
        self.__session.add(obj)

    def save(self):
        """saving"""
        self.__session.commit()

    def delete(self, obj=None):
        """deleting"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloading..."""
        from sqlalchemy.orm import sessionmaker
        Base.metadata.create_all(self.__engine)
        session_ = sessionmaker(bind=self.__engine,
                                expire_on_commit=False)
        Session = scoped_session(session_)
        self.__session = Session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
