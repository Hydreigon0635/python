from flask import *
import Astar
import json

app = Flask(__name__)

@app.route('/')
def data_import():
    # data = '{"car_id":"aaa","start":"tag_n_connect_000_id", "goal":"tag_n_connect_004_id", "disable":[]}'

    contents = request.args.get('data', '')
    data_json = json.loads(contents)
    print(type(data_json))
    print(data_json["start"])
    print(data_json["goal"])
    re = Astar.a_star(data["start"], data["goal"], data["disable"])
    return jsonify(re)
    

if __name__ == "__main__":
    app.run(debug = True)
