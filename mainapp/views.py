from django.core.files.base import ContentFile
from django.shortcuts import render
import json
import base64
from django.http import JsonResponse
from .models import Personal, Faceshape, Scalp
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

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

def styleresult_view(request):
    # Your view logic goes here
    return render(request, 'styleresult.html')

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

@csrf_exempt
def upload_scalp_image(request):
    if request.method == 'POST':
        # JSON 데이터 로딩
        data = json.loads(request.body)
        image_data = data['image_data']
        format, imgstr = image_data.split(';base64,')  # 이미지 포맷과 데이터 분리
        ext = format.split('/')[-1]  # 파일 확장자 추출

        # 이미지 데이터를 ContentFile로 변환
        image_file = ContentFile(base64.b64decode(imgstr), name='faceshape.' + ext)

        # Faceshape 모델 인스턴스 생성 및 저장
        new_scalp = Scalp(
            scalp_result=data.get('scalp_result', ''),  # 결과, 없다면 빈 문자열
            scalp_imgpath=image_file,  # 이미지 파일
            scalp_dt=timezone.now(),  # 등록일자, 현재 시간으로 설정
            # 기타 필요한 필드들을 추가
        )
        new_scalp.save()

        return JsonResponse({'status': 'success', 'faceshape_id': new_scalp.scalp_id})
    return JsonResponse({'status': 'fail'})

