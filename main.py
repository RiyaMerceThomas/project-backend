from flask import Flask, request
from covid import CovidPredictor
from dengue import DenguePredictor
from infection import InfectionPredictor
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cp = CovidPredictor()
dp = DenguePredictor()
ip = InfectionPredictor()


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/predict_covid_infection", methods=['POST'])
@cross_origin(origin='*')
def predict_covid_infection():
    global cp
    inputdata: dict = request.get_json()
    for x in inputdata.keys():
        inputdata[x] = [inputdata[x]]
    infected = cp.predict_infection(inputdata)
    return {'infected': not not infected}, 200


@app.route("/predict_dengue_infection", methods=['POST'])
@cross_origin(origin='*')
def predict_dengu_infection():
    global dp
    inputdata: dict = request.get_json()
    for x in inputdata.keys():
        inputdata[x] = [inputdata[x]]
    inputdata['bp'] = [dp.convert_bp_to_map(inputdata['bp'][0])]
    infected = dp.predict_infection(inputdata)
    print("Dengue ",infected)
    return {'infected': not not infected}, 200

@app.route("/predict_infection", methods=['POST'])
@cross_origin(origin='*')
def predict_infection():
    global ip
    inputdata: dict = request.get_json()
    print("heydata is here",inputdata)
    for x in inputdata.keys():
        inputdata[x] = [inputdata[x]]
    infected = ip.predict_infection(inputdata)
    print("Infection ",infected)
    return {'infected': infected}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
