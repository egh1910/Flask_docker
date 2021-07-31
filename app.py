from flask import Flask, render_template, make_response, jsonify, request
import traceback

app = Flask(__name__)

PORT = 3200

HOST = '0.0.0.0'

INFO = {
        'languages':{
            'es':'español',
            'fr':'frances',
            'en':'ingles'
        },
        'colors':{
            'r':'red',
            'b':'blue',
            'g':'green'
        },
        'clouds':{
            'AMAZON':'AWS',
            'IBM':'IBM CLOUD',
            'MICROSOFT':'AZURE'
        }
    }

@app.route('/')
def home():
    return "<h1 style='color:blue'> This is home </h1>"
@app.route('/temp')
def template():
    return render_template('index.html')

@app.route('/qstr')
def query_strings():
    if request.args:
        req = request.args
        res = {}
        for key, val in req.items():
            res[key] = val
        res = make_response(jsonify(res), 200)
        return res
    
    res = make_response(jsonify({'error':'no hay query string'}), 400)
    return res

@app.route('/json')
def get_json(): 
    res = make_response(jsonify(INFO), 200)

    return res

@app.route('/json/<collection>/<menber>')
def get_data(collection, menber):
    if collection in INFO:
        menber = INFO[collection].get(menber)
        if menber:
            res = make_response(jsonify({"res":menber}), 200)
            return res

        res = make_response(jsonify({"error": "Not found"}), 404)
        return res

    res = make_response(jsonify({"error": "Not found"}), 404)
    return res

@app.route("/json/<collection>", methods=["POST"])
def create_collection(collection):
    req = request.get_json()
    print('Entra aqui o que pedo', req)
    if collection in INFO:
        res = make_response(jsonify({'error':'La colleccion ya existe'  }))
        return res
    
    INFO.update({collection:req})
    
    res = make_response(jsonify({'message':'collection created '}), 200)
    return res

@app.route("/json/<collection>/<member>", methods=["PUT"])
def update_collection(collection, member):
    req = request.get_json()
    print('Entra aqui o que pedo', req)
    if collection in INFO:
        if member:
            INFO[collection][member] =req['new']
            res = make_response(jsonify({'res':INFO[collection]}), 200)
            return res
    
        res = make_response(jsonify({'error':'Member is not defined '}), 400)
        return res

    res = make_response(jsonify({'error':'collection not found'}), 400)
    return res

@app.route('/json/<collection>', methods=['DELETE'])
def delete_collection(collection):
    if collection in INFO:
        del INFO[collection]
        res = make_response(jsonify(INFO))
        return res
    res = make_response(jsonify({'Error':'collection not found '}), 400)
    return res

if __name__ == '__main__':
    print('server running.... ')
    app.run(host= HOST, port= PORT)

    