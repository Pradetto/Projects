from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# sqlite::/// this is relative path sq
app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite::///Users/michaelpradetto/Desktop/Projects/Blo/posts.db'
db = SQLAlchemy(app)

db.create_all()


class BlogPost(db.Model):
    # main distinguisher between table it's unique
    id = db.Column(db.Integer, primary_key=True)
    # string is limited 100 character and column can't be null
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # says author is required but if not there set it to N/A
    author = db.Column(db.String(20), nullable=False, default="N/A")
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post' + str(self.id)


all_posts = [
    {
        'title': 'Post 1',
        'content': 'This is the content of post 1',
        'author': 'Mike'
    },
    {
        'title': 'Post 2',
        'content': 'This is the content of post 2'
    }
]


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/posts')
def posts():
    return render_template('posts.html', posts=all_posts)


@app.route('/home/<string:name>/posts/<int:id>')
def hello(name, id):
    return "Hello " + name + " your id is: " + str(id)


@app.route('/onlyget', methods=['GET'])
def get_req():
    return 'You can only get this webpage'


if __name__ == "__main__":
    app.run(debug=True)


# this will allow you to pass in the variable name in the url and print it on the screen this is a dynamic URL

# url: http://127.0.0.1:5000/home/Mike/posts/10

# @app.route('/home/<string:name>/posts/<int:id>')
# def hello(name, id):
#     return "Hello " + name + " your id is: " + str(id)


# only allow get methods
# @app.route('/onlyget', methods=['GET'])
# def get_req():
#     return 'You can only get this webpage'
