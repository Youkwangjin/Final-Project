from django.db import models

# Create your models here.

class Facerecorn(models.Model):
    facerecorn_id = models.AutoField(primary_key=True)
    faceshape_result = models.CharField(max_length=20)
    hair_imgpath = models.ImageField(upload_to='hairstyle/')
    hair_name = models.CharField(max_length=20)
    hair_content = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'facerecorn'


class Faceshape(models.Model):
    faceshape_id = models.AutoField(primary_key=True)  # 자동으로 증가하는 ID
    faceshape_result = models.CharField(max_length=20)
    faceshape_imgpath = models.ImageField(upload_to='faceshapes/')  # 이미지 파일 저장
    faceshape_dt = models.DateTimeField(auto_now_add=True)  # 자동으로 현재 시간 저장

    class Meta:
        managed = False
        db_table = 'faceshape'


class Personal(models.Model):
    personal_id = models.AutoField(primary_key=True)  # AutoField를 사용하여 자동 ID 할당
    personal_result = models.CharField(max_length=20, blank=True, null=True)
    personal_imgpath = models.ImageField(upload_to='personal/')  # ImageField로 변경
    personal_dt = models.DateTimeField(auto_now_add=True)  # 레코드 생성 시 현재 시간 자동 저장

    class Meta:
        managed = False
        db_table = 'personal'


class Personalrecorn(models.Model):
    personalrecorn_id = models.AutoField(primary_key=True)
    personal_result = models.CharField(max_length=20, blank=True, null=True)
    cosmetics = models.CharField(max_length=10)
    dyecolor = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'personalrecorn'


class Scalp(models.Model):
    scalp_id = models.AutoField(primary_key=True)  # AutoField를 사용하여 자동 ID 할당
    scalp_result = models.CharField(max_length=20)
    scalp_imgpath = models.ImageField(upload_to='scalp/')  # ImageField로 변경
    scalp_dt = models.DateTimeField(auto_now_add=True)  # 레코드 생성 시 현재 시간 자동 저장

    class Meta:
        managed = False
        db_table = 'scalp'


class Scalprecorn(models.Model):
    scalprecorn_id = models.AutoField(primary_key=True)
    scalp_result = models.CharField(max_length=20)
    scalprecorn_imgpath = models.CharField(max_length=255)
    scalprecorn_name = models.CharField(max_length=20)
    scalprecorn_content = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'scalprecorn'