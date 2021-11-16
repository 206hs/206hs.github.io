import sys
from flask import Flask, render_template,request, jsonify
import sqlite3
import string
import random
import os
from datetime import datetime
import platform
import pyotp
app = Flask(__name__)
@app.route('/temp')
def temp():
    return render_template('temp.html')
if __name__=='__main__':
    app.debug=True
    app.run(host="0.0.0.0",port=8000)