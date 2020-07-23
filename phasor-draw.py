from flask import Flask, render_template, request, jsonify
import command_processor, phasor

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    a = phasor.Phasor(300, 400, True, 'a', True)
    b = phasor.Phasor(4, 3, True, 'b', True)
    c = phasor.Phasor(1, 1, True, 'c', True)
    return render_template('arrows.html')

@app.route('/reqprocess', methods=['POST'])
def process():
    xy = phasor.Phasor.draw_all_phasors()
    res = jsonify(xy), 200
    return res
