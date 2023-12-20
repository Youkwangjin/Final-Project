from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import json
import base64
from django.http import JsonResponse
from .models import Personal, Faceshape, Scalp, Facerecorn, Scalprecorn, Personalrecorn, Personaldesc
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
import os
from PIL import Image
import numpy as np
import joblib
import colorsys
import dlib
from sklearn.preprocessing import PolynomialFeatures
from django.conf import settings
from django.shortcuts import render

# 서호 모델
fmodel_path = os.path.join(settings.BASE_DIR, '../Final-Project/mainapp/models', 'shape_vgg16_process1.h5')
fmodel = load_model(fmodel_path)

# 민혁 모델
pmodel_path = os.path.join(settings.BASE_DIR, '../Final-Project/mainapp/models', 'ensemble_soft_model_poly.h5')
pmodel = joblib.load(pmodel_path)

# 혁진 모델
dupi_model1 = load_model(os.path.join(settings.BASE_DIR, '../Final-Project/mainapp/models/', 'scalp_model1.hdf5'))
dupi_model2 = load_model(os.path.join(settings.BASE_DIR, '../Final-Project/mainapp/models/', 'scalp_model2.hdf5'))
dupi_model3 = load_model(os.path.join(settings.BASE_DIR, '../Final-Project/mainapp/models/', 'scalp_model3.hdf5'))
dupi_model4 = load_model(os.path.join(settings.BASE_DIR, '../Final-Project/mainapp/models/', 'scalp_model4.hdf5'))
dupi_model5 = load_model(os.path.join(settings.BASE_DIR, '../Final-Project/mainapp/models/', 'scalp_model5.hdf5'))
dupi_model6 = load_model(os.path.join(settings.BASE_DIR, '../Final-Project/mainapp/models/', 'scalp_model6.hdf5'))


# # 로컬 환경에서 실행 시킬 때
# FMODEL_PATH = 'C:/work/Final-Project/mainapp/models/shape_vgg16_process1.h5'
# PMODEL_PATH = 'C:/work/pysou/makemeuppro/mainapp/models/ensemble_soft_model_poly.h5'
# DMODEL_PATH1 = 'C:/work/pysou/makemeuppro/mainapp/models/aram_model1.hdf5'
# DMODEL_PATH2 = 'C:/work/pysou/makemeuppro/mainapp/models/aram_model2.hdf5'
# DMODEL_PATH3 = 'C:/work/pysou/makemeuppro/mainapp/models/aram_model3.hdf5'
# DMODEL_PATH4 = 'C:/work/pysou/makemeuppro/mainapp/models/aram_model4.hdf5'
# DMODEL_PATH5 = 'C:/work/pysou/makemeuppro/mainapp/models/aram_model5.hdf5'
# DMODEL_PATH6 = 'C:/work/pysou/makemeuppro/mainapp/models/aram_model6.hdf5'
#
# # 서호 모델
# fmodel = load_model(settings.FMODEL_PATH)
#
# # 민혁 모델
# pmodel = joblib.load(settings.PMODEL_PATH)
#
# # 혁진 모델
# dupi_model1 = load_model(settings.DMODEL_PATH1)
# dupi_model2 = load_model(settings.DMODEL_PATH2)
# dupi_model3 = load_model(settings.DMODEL_PATH3)
# dupi_model4 = load_model(settings.DMODEL_PATH4)
# dupi_model5 = load_model(settings.DMODEL_PATH5)
# dupi_model6 = load_model(settings.DMODEL_PATH6)
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

        # Personal 모델 인스턴스 생성
        new_personal = Personal(
            personal_imgpath=image_file,  # 이미지 파일
            personal_dt=timezone.now(),  # 등록일자, 현재 시간으로 설정
        )
        new_personal.save()

        # 이미지 분석 및 DB 업데이트
        classifier_personal_color = classify_personal_color(new_personal.personal_imgpath)
        personal_color_string = get_personal_color_string(classifier_personal_color)
        new_personal.personal_result = personal_color_string
        new_personal.save()

        return JsonResponse({'status': 'success', 'personal_id': new_personal.personal_id})
    return JsonResponse({'status': 'fail'})


