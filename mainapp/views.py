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
fmodel_path = os.path.join(settings.BASE_DIR,'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'shape_vgg16.h5')
fmodel = load_model(fmodel_path)

keras_model1_path = os.path.join(settings.BASE_DIR, 'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'dupi_model1.hdf5')
keras_model2_path = os.path.join(settings.BASE_DIR, 'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'dupi_model2.hdf5')
keras_model3_path = os.path.join(settings.BASE_DIR, 'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'dupi_model3.hdf5')
keras_model4_path = os.path.join(settings.BASE_DIR, 'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'dupi_model4.hdf5')
keras_model5_path = os.path.join(settings.BASE_DIR, 'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'dupi_model5.hdf5')
keras_model6_path = os.path.join(settings.BASE_DIR, 'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'dupi_model6.hdf5')

# TensorFlow 및 Keras 모델 로드
keras_model1 = load_model(keras_model1_path)
keras_model2 = load_model(keras_model2_path)
keras_model3 = load_model(keras_model3_path)
keras_model4 = load_model(keras_model4_path)
keras_model5 = load_model(keras_model5_path)
keras_model6 = load_model(keras_model6_path)

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

# def hairlossresult_view(request):
#     # Your view logic goes here
#     return render(request, 'hairlossresult.html')

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
            personal_imgpath=image_file,  # 이미지 파일
            personal_dt=timezone.now(),  # 등록일자, 현재 시간으로 설정
            # personal_id는 자동 증가 필드로 가정, 필요하다면 명시적으로 설정
            # personal_content=data.get('personal_content', None)  # 내용, null 허용 필드
        )
        new_personal.save()

        return JsonResponse({'status': 'success', 'personal_id': new_personal.personal_id})
    return JsonResponse({'status': 'fail'})


@csrf_exempt
def upload_faceshape_image(request):
    if request.method == 'POST':
        # JSON 데이터 로딩
        data = json.loads(request.body)
        image_data = data['image_data']
        format, imgstr = image_data.split(';base64,')  # 이미지 포맷과 데이터 분리
        ext = format.split('/')[-1]  # 파일 확장자 추출

        # 이미지 데이터를 ContentFile로 변환
        image_file = ContentFile(base64.b64decode(imgstr), name='faceshape.' + ext)

        # Faceshape 모델 인스턴스 생성 및 저장
        new_faceshape = Faceshape(
            faceshape_result=data.get('faceshape_result', ''),  # 결과, 없다면 빈 문자열
            faceshape_imgpath=image_file,  # 이미지 파일
            faceshape_dt=timezone.now(),  # 등록일자, 현재 시간으로 설정
            # 기타 필요한 필드들을 추가
        )
        new_faceshape.save()

        return JsonResponse({'status': 'success', 'faceshape_id': new_faceshape.faceshape_id})
    return JsonResponse({'status': 'fail'})


# 이미지 로드 및 전처리(얼굴형)
def classify_face_shape(img_path):
    img = load_img(img_path, target_size=(224, 224))  # 이미지 로드 및 크기 조정
    img_array = img_to_array(img)  # 이미지를 배열로 변환
    # print('img_array : ', img_array[0])
    img_array = np.expand_dims(img_array, axis=0)  # 행 방향으로 차원 확대
    # img_array /= 255.0  # 정규화
    # print('img_array : ', img_array)
    # 이미지를 분류하고 결과를 반환합니다.
    predictions = fmodel.predict(img_array)
    print('Predictions:', predictions)  # 변환된 이미지의 배열값을 확인
    predictions_percent = predictions[0] * 100      # 각 클래스에 대한 예측 확률을 백분율로 변환합니다.

    predicted_index = np.argmax(predictions, axis=1)
    print('predicted_index : ', predicted_index)

    # 클래스 이름 정의
    class_names = ['하트형', '직사각형', '계란형', '둥근형', '사각형']
    # 가장 높은 확률을 가진 클래스의 인덱스를 찾습니다. (axis=-1 추가)
    predicted_class = class_names[predicted_index[0]]
    print('predicted_class : ', predicted_class)

    # 예측된 각 클래스의 확률과 가장 높은 확률을 가진 클래스를 반환합니다.
    return predicted_class, predictions_percent

# classify_face_shape 함수 정의

from django.shortcuts import render
from django.http import JsonResponse
from .models import Faceshape
from django.conf import settings
import os
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

# 여기에 classify_face_shape 함수를 정의해주세요~! .
def styleresult_view(request):
    try:
        # 데이터베이스에서 가장 최근에 추가된 Faceshape 인스턴스를 가져옵니다.
        latest_faceshape = Faceshape.objects.latest('faceshape_dt')

        # MEDIA_ROOT를 사용하여 전체 파일 경로를 구성합니다.
        img_path = os.path.join(settings.MEDIA_ROOT, str(latest_faceshape.faceshape_imgpath))

        # 이미지 분류 함수를 호출합니다.
        predicted_class, predictions_percent = classify_face_shape(img_path)

        # 분류 결과와 확률을 템플릿에 전달합니다.
        context = {
            'face_shape': predicted_class,
            'predictions_percent': predictions_percent
        }
        return render(request, 'styleresult.html', context)
    except Faceshape.DoesNotExist:
        # Faceshape 인스턴스가 없는 경우 오류 메시지와 함께 응답합니다.
        return JsonResponse({'status': 'fail', 'message': 'No face shape record found.'})
    except Exception as e:
        # 기타 예외 처리
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


def classify_scalp_type(img_path):
    img = load_img(img_path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    predictions = [keras_model1.predict(img_array), keras_model2.predict(img_array), ...]
    class_names = [
        ['모낭사이홍반_0.양호', '모낭사이홍반_1.경증', '모낭사이홍반_2.중등도', '모낭사이홍반_3.중증'],
        ['미세각질_0.양호', '미세각질_1.경증', '미세각질_2.중등도', '미세각질_3.중증'],
        ['모낭사이홍반_0.양호', '모낭사이홍반_1.경증', '모낭사이홍반_2.중등도', '모낭사이홍반_3.중증'],
        ['미세각질_0.양호', '미세각질_1.경증', '미세각질_2.중등도', '미세각질_3.중증'],
        ['모낭사이홍반_0.양호', '모낭사이홍반_1.경증', '모낭사이홍반_2.중등도', '모낭사이홍반_3.중증'],
        ['미세각질_0.양호', '미세각질_1.경증', '미세각질_2.중등도', '미세각질_3.중증']
    ]

    results = {}
    for i, (pred, names) in enumerate(zip(predictions, class_names), start=1):
        predicted_class = np.argmax(pred)
        predicted_class_name = names[predicted_class]
        predictions_percent = pred[0] * 100
        results[f'model{i}'] = {
            'predicted_class_name': predicted_class_name,
            'predictions_percent': predictions_percent.tolist(),
            'predicted_class': predicted_class
        }

    # 이진 분류 결과 생성
    result_model1 = 'Good' if class_names[[0]] == 0 else 'Bad'
    result_model2 = 'Good' if class_names[[1]] == 0 else 'Bad'
    result_model3 = 'Good' if class_names[[2]] == 0 else 'Bad'
    result_model4 = 'Good' if class_names[[3]] == 0 else 'Bad'
    result_model5 = 'Good' if class_names[[4]] == 0 else 'Bad'
    result_model6 = 'Good' if class_names[[5]] == 0 else 'Bad'

    # 이진 분류 결과에 따른 최종 결과 생성
    if result_model1 == 'Good' and result_model2 == 'Good' and result_model3 == 'Good' and result_model4 == 'Good' and result_model5 == 'Good' and result_model6 == 'Good':
        final_result = '양호'
    elif result_model1 == 'Bad' and result_model2 == 'Good' and result_model3 == 'Good' and result_model4 == 'Good' and result_model5 == 'Good' and result_model6 == 'Good':
        final_result = '건성'
    elif result_model1 == 'Good' and result_model2 == 'Bad' and result_model3 == 'Good' and result_model4 == 'Good' and result_model5 == 'Good' and result_model6 == 'Good':
        final_result = '지성'
    elif result_model2 == 'Good' and result_model3 == 'Bad' and result_model4 == 'Good' and result_model5 == 'Good' and result_model6 == 'Good':
        final_result = '민감성'
    elif result_model2 == 'Bad' and result_model3 == 'Bad' and result_model4 == 'Good' and result_model6 == 'Good':
        final_result = '지루성'
    elif result_model3 == 'Good' and result_model4 == 'Bad' and result_model6 == 'Good':
        final_result = '염증성'
    elif result_model3 == 'Good' and result_model4 == 'Good' and result_model5 == 'Bad' and result_model6 == 'Good':
        final_result = '비듬성'
    elif result_model1 == 'Good' and result_model2 == 'Good' and result_model3 == 'Good' and result_model4 == 'Good' and result_model5 == 'Good' and result_model6 == 'Bad':
        final_result = '탈모성'
    else:
        final_result = '복합성'

    return results, final_result

from django.shortcuts import render

def hairlossresult_view(request, img_path):
    # 이미지 분류 함수를 호출합니다.
    classification_results, final_result = classify_scalp_type(img_path)

    # 분류 결과와 최종 결과를 템플릿에 전달합니다.
    context = {
        'classification_results': classification_results,
        'final_result': final_result
    }
    return render(request, 'hairlossresult.html', context)

# def hairlossresult_view(request):
#     try:
#         # 데이터베이스에서 가장 최근에 추가된 Scalp 인스턴스를 가져옵니다.
#         latest_scalp = Scalp.objects.latest('scalp_dt')
#
#         # MEDIA_ROOT를 사용하여 전체 파일 경로를 구성합니다.
#         img_path = os.path.join(settings.MEDIA_ROOT, str(latest_scalp.scalp_imgpath))
#
#         # 이미지 분류 함수를 호출합니다.
#         predicted_class, predictions_percent = classify_scalp_image(img_path)
#
#         # 분류 결과와 확률을 템플릿에 전달합니다.
#         context = {
#             'scalp_condition': predicted_class,
#             'predictions_percent': predictions_percent
#         }
#         return render(request, 'hairlossresult.html', context)
#     except ObjectDoesNotExist:
#         # Scalp 인스턴스가 없는 경우 오류 메시지와 함께 응답합니다.
#         return JsonResponse({'status': 'fail', 'message': 'No scalp record found.'})
#     except Exception as e:
#         # 기타 예외 처리
#         return JsonResponse({'status': 'fail', 'message': str(e)})
