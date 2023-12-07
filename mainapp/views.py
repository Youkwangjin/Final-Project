from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'index.html')

def camera_view(request):
    # Your view logic goes here
    return render(request, 'camera_view.html')