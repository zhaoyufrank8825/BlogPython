import datetime, uuid
from models.post import Post
from database import Database


class Blog:
    def __init__(self, author, title, description, id=None) -> None:
        self.author = author
        self.title = title
        self.description = description
        self.id = uuid.uuid4().hex if id is None else id
    
    def new_post(self):
        title = input("Enter post title: ")
        content = input("Enter post content: ")
        post = Post(blog_id = self.id, 
                    title=title, 
                    content=content, 
                    author=self.author, 
                    date=datetime.datetime.utcnow())
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self.id)

    def save_to_mongo(self):
        Database.insert(collection="blogs", data=self.json())

    def json(self):
        return {
            "author": self.author,
            "title": self.title,
            "description": self.description,
            "id": self.id
        }
    
    @classmethod
    def from_mongo(cls, id):
        blog = Database.find_one("blogs", {"id":id})
        return cls(author=blog["author"],
                    title=blog["title"],
                    description=blog["description"],
                    id=blog["id"])

    
