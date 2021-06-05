import datetime, uuid
from src.models.post import Post
from src.common.database import Database


class Blog:
    def __init__(self, author, title, description, author_id, _id=None) -> None:
        self.author = author
        self.author_id = author_id
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id
    
    def new_post(self, title, content):
        post = Post(blog_id = self._id, 
                    title=title, 
                    content=content, 
                    author=self.author, 
                    date=datetime.datetime.utcnow())
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection="blogs", data=self.json())

    def json(self):
        return {
            "author": self.author,
            "title": self.title,
            "description": self.description,
            "author_id": self.author_id,
            "_id": self._id
        }
    
    @classmethod
    def from_mongo(cls, id):
        blog = Database.find_one("blogs", {"_id":id})
        return cls(**blog)

    @classmethod
    def find_by_author_id(cls, id):
        blogs = Database.find("blogs", {"author_id":id})
        return [cls(**blog) for blog in blogs]

    