# 이미지 로드 및 전처리
def classify_personal_color(img_path):
    image = Image.open(img_path).convert('RGB')  # 이미지 로드 및 크기 조정
    image_array = np.array(image)

    # dlib 얼굴 검출기 초기화
    detector = dlib.get_frontal_face_detector()

    # 얼굴 위치 인식
    face_locations = detector(image_array, 2)
    # 얼굴 영역 추출
    if len(face_locations) > 0:
        # 첫 번째 얼굴만 처리
        top, right, bottom, left = (face_locations[0].top(), face_locations[0].right(),
                                    face_locations[0].bottom(), face_locations[0].left())

        # 얼굴 영역을 크롭
        face_image = Image.fromarray(image_array[top:bottom, left:right])
        # print(face_image)
        # 이미지 크기 조정 (모델에 맞게)
        resized_face_image = face_image.resize((100, 100))
        # print(resized_face_image)

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

        # print(input_data)

        # 모델 예측
        classifier_personal_color = pmodel.predict(input_data)
        return classifier_personal_color  # 최종 반환값
    else:
        print("이미지에서 얼굴을 찾을 수 없습니다.")


def get_personal_color_string(classifier_personal_color):
    personal_color_string = ''
    if classifier_personal_color[0] == 0:
        personal_color_string = '봄웜'
    elif classifier_personal_color[0] == 1:
        personal_color_string = '여름쿨'
    elif classifier_personal_color[0] == 2:
        personal_color_string = '가을웜'
    elif classifier_personal_color[0] == 3:
        personal_color_string = '겨울쿨'
    # 최종 반환 값
    return personal_color_string


# 결과 출력
def personalcolorresult_view(request):
    try:
        # 데이터베이스에서 가장 최근에 추가된 Personal 인스턴스를 가져옵니다.
        latest_personal = Personal.objects.latest('personal_dt')

        # Personal 모델에서 personal_color 값을 가져옵니다.
        personal_color = latest_personal.personal_result

        # Personalrecorn 모델에서 상품 추천 목록을 가져옵니다.
        product_recommendations = Personalrecorn.objects.filter(personal_result=personal_color)

        # Personaldesc 모델에서 매핑
        personaldesc_data_list = Personaldesc.objects.filter(personal_result=personal_color)

        # 템플릿에 결과 데이터 전달
        context = {
            'captured_photo_url': latest_personal.personal_imgpath.url,
            'personal_color': personal_color,
            'product_recommendations': product_recommendations,
            'personaldesc_data_list': personaldesc_data_list,  # 모든 Personaldesc 레코드를 전달합니다.
        }

        return render(request, 'personalcolorresult.html', context)
    except Personal.DoesNotExist:
        # Personal 인스턴스가 없는 경우 오류 메시지와 함께 응답합니다.
        return JsonResponse({'status': 'fail', 'message': 'No personal record found.'})
    except Exception as e:
        # 기타 예외 처리
        return JsonResponse({'status': 'fail', 'message': str(e)})


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

        return JsonResponse(
            {'status': 'success', 'faceshape_id': new_faceshape.faceshape_id, 'faceshape_result': predicted_class})
    return JsonResponse({'status': 'fail'})


# 이미지 로드 및 전처리(얼굴형)
'''
def classify_face_shape(img_path):
    img = load_img(img_path, target_size=(224, 224))  # 이미지 로드 및 크기 조정
    img_array = img_to_array(img)  # 이미지를 배열로 변환
    img_array = np.expand_dims(img_array, axis=0)  # 행 방향으로 차원 확대
    # 이미지를 분류하고 결과를 반환합니다.
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
'''


# 얼굴 형태 분류 함수 (위에서 제공된 함수)
def classify_face_shape(img_path):
    detector = dlib.get_frontal_face_detector()

    # load_img를 이용해 이미지를 PIL 형식으로 로드합니다.
    img = load_img(img_path)
    img = img.resize((224, 224))  # 이미지 크기 조정

    # PIL 이미지를 NumPy 배열로 변환
    img_array = img_to_array(img)

    # NumPy 배열을 uint8 타입으로 변환 (dlib 처리를 위해)
    img_array = img_array.astype('uint8')

    # 얼굴 감지
    faces = detector(img_array, 1)  # 두 번째 인자로 이미지의 업샘플링 횟수 지정
    if len(faces) == 0:
        print("얼굴을 감지하지 못했습니다.")
        return None, None

    # 첫 번째 감지된 얼굴을 사용합니다 (여러 얼굴이 있는 경우)
    face = faces[0]

    # 얼굴 영역을 기반으로 이미지를 crop합니다.
    cropped_img = img_array[face.top():face.bottom(), face.left():face.right()]

    # PIL 이미지로 변환
    pil_image = Image.fromarray(cropped_img)
    pil_image = pil_image.resize((224, 224))

    # 이미지를 배열로 변환 및 차원 확대
    img_array = img_to_array(pil_image)
    # img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # 이미지 분류 및 결과 반환
    predictions = fmodel.predict(img_array)

    predictions_percent = [int(value * 100) for value in predictions[0]]
    print('predictions_percent : ', predictions_percent)
    predicted_index = np.argmax(predictions, axis=1)
    print('predicted_index : ', predicted_index)

    class_names = ['하트형', '직사각형', '계란형', '둥근형', '사각형']
    predicted_class = class_names[predicted_index[0]]

    return predicted_class, predictions_percent


