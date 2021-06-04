from src.common.database import Database
from src.models.blog import Blog


class Menu:
    def __init__(self) -> None:
        self.user = input("Enter your author name: ")
        self.user_blog = None
        if self._user_has_account():
            print("Welcome back "+self.user)
        else:
            self._prompt_user_for_account()

    def _user_has_account(self):
        blog = Database.find_one("blogs", {"author": self.user})
        if blog is not None:
            self.user_blog = Blog.from_mongo(blog["id"])
            return True
        return False

    def _prompt_user_for_account(self):
        title = input("Enter blog title: ")
        description = input("Enter blog description: ")
        blog = Blog(self.user, title, description)
        blog.save_to_mongo()
        self.user_blog = blog

    def run_menu(self):
        read_or_write = input("Do you want to read (R) or write (W) blogs?")
        if read_or_write == "R":
            self._list_blogs()
            self._view_blog()
        elif read_or_write == "W":
            self.user_blog.new_post()
        else:
            print("Thank you for blogging.")

    def _list_blogs(self):
        blogs = Database.find("blogs", {})
        for blog in blogs:
            print("ID: {}, Title: {}, Author: {}".format(blog["id"], blog["title"], blog["author"]))
    
    def _view_blog(self):
        blog_id = input("Enter the ID of the blog you want to read: ")
        blog = Blog.from_mongo(blog_id)
        for post in blog.get_posts():
            print("Date: {}, Title: {}\n\n{}".format(post["created_date"], post["title"], post["content"]))

