from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hm, you shouldn\'t be able to see that. Weird.'