"""
# -----
import matplotlib.pyplot as plt
# 이미지 경로 설정
# img_path = 'C:/Users/SEOHO/Desktop/egg.jpg'
img_path = 'C:/Users/SEOHO/Desktop/취업/이력서사진.jpg'
img = Image.open(img_path)

# 이미지 표시
plt.imshow(img)
plt.axis('off')  # 축 정보 끄기
plt.show()
# 함수 실행
predicted_class, predictions_percent = classify_face_shape(img_path)

# 결과 출력
print("Predicted Class:", predicted_class)
print("Prediction Percentages:", predictions_percent)
# ---
"""


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

            # 이미지 파일 처리 및 Scalp 모델 인스턴스 생성
            ext = photo.name.split('.')[-1]
            new_scalp = Scalp(
                scalp_imgpath=photo,
                scalp_dt=timezone.now(),
            )

            # 이미지 저장
            new_scalp.save()

            # 이미지 경로를 classify_scalp_type 함수에 전달하여 두피 유형 분류
            _, final_result = classify_scalp_type(new_scalp.scalp_imgpath.path)

            # final_result를 Scalp 인스턴스의 scalp_result 필드에 저장
            new_scalp.scalp_result = final_result
            new_scalp.save()

            return JsonResponse({'status': 'success', 'scalp_id': new_scalp.scalp_id, 'scalp_result': final_result})
    return JsonResponse({'status': 'fail'})


# 이미지 분류 함수 정의 (데이터 분류 및 결과를 출력하는 함수)
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
    result_model1 = 'Good' if results['model1']['predicted_class'] == 0 or results['model1'][
        'predicted_class'] == 1 else 'Bad'
    result_model2 = 'Good' if results['model2']['predicted_class'] == 0 or results['model2'][
        'predicted_class'] == 1 else 'Bad'
    result_model3 = 'Good' if results['model3']['predicted_class'] == 0 or results['model3'][
        'predicted_class'] == 1 else 'Bad'
    result_model4 = 'Good' if results['model4']['predicted_class'] == 0 or results['model4'][
        'predicted_class'] == 1 else 'Bad'
    result_model5 = 'Good' if results['model5']['predicted_class'] == 0 or results['model5'][
        'predicted_class'] == 1 else 'Bad'
    result_model6 = 'Good' if results['model6']['predicted_class'] == 0 or results['model6'][
        'predicted_class'] == 1 else 'Bad'

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


def hairlossresult_view(request):
    # 데이터베이스에서 가장 최근에 추가된 Scalp 인스턴스를 가져옵니다.
    latest_scalp = Scalp.objects.latest('scalp_dt')

    # MEDIA_ROOT를 사용하여 전체 파일 경로를 구성합니다.
    img_path = os.path.join(settings.MEDIA_ROOT, str(latest_scalp.scalp_imgpath))

    # 이미지 분류 함수를 호출합니다.
    classification_results, final_result = classify_scalp_type(img_path)

    # 공백을 제거
    final_result = final_result.strip()

    # 데이터베이스에서 분류 결과에 해당하는 추천 제품들을 조회
    recommended_products = Scalprecorn.objects.filter(scalp_result=final_result)

    # scalprecorn_content에서 특수 문자를 제거
    for item in recommended_products:
        item.scalprecorn_content = item.scalprecorn_content.strip('\ufeff')

    # 분류 결과, 최종 결과, 추천 제품들을 템플릿에 전달
    context = {
        'classification_results': classification_results,
        'final_result': final_result,
        'recommended_products': recommended_products,
    }
    return render(request, 'hairlossresult.html', context)
