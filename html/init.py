from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def hs():
    return render_template('index.html')