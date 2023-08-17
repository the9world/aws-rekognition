from flask import request
from flask_restful import Resource
import requests
from config import Config

class TMapRoute(Resource):
    def post(self):
        try:
            data = request.json

            if not data or 'start' not in data or 'waypoints' not in data or 'end' not in data:
                return {'error': '잘못된 요청입니다. 필수 항목: start, waypoints, end'}, 400

            start = data['start']
            waypoints = data['waypoints']
            end = data['end']

            waypoints_string = "|".join([f"{waypoint['longitude']},{waypoint['latitude']}" for waypoint in waypoints])

            TMAP_API_KEY = Config.tmap_app_key
            url = f'https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&format=json&appKey={TMAP_API_KEY}&startX={start["longitude"]}&startY={start["latitude"]}&endX={end["longitude"]}&endY={end["latitude"]}&passList={waypoints_string}'

            response = requests.get(url)
            response_data = response.json()

            return response_data, 200

        except Exception as e:
            return {'error': str(e)}, 500
