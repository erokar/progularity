# PROGULARITY

## Ok, men hvordan bør denne strukturen se ut?
# Måned for måned, det er nok.
# måned: [ {language: 'elm', stats: {submissions: 3, ... }}, {}  ]
# år: [ {month: 1, stats: [ månedsdata ] }

import decimal, datetime
from flask import Flask, json, Response
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

    def add_visitors_and_submissions(stat: dict) -> dict:
        average_visitors = stat["accounts_sum"] / stat["days"]
        stat["average_visitors"] = round(average_visitors)
        del stat["accounts_sum"]
        return stat

    res = db.engine.execute("SELECT language, date, sum(submissions) as submissions, subscribers, count(*) as days, SUM(accounts) as accounts_sum FROM reddit WHERE strftime('%m', date) = '05' AND strftime('%Y', date) = '2015' GROUP BY language")
    stats = [add_visitors_and_submissions(s) for s in [dict(r) for r in res]]
    return json.dumps(stats, default=alchemyencoder)




def all_stats() -> json:
    res = db.engine.execute("SELECT * FROM reddit")
    return json.dumps([dict(r) for r in res], default=alchemyencoder)


@app.route('/')
def root():
    #response = requests.get("https://oauth.reddit.com/r/elm/top?sort=top&t=day&limit=999", headers=headers)
    #data = json.loads(response.text)
    #return jsonify(data)
    #return str(len(data['data']['children']))
    return Response(month_stats(), mimetype='application/json')

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