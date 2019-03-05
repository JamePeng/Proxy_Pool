import sys
sys.path.append("..")
import json

from flask import Flask, render_template
from DB.db_operation import MongoOperator

__all__ = ['app']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get')
def get_proxy():
    db = MongoOperator()
    item = db.select(count=1)
    db.close()
    return json.dumps(item)

@app.route('/count')
def get_count():
    db = MongoOperator()
    count = db.count
    db.close()
    return str(count)