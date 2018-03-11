from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "I am root."

app.run()
