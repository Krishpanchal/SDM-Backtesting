from flask import Flask, jsonify, request, send_from_directory
import numpy as np
from joblib import Parallel, delayed
from SDMBT_FR import Backtest
import time
import datetime as dt
import json
from flask_cors import CORS
app = Flask(__name__)
cors = CORS()
cors.init_app(app)
app.config['JSON_SORT_KEYS'] = False


def generate_json(obj):
    json_data = {"std": obj.standard_deviation, "ma": obj.moving_average, "df_json": obj.df_runtime_json,
                 "df_analysis_json": obj.df_analysis_json, "max_position": obj.max_position}
    return json_data


def calculate_sdm(obj):
    obj.build_table()
    obj.build_df_analysis()
    obj.tojson()
    return obj
# request sample : {symbol1,symbol2,startdate,enddate,maxposition}


@app.route('/sdm', methods=['GET'])
def fetch_sdm_data():
    print("request recieved at endpoint /sdm")
    data = request.args
    print(f"->{data.get('symbol1')}")
    input_symbol1 = data.get('symbol1')
    input_symbol2 = data.get('symbol2')
    moving_average_limit = int(data.get('moving_average_limit'))
    risk_free = float(data.get('risk_free'))
    standard_deviation_limit = int(data.get("standard_deviation_limit"))
    print(input_symbol1)
    input_start_date = data.get('start_date').split("-")
    input_start_date = dt.datetime(int(input_start_date[0]), int(
        input_start_date[1]), int(input_start_date[2]))
    input_end_date = data.get('end_date').split("-")
    input_end_date = dt.datetime(int(input_end_date[0]), int(
        input_end_date[1]), int(input_end_date[2]))
    input_max_position = int(data.get("max_position"))
    sdm_combination = []
    sample_obj = Backtest(input_symbol1, input_symbol2,
                          input_start_date, input_end_date, input_max_position, risk_free)
    sample_obj.fetch_data()
    initial_df = sample_obj.df
    # converting date to string so that it becomes easy to show in ui
    initial_df['Date'] = initial_df['Date'].dt.strftime('%Y-%m-%d')
    # std-3-26 ma3-11
    for std in range(3, standard_deviation_limit+1):
        for ma in range(3, moving_average_limit+1):
            obj = Backtest(input_symbol1, input_symbol2, input_start_date,
                           input_end_date, input_max_position, risk_free)
            obj.standard_deviation = std
            obj.moving_average = ma
            obj.greater_sd_ma = obj.standard_deviation if obj.standard_deviation > obj.moving_average else obj.moving_average
            obj.df = initial_df
            sdm_combination.append(obj)

    results = Parallel(n_jobs=-1)(delayed(calculate_sdm)(obj)
                                  for obj in sdm_combination)
    json_list = Parallel(n_jobs=-1)(delayed(generate_json)(obj)
                                    for obj in results)
    # json_list = []
    # for obj in sdm_combination :
    #     result = calculate_sdm(obj)
    #     json_list.append( generate_json (result) )

    print(json_list[0]["df_json"])
    print(len(json_list))
    return jsonify({"result": json_list}), 200


@app.route("/")
def index():
    return send_from_directory(app.static_folder,"index.html")

# ------------------------------------------------------------
if __name__ == "__main__":
    app.run()
