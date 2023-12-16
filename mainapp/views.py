from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
import json
import base64
import numpy as np
from django.http import JsonResponse
from .models import Personal, Faceshape, Scalp, Facerecorn
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
from django.conf import settings
import os

# 모델을 불러옵니다. 이 경로는 실제 모델 파일의 위치를 반영해야 합니다.
fmodel_path = os.path.join(settings.BASE_DIR, 'C:/work/pysou/makemeuppro/mainapp/models/', 'shape_vgg16.h5')
fmodel = load_model(fmodel_path)
def main(request):
    return render(request, 'index.html')

def personalcolor_view(request):
    # Your view logic goes here
    return render(request, 'personalcolor.html')

def style_view(request):
    # Your view logic goes here
    return render(request, 'style.html')

def hairloss_view(request):
    # Your view logic goes here
    return render(request, 'hairloss.html')

def hairlossresult_view(request):
    # Your view logic goes here
    return render(request, 'hairlossresult.html')

def personalcolorresult_view(request):
    # Your view logic goes here
    # 모델 함수 여기다가
    # 원 function으로... 분류결과를 db에 넣어야함.
    return render(request, 'personalcolorresult.html')

# def styleresult_view(request):
#     # Your view logic goes here
#     return render(request, 'styleresult.html')


@csrf_exempt
def upload_personal_image(request):
    if request.method == 'POST':
        # JSON 데이터 로딩
        data = json.loads(request.body)
        image_data = data['image_data']
        format, imgstr = image_data.split(';base64,')  # 이미지 포맷과 데이터 분리
        ext = format.split('/')[-1]  # 파일 확장자 추출

        # 이미지 데이터를 ContentFile로 변환
        image_file = ContentFile(base64.b64decode(imgstr), name='personal.' + ext)

        # Personal 모델 인스턴스 생성 및 저장
        new_personal = Personal(
            personal_result=data.get('personal_result', ''),  # 내용, 없다면 빈 문자열
            personal_imgpath=image_file,
            personal_dt=timezone.now(),
        )
        new_personal.save()

        return JsonResponse({'status': 'success', 'personal_id': new_personal.personal_id})
    return JsonResponse({'status': 'fail'})

@csrf_exempt
def upload_faceshape_image(request):
    # 사용자가 웹캠으로 캡처한 이미지를 서버에서 분석하고 결과를 저장
    if request.method == 'POST':
        # JSON 데이터 로딩
        data = json.loads(request.body)
        image_data = data['image_data']
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        # 이미지 데이터를 ContentFile로 변환
        image_file = ContentFile(base64.b64decode(imgstr), name='faceshape.' + ext)
        saved_image_path = default_storage.save('faceshapes/' + image_file.name, image_file)

        # 저장된 이미지로 분석을 수행합니다.
        full_image_path = os.path.join(settings.MEDIA_ROOT, saved_image_path)
        predicted_class, predictions_percent = classify_face_shape(full_image_path)

        # 분석 결과를 Faceshape 인스턴스에 저장합니다.
        new_faceshape = Faceshape(
            faceshape_result=predicted_class,  # 분석 결과
            faceshape_imgpath=saved_image_path,  # 저장된 이미지 경로
            faceshape_dt=timezone.now()  # 현재 시간
        )
        new_faceshape.save()

        return JsonResponse({'status': 'success', 'faceshape_id': new_faceshape.faceshape_id, 'faceshape_result': predicted_class})
    return JsonResponse({'status': 'fail'})



# 이미지 로드 및 전처리(얼굴형)
def classify_face_shape(img_path):
    img = load_img(img_path, target_size=(224, 224))  # 이미지 로드 및 크기 조정
    img_array = img_to_array(img)  # 이미지를 배열로 변환
    img_array = np.expand_dims(img_array, axis=0)  # 행 방향으로 차원 확대
    # 이미지를 분류하고 결과를 반환합니다.
    predictions = fmodel.predict(img_array)
    predictions = fmodel.predict(img_array)
    print('Predictions:', predictions)  # 변환된 이미지의 배열값을 확인
    # 각 클래스에 대한 예측 확률을 백분율로 변환하고 정수로 변환합니다.
    predictions_percent = [int(value * 100) for value in predictions[0]]
    print('Predictions Percent as Integer:', predictions_percent)

    predicted_index = np.argmax(predictions, axis=1)
    print('predicted_index : ', predicted_index)

    # 클래스 이름 정의
    class_names = ['하트형', '직사각형', '계란형', '둥근형', '사각형']
    # 가장 높은 확률을 가진 클래스의 인덱스를 찾습니다. (axis=-1 추가)
    predicted_class = class_names[predicted_index[0]]
    # print('predicted_class : ', predicted_class)

    # 예측된 각 클래스의 확률과 가장 높은 확률을 가진 클래스를 반환합니다.
    return predicted_class, predictions_percent

def styleresult_view(request):

    try:
        # 데이터베이스에서 가장 최근에 추가된 Faceshape 인스턴스를 가져온다.
        latest_faceshape = Faceshape.objects.latest('faceshape_dt')
        img_path = os.path.join(settings.MEDIA_ROOT, str(latest_faceshape.faceshape_imgpath))

        # 이미지 분류 함수를 호출
        predicted_class, predictions_percent = classify_face_shape(img_path)

        # 해당 얼굴형에 맞는 헤어스타일을 Facerecorn 테이블에서 조회 (inner join)
        recommended_hairstyles = Facerecorn.objects.filter(faceshape_result=predicted_class)

        context = {
            'face_shape': predicted_class,
            'predictions_percent': predictions_percent,
            'recommended_hairstyles': recommended_hairstyles
        }
        return render(request, 'styleresult.html', context)
    except Faceshape.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': 'No face shape record found.'})
    except Exception as e:
        return JsonResponse({'status': 'fail', 'message': str(e)})



@csrf_exempt
def upload_scalp_image(request):
    if request.method == 'POST':
        if 'photo' in request.FILES:
            photo = request.FILES['photo']

            # 이미지 파일 처리
            # 파일 확장자를 추출합니다 (예: 'jpg', 'png' 등)
            ext = photo.name.split('.')[-1]

            # Faceshape 모델 인스턴스 생성 및 저장
            new_scalp = Scalp(
                scalp_imgpath=photo,  # 업로드된 이미지 파일
                scalp_dt=timezone.now(),  # 등록일자, 현재 시간으로 설정
                # 기타 필요한 필드들을 추가
            )
            new_scalp.save()

        return JsonResponse({'status': 'success', 'faceshape_id': new_scalp.scalp_id})
    return JsonResponse({'status': 'fail'})