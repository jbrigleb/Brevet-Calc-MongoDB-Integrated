import os
import flask
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.tododb

db.tododb.delete_many({})

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brev = request.args.get('brev',200, type=float)
    start = request.args.get('begin',arrow.now().isoformat(), type=str) 
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME: These probably aren't the right open and close times
    # and brevets may be longer than 200km
    open_time = acp_times.open_time(km, brev, start)
    close_time = acp_times.close_time(km, brev, start)
    if(open_time == "err"):
        result = {"open": open_time, "close": close_time}
    else:    
        result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############


@app.route("/display")
def display():
    
    dili = []
    
    for entry in db.tododb.find():
        dili.append(entry)
    
    flask.render_template('display_test.html',entries = dili)


@app.route('/new', methods=['POST'])
def new():
    
    kmli = request.form.getlist("km")
    loli = request.form.getlist("location")
    opli = request.form.getlist("open")
    clli = request.form.getlist("close")
    for i in range(0, len(kmli)):
        if kmli[i] != "":
            item = {
                'km': kmli[i],
                'location': loli[i],
                'open': opli[i],
                'close': clli[i]
            }
        db.tododb.insert_one(item)

    return redirect("/index")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
