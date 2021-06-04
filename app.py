from menu import Menu
from src.common.database import Database
from flask import Flask


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

if __name__ == '__main__':
    app.run()
