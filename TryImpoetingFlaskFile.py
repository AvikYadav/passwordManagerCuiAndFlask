from flask import Flask
app = Flask(__name__)
from TRial import All
@app.route("/")
def hello():
    return "hello from flask"
@app.route("/passwords")
def setting():
    return All()

app.run()
