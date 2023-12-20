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
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
from django.conf import settings
import os
import joblib

# 모델을 불러옵니다. 이 경로는 실제 모델 파일의 위치를 반영해야 합니다.
fmodel_path = os.path.join(settings.BASE_DIR, '../Final-Project/mainapp/models', 'shape_vgg16.h5')
fmodel = load_model(fmodel_path)
pmodel_path = os.path.join(settings.BASE_DIR,'../Final-Project/mainapp/models', 'ensemble_soft_model_poly.h5')
pmodel = joblib.load(pmodel_path)
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

from PIL import Image
import colorsys
import dlib
from sklearn.preprocessing import PolynomialFeatures


def classify_personal_color(img_path):
    image = Image.open(img_path).convert('RGB')  # 이미지 로드 및 크기 조정
    image_array = np.array(image)
    print(image)
    print('image_array : ', image_array)
    # dlib 얼굴 검출기 초기화
    detector = dlib.get_frontal_face_detector()

    # 얼굴 위치 인식
    face_locations = detector(image_array, 2)
    print('face_locations : ', face_locations)
    # 얼굴 영역 추출
    if len(face_locations) > 0:
        # 첫 번째 얼굴만 처리
        top, right, bottom, left = (face_locations[0].top(), face_locations[0].right(),
                                    face_locations[0].bottom(), face_locations[0].left())

        # 얼굴 영역을 크롭
        face_image = Image.fromarray(image_array[top:bottom, left:right])
        print(face_image)
        # 이미지 크기 조정 (모델에 맞게)
        resized_face_image = face_image.resize((100, 100))
        print(resized_face_image)

        # 이미지를 배열로 변환
        face_array = np.array(resized_face_image)

        # 이미지의 평균 색상 계산 (RGB 값 사용)
        average_color_rgb = np.mean(face_array, axis=(0, 1)).astype(int)
        scaled_rgb = average_color_rgb / 255.0

        # RGB 값을 HSV로 변환
        average_color_hsv = colorsys.rgb_to_hsv(*scaled_rgb)

        # RGB 값을 YCbCr로 변환
        average_color_ycbcr = colorsys.rgb_to_yiq(*scaled_rgb)

        # 입력 데이터를 모델에 맞게 변환
        X = np.concatenate([scaled_rgb, average_color_hsv, average_color_ycbcr], axis=0).reshape(1, -1)

        # PolynomialFeatures를 사용하여 피처 확장
        poly = PolynomialFeatures(degree=2, include_bias=False)
        input_data = poly.fit_transform(X)

        print(input_data)

        # 모델 예측
        classifier_personal_color = pmodel.predict(input_data)
        print(classifier_personal_color)

        # 예측 결과 출력
        print(f"퍼스널 컬러 : {classifier_personal_color}")

        return classifier_personal_color


    else:
        print("이미지에서 얼굴을 찾을 수 없습니다.")

# 이미지 파일 저장 경로
IMAGE_PATHS = {
    0: '../static/image/result_spring.jpg',
    1: '../static/image/result_summer.jpg',
    2: '../static/image/result_autumn.jpg',
    3: '../static/image/result_winter.jpg',
}

IMAGE_PATHS_lip = {
    0: '../static/image/result_spring.jpg',
    1: '../static/image/result_summer.jpg',
    2: '../static/image/result_autumn.jpg',
    3: '../static/image/result_winter.jpg',
}

IMAGE_PATHS_eye = {
    0: '../static/image/result_spring.jpg',
    1: '../static/image/result_summer.jpg',
    2: '../static/image/result_autumn.jpg',
    3: '../static/image/result_winter.jpg',
}


IMAGE_PATHS_blur = {
    0: '../static/image/result_spring.jpg',
    1: '../static/image/result_summer.jpg',
    2: '../static/image/result_autumn.jpg',
    3: '../static/image/result_winter.jpg',
}


