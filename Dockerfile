FROM python:3.11.5

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1



WORKDIR /app/

# 먼저 requirements.txt만 복사
COPY requirements.txt /app/

# 의존성 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 나머지 소스 코드 복사
COPY . /app/

COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Collect static files
# RUN python manage.py collectstatic

# 모델 경로 복사
COPY mainapp/models/shape_vgg16_process1.h5 /app/mainapp/models/shape_vgg16_process1.h5
COPY mainapp/models/ensemble_soft_model_poly.h5 /app/mainapp/models/ensemble_soft_model_poly.h5
COPY mainapp/models/scalp_model1.hdf5 /app/mainapp/models/scalp_model1.hdf5
COPY mainapp/models/scalp_model2.hdf5 /app/mainapp/models/scalp_model2.hdf5
COPY mainapp/models/scalp_model3.hdf5 /app/mainapp/models/scalp_model3.hdf5
COPY mainapp/models/scalp_model4.hdf5 /app/mainapp/models/scalp_model4.hdf5
COPY mainapp/models/scalp_model5.hdf5 /app/mainapp/models/scalp_model5.hdf5
COPY mainapp/models/scalp_model6.hdf5 /app/mainapp/models/scalp_model6.hdf5

EXPOSE 8000



CMD ["gunicorn", "makemeuppro.wsgi:application", "--bind", "0.0.0.0:8000"]
