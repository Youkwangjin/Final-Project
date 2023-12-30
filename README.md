# AI를 활용한 스타일 추천 서비스 (Team Project)
- 참여자 : 최민혁, 조혁진, 이재민, 유광진, 이서호, 김효림 (6명)
- 총 개발기간 : 2023/11/20 ~ 2023/12/26 (5주)


# 목차
- [시연 동영상](https://github.com/Youkwangjin/Final-Project)
- [프로젝트 개요](https://github.com/Youkwangjin/Final-Project)
- [프로젝트 문서](https://github.com/Youkwangjin/Final-Project)
- [데이터 분석 과정](https://github.com/Youkwangjin/Final-Project)
- [웹 개발 과정](https://github.com/Youkwangjin/Final-Project)
- [미래 개선 방안](https://github.com/Youkwangjin/Final-Project)
- [개발환경](https://github.com/Youkwangjin/Final-Project)
- [참조 사이트](https://github.com/Youkwangjin/Final-Project)

# 시연 동영상
[시연 동영상](https://github.com/Youkwangjin/Final-Project)

# 프로젝트 개요

**1. 프로젝트명 : Make Me Up**

**2. 주제 : AI를 활용한 스타일 추천 서비스**

**3. 배경**
> 적절한 뷰티 제품을 찾는 과정에서 소비자들은 상당한 시간과 비용을 투자해야 합니다. 뿐만 아니라, 다양한 브랜드와 제품들이 시장에 풍부하게 존재하면서 선택에 대한 혼란이 빈번하게 발생합니다. 이로 인해 소비자들은 제품 선택에 어려움을 겪고, 효과적인 뷰티 루틴을 구축하는 데 어려움을 겪는 현상이 나타납니다. 이 프로젝트는 이러한 소비자들의 어려움을 해소하고, 최적의 뷰티 제품을 찾을 수 있는 효율적이고 개인화된 솔루션을 제공하는 데 중점을 둡니다.

**4. 목적**
-  소비자들이 뷰티 제품을 효과적으로 찾고 선택함으로써 시간과 비용을 절약합니다.
-  개인화된 뷰티 관리를 간편하게 수행할 수 있도록 지원하는 것입니다. 이를 통해 고객들의 만족도를 높이고, 개인 맞춤형 뷰티 루틴을 손쉽게 구축할 수 있는 경험을 제공합니다.

# 프로젝트 문서

# 시스템 구성도

![image](https://github.com/Youkwangjin/Final-Project/assets/117841714/08622152-5308-4c8d-9720-c80011aa3131)


# 데이터 분석 과정

📌 **퍼스널 컬러**
1. 데이터 수집
   
- 퍼스널 컬러 논문자료를 토대로 각 유형별 4개의 색상에 대한 RGB값 수집 
    ![수집1](https://github.com/Youkwangjin/Final-Project/assets/138757075/ab0536be-616f-4134-bfbc-7a21b5c3f1de)

2. 데이터 전처리
- 수집된 RGB값에 대해 HSV, YCbCr 값을 추가해 각각의 색상값에 대해 유사한 색상 증강 : 총 1111개의 색상 데이터로 증강
  ![증강1](https://github.com/Youkwangjin/Final-Project/assets/138757075/f24bcc27-2aca-4420-83b7-fdd18a7cce5f)
- 증강된 색상값에서 흰색에 가까운 색상 및 중복 색상값 제거
   : 총 875개의 색상 데이터로 조정

3. 데이터 분석 :  모델 설계 및 학습

- 머신러닝 모델 설계
  - Ensemble(voting = soft) 모델 설계
      SVM, KNN, LDA, LR_L2, RandomForest, GradientBoost 모델 생성 및 학습 후 Ensemble모델을 통해 성능 개선
      ![소프트](https://github.com/Youkwangjin/Final-Project/assets/138757075/94ff13da-810e-4899-80c6-8f6e487df585)
  - Ensemble(voting = hard) 모델 설계
      SVM, KNN, LDA, LR_L2, RandomForest, GradientBoost 모델 생성 및 학습 후 Ensemble모델을 통해 성능 개선
    ![하드](https://github.com/Youkwangjin/Final-Project/assets/138757075/6530318c-396d-449a-8551-4ee05573e55c)
  - CatBoostClassifier 모델 설계
  - 모델 성능평가
      3가지 모델 학습 결과 soft 방식으로 voting한 Ensemble 모델이 성능이 가장 우수해 머신러닝 모델에서는 Ensemble(voting = soft) 채택
      ![각 모델 별 혼동행렬](https://github.com/Youkwangjin/Final-Project/assets/138757075/1287df48-e57d-4344-8fab-3f044815b274)


     

- 딥러닝 모델 설계

# 웹 백엔드 개발 과정

실시간 웹 캠으로 찍은 사진들을 ajax처리 방식으로 DB에 저장

![image](https://github.com/Youkwangjin/Final-Project/assets/117841714/e127f81b-f7b9-4ccb-99d2-bf0651550042)



# Docker

![image](https://github.com/Youkwangjin/Final-Project/assets/117841714/b86fe2a7-eca4-4df3-aac9-5167eb9ce895)



# 미래 개선 방안
**1. Docker 환경으로 작업한 프로젝트를 aws EC2 환경으로 배포**


# 개발환경 
📌 **Front-end**

<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white"> 

📌 **Back-end**

<img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
<img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">

📌 **DataBase**

<img src="https://img.shields.io/badge/mariadb-003545?style=for-the-badge&logo=mariadb&logoColor=white">  

📌 **Data Analysis**

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/keras-D00000?style=for-the-badge&logo=keras&logoColor=white"> <img src="https://img.shields.io/badge/tensorflow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"> <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"> <img src="https://img.shields.io/badge/matplotlib-2E5E82?style=for-the-badge&logo=MyBatis&logoColor=white">

# 참조 사이트
