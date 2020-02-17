
from flask import Flask, abort, jsonify, send_file, make_response
import redis
import requests
import datetime
import csv
import json
import os
import model


app          = Flask(__name__)
base_api_uri = "http://weather.livedoor.com/forecast/webservice/json/v1?city="
r            = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0)
csv_header   = '日付,都市,天気,最低気温,最高気温'


def filter_forecasts(city, forecasts):
    forecasts_filterd = ''

    for forecast in forecasts:
        date  = forecast['date']
        telop = forecast['telop']
        
        if forecast['temperature']['min'] is not None:
            min_temp = forecast['temperature']['min']['celsius']
        else:
            min_temp = '-'

        if forecast['temperature']['max'] is not None:
            max_temp = forecast['temperature']['max']['celsius']
        else:
            max_temp = '-'

        forecasts_filterd += date + ',' + city + ',' + telop + ',' + min_temp + ',' + max_temp + '\n'

    return forecasts_filterd


@app.route('/api/city/<city_code>')
def get_weather(city_code):
    csv      = city_code + '.csv'
    api_uri  = base_api_uri + city_code
    response = make_response()
    response.headers['Content-Disposition'] = 'attachment; filename=' + csv

    if r.get(city_code) != None:
        print('hit redis')
        print(city_code)
        response.data = r.get(city_code)
        return response

    try:
        api_response = requests.get(api_uri).json() 
    except:
        print('error: api url is wrong!')
        abort(404)

    city          = api_response['location']['city']
    forecasts     = csv_header + '\n' + filter_forecasts(city, api_response['forecasts'])
    response.data = forecasts

    r.set(city_code, forecasts)
    r.expire(city_code, 300)

    return response


@app.route('/api/cities')
def list_weather():
    city_code_all = 'all'
    csv           = city_code_all + '.csv'
    forecasts     = ''
    response      = make_response()
    response.headers['Content-Disposition'] = 'attachment; filename=' + csv

    if r.get(city_code_all) != None:
        print('hit redis')
        print(city_code_all)
        response.data = r.get(city_code_all)
        return response

    for city_code in model.list_city_code():
        api_uri = base_api_uri + city_code

        try:
            api_response = requests.get(api_uri).json() 
        except:
            print('error: api url is wrong!')
            abort(404)
        
        city       = api_response['location']['city']
        forecasts += filter_forecasts(city, api_response['forecasts'])

    forecasts     = csv_header + '\n' + forecasts
    response.data = forecasts
    r.set(city_code_all, forecasts)
    r.expire(city_code, 300)

    return response


if __name__ == "__main__":
    app.run()