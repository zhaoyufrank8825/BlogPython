from flask import session
from src.models.blog import Blog
from src.common.database import Database
import uuid


class User:
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        user = Database.find_one("users", {"email": email})
        if user is not None:
            return cls(**user)

    @classmethod
    def get_by_id(cls, id):
        user = Database.find_one("users", {"_id": id})
        if user is not None:
            return cls(**user)

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session["email"] = email
            return True
        else:
            return False

    @staticmethod
    def login(email):
        session["email"] = email

    @staticmethod
    def logout():
        session["email"] = None   

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        blog = Blog(self.email, title, description, self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title, content)

    def json(self):
        return {
            "email": self.email,
            "password": self.password,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())
