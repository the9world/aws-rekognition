#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import json
from flask import request
import boto3
from config import Config
from flask_restful import Resource

# '/photo'로 들어온 것을 해당 PhotoResource로 처리
class DetectResource (Resource):
    def post(self):
        # 이미지 파일을 Bytes로 변환 (S3 Bucket을 사용 안할 경우 필요함 form-data key 이름과 같아야함.)
        image_bytes = request.files['photo'].read()
        # REST API(PostMan)을 사용하지 않고 로컬에서 직접 파일을 지정할 경우 with open
        # with open('path_to_your_local_photo.jpg', 'rb') as image_file:
        # image_bytes = image_file.read()
        
        # from flask import request, file로 들어온 것을 처리(body: Value의 파일)
        # 업로드 된 사진을 확인. 현재에선 postMan으로 입력된 사진
        print(request.files)        
        
        # 사진 필수, 사진이 등록되지 않을 경우 : (form-data로 들어온 파일 중에 photo가 있는지 확인)
        if 'photo' not in request.files :
            return {'result': 'fail', 'error': '필수항목 확인'}, 400
        
        # boto3 객체 생성
        # client=boto3.client('rekognition') 는 인증 정보(인증 키)가 지정되지 않았기에, 시스템 환경 변수나 AWS 설정 파일을 통해 인증 정보를 찾음
        client=boto3.client('rekognition', 
                            'us-east-1',
                            aws_access_key_id = Config.aws_access_key_id,
                            aws_secret_access_key = Config.aws_secret_access_key)
        
        # client: Amazon Rekognition 클라이언트 객체. 이 객체를 통해 서비스와 통신하여 이미지 처리를 수행.
        # detect_faces: Amazon Rekognition의 detect_faces 메서드를 호출하여 얼굴 감지를 수행.
        # Image=request.files: request.files에서 이미지 데이터를 가져와서 사용. request.files는 Flask 애플리케이션에서 업로드된 파일들을 관리하는 객체.
        # Attributes=['ALL']: 얼굴 감지 시 반환할 속성을 설정. 'ALL'은 모든 가능한 속성(성별, 나이 등)을 반환하라는 의미.
        response = client.detect_faces(Image={'Bytes': image_bytes},Attributes=['ALL'])
        # Image={'S3Object':{'Bucket':bucket,'Name':photo} 이렇게 사용 할 경우
        # 해당 버킷에서 photo라는 변수의 파일을 지정, (photo는 메서드 매개변수임, 원 변수는 iso포매팅한 fileName)
        
        # 버킷에서 불러올 경우 버킷에 업로드도 해야한다.
        # 유저가 올린 파일을 변수로 만든다.
        # file = request.files['photo']
        
        # # 파일명을 유니크하게 만들어준다. (datetime)
        # current_time = datetime.now() # 현재 시간 가져오기
        # print(current_time.isoformat().replace(':','_').replace(':','_')+'.jpg') 
        # # 문자열로 변환 및 파일명
        # new_filename = current_time.isoformat().replace(':','_').replace('.','_')+'.jpg'
        # s3.upload_fileobj(file,
        #             Config.S3_BUCKET,
        #             new_filename,
        #             ExtraArgs={'ACL':'public-read', 'ContentType':'image/jpeg'})
        
        
        for faceDetail in response['FaceDetails']:
                    print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) 
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')

        print('Here are the other attributes:')
        print(json.dumps(faceDetail, indent=4, sort_keys=True))

		# Access predictions for individual face details and print them
        print("Gender: " + str(faceDetail['Gender']))
        print("Smile: " + str(faceDetail['Smile']))
        print("Eyeglasses: " + str(faceDetail['Eyeglasses']))
        print("Emotions: " + str(faceDetail['Emotions'][0]))

        return response['FaceDetails']
    
    
