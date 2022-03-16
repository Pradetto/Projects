from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
# import os


app = Flask(__name__) # just referencing this file
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///flashcards.db'
db = SQLAlchemy(app)


class Flashcards(db.Model):

    name = db.Column(db.String(200), primary_key=True) 
    question = db.Column(db.String(500),nullable=False) #nullable means user cannot leave it blank
    answer = db.Column(db.String(500),nullable=False) #nullable means user cannot leave it blank

    def __repr__(self):
        return f'<Dataset {self.name}>'

# db.create_all() # this line create the database file


@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form["content"]
        new_task = Flashcards(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your flashcard"

    else:
        tasks = Flashcards.query.all()
        return render_template("index.html",tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)



# Conencted with SQLite remember to run it type sqlite3 in the terminal and to quit hit ctrl-c twice


#Start interactive python3 shell just typing python3 in terminal
