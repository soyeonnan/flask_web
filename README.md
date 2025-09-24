# clone 후 해야할 것
## .env파일 생성하기
```
FLASK_APP=app.py가 있는 경로잡아주기
FLASK_DEBUG=True
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