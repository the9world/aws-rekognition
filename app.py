from flask import Flask
from flask_restful import  Api


# AWS의 여러 서비스들을 이용할 수 있는 파이썬 라이브러리(boto3)
import boto3
from resources.rekognition import ComepareResouece, DetectResource


app = Flask(__name__)
api = Api(app)

# api Resource 생성 

# api : Flask 애플리케이션에서 RESTful API를 관리하는 역할
# add_resource: Fask-RESTful API 객체에서 제공, 새로운 리소스(자원)를 API에 추가할 때 사용.
# PhotoResource: 새로운 리소스 클래스를 나타낸다. 이 클래스는 '/photo' 경로에 대한 동작과 로직을 정의.
# /photo':새로운 리소스의 경로. '/photo' 경로는 이 리소스가 접근 가능한 엔드포인트를 나타냄.
# 클라이언트가 이 경로로 요청을 보내면 PhotoResource 클래스에서 정의된 동작이 실행

# PhotoResource 클래스를 생성하고,
# '/photo' 경로에 해당하는 엔드포인트를 Flask 애플리케이션의 API에 추가하는 역할.
# 클라이언트가 '/photo' 경로로 요청을 보내면 PhotoResource 클래스의 메서드들이 실행되어 해당 요청에 대한 응답을 생성합니다.

api.add_resource( DetectResource ,  '/rekognition/detect')
api.add_resource( ComepareResouece ,  '/rekognition/compare')

if __name__ == '__main__':
    app.run()