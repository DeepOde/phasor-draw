from flask import Flask, render_template, request, jsonify, session
import command_processor, phasor

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'alohamora9andThreeqauraterS'


@app.route('/')
def index():
    session.permanent = False
    session['userdict'] = {}
    if 'userdict' not in session:
        session['userdict'] = {}
    return render_template('arrows.html')

@app.route('/reqprocess', methods=['POST'])
def process():
    ##Retrieve user's phasor dict and load it in the server
    serialised_phasor_dict = session['userdict'].copy()
    
    #deserialise it
    for key, value in serialised_phasor_dict.items():
        temp_phasor = phasor.Phasor(value['_x'], value['_y'], value['_user_created'], value['_name'], value['_todraw'], value['_color'], value['_beginfrom'])
        
    cmds = request.get_json()
    for cmd in cmds.split('\n'):
        if cmd.strip() != '':
            command_processor.process_input(cmd)

    xy = phasor.Phasor.draw_all_phasors()
    res = jsonify(xy), 200
    return res
