from flask import Flask

app = Flask(__name__) # just referencing this file

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)

    