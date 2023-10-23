import json
from tensorflow import keras
from PIL import Image
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class AiService() :
        def __init__(self):
            self.targetList = ['감성돔' , '넙치농어' , '부시리' , '독가시치' ]
            ## 사진 크기 줄이기 #
            ## 모델 불러오기 : 모델 저장한 경로 넣어줘야함
        def custom_serializer(self, obj):
            if isinstance(obj, np.float32):
                return float(obj)
            raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

        ##이미지 파일을 file에 넣기.
        ##file = sorted(glob.glob('./FishData/jeju/01_rotate 복사본/*.png'))  ##  이미지 파일
        def predictFish(self,file):
            ''' 이미지를 넣어서, 생선 유추하기'''
            ### 사용할 변수들 설정 및 불러오기
            img_height_size =200 # 리사이징할 그림의 높이
            img_width_size =350 # 리사이징할 그림의 넓이
            img_color = 3 # 칼라값 RGB 로 함. RGBA 계획은 파토.
            modelPath = "./app/static/350_200_ForthModel.h5" ## 모데 저장한 경로
            fishmodel = keras.models.load_model(modelPath)            
            image = Image.open(file)
            ## 가져온 이미지 (file)을 RGB로 convert 하기.
            image = image.convert('RGB')
            ## 모델을 위해 데이터 크기를 리사이징
            image = image.resize((img_width_size,img_height_size), Image.Resampling.LANCZOS)
            ## numpy 배열로 바꾸기
            image = np.array(image,dtype=np.int32)
            ## 3차원의 배열 즉 4차원 데이터로 만들고 / normalization 하기.
            image = image.reshape(-1,img_height_size,img_width_size,img_color) / 255.0
            ## 예측하기.
            pred = fishmodel.predict(image)            
            ## 확률이 큰 순서대로 3개 가져오기. (이후 2개로 수정하는 것을 권장. 타겟이 4개 이기 때문; (학공치 제외))
            sorted_indices = np.argsort(pred) 
            
            result = {}
            for i in range(1,3):
                result[self.targetList[sorted_indices[0][-1*i]]] = pred[0][sorted_indices[0][-1*i]]
            return json.dumps(result, default=self.custom_serializer, ensure_ascii=False)