class ComepareResouece(Resource):
    def post(self):
        # 이미지 파일을 Bytes로 변환 (S3 Bucket을 사용 안할 경우 필요함 form-data key 이름과 같아야함.)
        image_bytes1 = request.files['photo1'].read()
        image_bytes2 = request.files['photo2'].read()
        # postman이 아닌 로컬에서 직접 파일을 지정할 경우 with open
        # with open('path_to_your_local_photo.jpg', 'rb') as image_file:
        # image_bytes = image_file.read()
        
        # from flask import request, file로 들어온 것을 처리(body: Value의 파일)
        # 업로드 된 사진을 확인. 현재에선 postMan으로 입력된 사진
        print(request.files)
        #  ImmutableMultiDict([('photo1', <FileStorage: '침착맨.jpg' ('image/jpeg')>),
        # ('photo2', <FileStorage: '2023-01-13T03_31_12.564141.jpeg' ('image/jpeg')>)])
        # Flask 애플리케이션에서 POST 요청을 처리하고 얻은 파일 업로드 정보.
        # 여기서 'photo1'과 'photo2'는 각각 키로 사용되는 파일 업로드의 이름을 나타내며,
        # <FileStorage> 객체는 실제 업로드된 파일 정보를 나타냄
        # 키 'photo1'에 해당하는 파일은 '침착맨.jpg'로, MIME 타입이 'image/jpeg'인 JPEG 이미지 파일.
        # 키 'photo2'에 해당하는 파일은 '2023-01-13T03_31_12.564141.jpeg'로, 마찬가지로 MIME 타입이 'image/jpeg'인 JPEG 이미지 파일.
        # 클라이언트로부터 업로드된 파일들을 Flask 애플리케이션에서 받아온 것을 나타내며, 이 정보를 활용하여 AWS Rekognition과 같은 서비스를 이용하여 이미지 처리 작업을 수행할 수 있음
        
        # boto3 객체 생성
        # client=boto3.client('rekognition') 는 인증 정보(인증 키)가 지정되지 않았기에, 시스템 환경 변수나 AWS 설정 파일을 통해 인증 정보를 찾음
        client=boto3.client('rekognition', 
                            'us-east-1',
                            aws_access_key_id = Config.aws_access_key_id,
                            aws_secret_access_key = Config.aws_secret_access_key)
        try:        
            response=client.compare_faces(SimilarityThreshold=0,
                                          # =int 이하이면 불일치로 판단한다. 일치율 보여주려면 0으로 하고 match 관련 로직 작성
                                          # 일치율이 불필요하다면 ex)90으로 할 경우 90% 미만은 [] 빈 리스트를 반환하니까
                                          # 해당 빈 리스트에 대한 로직을 작성한다.
                                    SourceImage={'Bytes': image_bytes1},
                                    TargetImage={'Bytes': image_bytes2})

            matching_results = []
            for faceMatch in response['FaceMatches']:
                # 각 얼굴 매칭 정보에서 얼굴의 위치 정보를 추출하여 'position' 변수에 저장
                position = faceMatch['Face']['BoundingBox']
                # 각 얼굴 매칭 정보에서 유사성 정보를 추출하여 문자열 형태로 'similarity' 변수에 저장
                similarity = str(faceMatch['Similarity'])
                print('The face at ' +
                    str(position['Left']) + ' ' +
                    str(position['Top']) +
                    ' matches with ' + similarity + '% confidence')
                
                # 일치율이 95% 이하일 경우 'No Match'로 표시하고, 그 이상일 경우 'Match'로 표시
                match_status = 'No Match' if faceMatch['Similarity'] < 95 else 'Match'
                matching_result = {
                    'Position': position,
                    'Similarity': faceMatch['Similarity'],
                    'MatchStatus': match_status
                }
                matching_results.append(matching_result)
                return matching_results
        
            if matching_results["MatchStatus"] == "No Match":
                
                return
                
        
        except Exception as e:
            return {'result': 'fail', 'error': '사진 파일이 잘못 되었습니다.'}, 500

        