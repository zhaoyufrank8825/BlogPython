from flask import Flask, render_template, request, session, make_response
from models.post import Post
from src.models.blog import Blog
from src.common.database import Database 
from src.models.user import User


app = Flask(__name__)
app.secret_key="zhaoyu"

@app.route("/")
def hello():
    return render_template("login.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.before_first_request
def init_database():
    Database.initialize()

@app.route("/auth/login", methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password):
        User.login(email)
    else:
        session["email"] = None
    return render_template("profile.html", email=session["email"])
    
@app.route("/auth/register", methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    User.register(email, password)
    return render_template("profile.html", email=session["email"])
    
@app.route("/blogs")
def blogs():
    user = User.get_by_email(session['email'])
    blogs = user.get_blogs()
    return render_template("blogs.html", blogs=blogs, user=user)

@app.route("/blogs/new_blog", methods=["GET", "POST"])
def new_blog():
    if request.method == "GET":
        return render_template("new_blog.html")
    else:
        user=User.get_by_email(session['email'])
        title = request.form['title']
        description = request.form['description']
        blog = Blog(user.email, title, description, user._id)
        blog.save_to_mongo()
        return make_response(blogs())

@app.route("/<string:blog_id>/posts")
def posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()
    return render_template("posts.html", posts=posts, blog=blog)

@app.route("/<string:blog_id>/posts/new_post", methods=['GET', 'POST'])
def new_post(blog_id):
    if request.method == "GET":
        return render_template("new_post.html", blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        post = Post(blog_id, title, content, session['email'])
        post.save_to_mongo()
        return make_response(posts(blog_id))

if __name__ == '__main__':
    app.run()
