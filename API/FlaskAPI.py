from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import HueController
from colour import Color
import simplejson

app = FlaskAPI(__name__)

hue = HueController.hue_rgb("192.168.1.2")

def set_rgb(rgb):
    rgb = rgb.split(',')
    rgb = map(float, rgb)
    hue.rgb_set(rgb)

def hue_on(state):
    hue.on(state)
    return {'lights' : state}



def handle_hue(payload):
    try:
        hue.set_group(payload['group'])
    except:
        return failed("couldn't get group")
    if(payload.has_key('rgb')):
        try:
            set_rgb(payload['rgb'])
        except:
            return failed("couldn't change rgb")
    if(payload.has_key('on')):
        hue_on(payload['on'])
    return {'API Status' : 'suceeded'}

def failed(result):
    return {
            'api result' : result
            }

@app.route("/", methods=['GET', 'POST'])
def notes_list():
    """
    List or create notes.
    """
    if request.method == 'POST':
#        action = str(request.data.get('action', ''))
        payload = request.get_json(silent=True)
        print payload['action']
        if(payload['action'] == 'hue'):
            return handle_hue(payload['params']);
        else:
            return failed("couldn't get params")

@app.route("/<string:key>/", methods=['GET', 'PUT', 'DELETE'])
def notes_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == 'PUT':
        note = str(request.data.get('text', ''))
        notes[key] = note
        return note_repr(key)

    elif request.method == 'DELETE':
        notes.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in notes:
        raise exceptions.NotFound()
    return note_repr(key)


if __name__ == "__main__":
    app.run(debug=True, host='192.168.1.3')