def personalcolorresult_view(request):
    try:
        # 데이터베이스에서 가장 최근에 추가된 Faceshape 인스턴스를 가져옵니다.
        latest_personal = Personal.objects.latest('personal_dt')

        # MEDIA_ROOT를 사용하여 전체 파일 경로를 구성합니다.
        img_path = os.path.join(settings.MEDIA_ROOT, str(latest_personal.personal_imgpath))

        # 이미지 분류 함수를 호출합니다.
        classifier_personal_color = classify_personal_color(img_path)

        # 결과 값에 따른 퍼스널 컬러 문자열
        personal_color_string = ''
        if classifier_personal_color[0] == 0:
            personal_color_string = '봄 웜톤'
        elif classifier_personal_color[0] == 1:
            personal_color_string = '여름 쿨톤'
        elif classifier_personal_color[0] == 2:
            personal_color_string = '가을 웜톤'
        elif classifier_personal_color[0] == 3:
            personal_color_string = '겨울 쿨톤'

        # personal_color에 따른 이미지 경로
        result_image_path = IMAGE_PATHS.get(classifier_personal_color[0])
        result_image_path_lip = IMAGE_PATHS_lip.get(classifier_personal_color[0])
        result_image_path_eye = IMAGE_PATHS_eye.get(classifier_personal_color[0])
        result_image_path_blur = IMAGE_PATHS_blur.get(classifier_personal_color[0])

        # 분류 결과를 템플릿에 전달합니다.
        context = {
            'personal_color': personal_color_string,
            'result_image_path': result_image_path,
            'result_image_path_lip': result_image_path_lip,
            'result_image_path_eye': result_image_path_eye,
            'result_image_path_blur': result_image_path_blur,
        }
        return render(request, 'personalcolorresult.html', context)
    except Personal.DoesNotExist:
        # Faceshape 인스턴스가 없는 경우 오류 메시지와 함께 응답합니다.
        return JsonResponse({'status': 'fail', 'message': 'No face record found.'})
    except Exception as e:
        # 기타 예외 처리
        return JsonResponse({'status': 'fail', 'message': str(e)})
    return render(request, 'personalcolorresult.html')


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

'''
# 모델 로딩
dupi_model1 = load_model(os.path.join(settings.BASE_DIR, 'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'dupi_model1.hdf5'))
dupi_model2 = load_model(os.path.join(settings.BASE_DIR, 'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'dupi_model2.hdf5'))
dupi_model3 = load_model(os.path.join(settings.BASE_DIR, 'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'dupi_model3.hdf5'))
dupi_model4 = load_model(os.path.join(settings.BASE_DIR, 'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'dupi_model4.hdf5'))
dupi_model5 = load_model(os.path.join(settings.BASE_DIR, 'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'dupi_model5.hdf5'))
dupi_model6 = load_model(os.path.join(settings.BASE_DIR, 'C:/Users/Cho/PycharmProjects/Final-Project/mainapp/models', 'dupi_model6.hdf5'))

# 이미지 분류 함수 정의
def classify_scalp_type(img_path):
    img = load_img(img_path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    predictions = [dupi_model1.predict(img_array), dupi_model4.predict(img_array), dupi_model3.predict(img_array),
                   dupi_model2.predict(img_array), dupi_model5.predict(img_array), dupi_model6.predict(img_array)]
    class_names = [
        ['모낭사이홍반 : 양호', '모낭사이홍반 : 경증', '모낭사이홍반 : 중등도', '모낭사이홍반 : 중증'],
        ['비듬 : 양호', '비듬 : 경증', '비듬 : 중등도', '비듬 : 중증'],
        ['미세각질 : 양호', '미세각질 : 경증', '미세각질 : 중등도', '미세각질 : 중증'],
        ['모낭홍반농포 : 양호', '모낭홍반농포 : 경증', '모낭홍반농포 : 중등도', '모낭홍반농포 : 중증'],
        ['탈모 : 양호', '탈모 : 경증', '탈모 : 중등도', '탈모 : 중증'],
        ['피지과다 : 양호', '피지과다 : 경증', '피지과다 : 중등도', '피지과다 : 중증']
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
    result_model1 = 'Good' if results['model1']['predicted_class'] == 0 else 'Bad'
    result_model2 = 'Good' if results['model2']['predicted_class'] == 0 else 'Bad'
    result_model3 = 'Good' if results['model3']['predicted_class'] == 0 else 'Bad'
    result_model4 = 'Good' if results['model4']['predicted_class'] == 0 else 'Bad'
    result_model5 = 'Good' if results['model5']['predicted_class'] == 0 else 'Bad'
    result_model6 = 'Good' if results['model6']['predicted_class'] == 0 else 'Bad'

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

def hairlossresult_view(request):
    # 데이터베이스에서 가장 최근에 추가된 Scalp 인스턴스를 가져옵니다.
        latest_scalp = Scalp.objects.latest('scalp_dt')
    #
    #         # MEDIA_ROOT를 사용하여 전체 파일 경로를 구성합니다.
        img_path = os.path.join(settings.MEDIA_ROOT, str(latest_scalp.scalp_imgpath))

    # 이미지 분류 함수를 호출합니다.
        classification_results, final_result = classify_scalp_type(img_path)

    # 분류 결과와 최종 결과를 템플릿에 전달합니다.
        context = {
            'classification_results': classification_results,
            'final_result': final_result,
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
'''