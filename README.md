# clone 후 해야할 것
## .env파일 생성하기
```
FLASK_APP=apps.app.py
FLASK_DEBUG=True
FLASK_CONFIG_KEY=local
```
## 가상환경 만들고 활성화 하기
```
py -3.11 -m venv venv  # 가상환경 생성
.\venv\Scripts\activate # 가상환경 활성화
```
## 라이브러리 설치하기
```
pip install -r requirements.txt
```
## DB 설정
MySQL에 데이터베이스(flaskdb) 생성

```
flask db init
flask db migrate
flask db upgrade
```

## flask 서버 실행
```
flask run
```

# 작업 후 커밋하기 전에 할 것
만약 라이브러리 추가 설치를 했을 경우
```
pip freeze > requirements.txt
```