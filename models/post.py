import uuid
from database import Database
import datetime


class Post:
    def __init__(self, blog_id, title, content, author, id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = datetime.datetime.utcnow()
        self.id = uuid.uuid4().hex if id is None else id

    def save_to_mongo(self):
        Database.insert(collection="posts", data=self.json())

    def json(self):
        return {
            "id": self.id,
            "blog_id": self.blog_id,
            "title": self.title,
            "author": self.author,
            "content": self.content,
            "created_date": self.created_date
        }

    @classmethod
    def from_mongo(cls, id):
        post = Database.find_one(collection='posts', query={'id':id})
        return cls(blog_id=post["blog_id"],
                    title=post["title"],
                    content=post["content"],
                    author=post["author"],
                    date=post["created_date"],
                    id=post["id"])

    @staticmethod
    def from_blog(id):
        return [ post for post in Database.find(collection="posts", query={"blog_id":id})]

