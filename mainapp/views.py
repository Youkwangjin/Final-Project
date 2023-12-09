from django.shortcuts import render
# Create your views here.
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

