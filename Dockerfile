FROM python:3.11.5

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /makemeuppro

# 먼저 requirements.txt만 복사
COPY requirements.txt /makemeuppro/

# 의존성 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 나머지 소스 코드 복사
COPY . /makemeuppro

# 모델 경로 복사
COPY mainapp/models/personalcolor_ensemble1.h5 /app/models/personalcolor_ensemble1.h5
EXPOSE 8000

CMD ["gunicorn", "makemeuppro.wsgi:application", "--bind", "0.0.0.0:8000"]
