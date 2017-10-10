from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

@app.route("/", methods=['GET', 'POST'])
def get_request():
    if request.method == 'POST':
        payload = request.get_json(silent=True)
        print "Got data: " + str(payload) 
        print "Hello, " + payload['hello']['name']
        return {'succeeded with query' : str(payload)}

if __name__ == "__main__":
    app.run(debug=True)
