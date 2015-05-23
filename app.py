# PROGULARITY

import decimal, datetime
from flask import Flask, json
from flask.ext.sqlalchemy import SQLAlchemy
 
app = Flask(__name__, static_url_path='')
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stats'
db = SQLAlchemy(app)


def alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def month_stats() -> json:
    """ Return all results from db """
    #res = db.engine.execute("SELECT * FROM reddit")
    res = db.engine.execute("SELECT * FROM reddit WHERE strftime('%m', date) = '05' GROUP BY language")
    return json.dumps([dict(r) for r in res], default=alchemyencoder)


def all_stats() -> json:
    res = db.engine.execute("SELECT * FROM reddit")
    return json.dumps([dict(r) for r in res], default=alchemyencoder)


@app.route('/')
def root():
    #response = requests.get("https://oauth.reddit.com/r/elm/top?sort=top&t=day&limit=999", headers=headers)
    #data = json.loads(response.text)
    #return jsonify(data)
    #return str(len(data['data']['children']))
    return all_stats()

# TODO
@app.route('/week')
def week():
    return "Last week."

# TODO
@app.route('/month')
def month():
    return "Last month."

# TODO
@app.route('/year')
def year():
    return "Data for this year"

# TODO
@app.route('/alltime')
def all():
    return "All time"



if __name__ == "__main__":
    app.debug = True
    app.run()