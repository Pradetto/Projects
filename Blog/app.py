from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# sqlite:/// this is relative path sq
# 'sqlite:////Users/michaelpradetto/Desktop/Projects/Blog/posts.db' absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


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


# all_posts = [
#     {
#         'title': 'Post 1',
#         'content': 'This is the content of post 1',
#         'author': 'Mike'
#     },
#     {
#         'title': 'Post 2',
#         'content': 'This is the content of post 2'
#     }
# ]


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()  # only after calling commit it will be saved permanently
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect("/posts")
    else:
        return render_template('edit.html', post=post)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/posts")
    else:
        return render_template('new_post.html')


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
