from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index() : 
  return "hello flask world"

@app.route('/hello/<name>')
def hello(name):
  return render_template('index.html', name=name)

@app.route('/contact')
def contact():
  return render_template('contact.html')

# 이 두개를 합칠거임
'''
작업 하는 거에 따라서 이렇게 분리해도 되고 밑에 처럼 합쳐도 됨

@app.route('/contact_complete')
def contact_complete():
  return render_template('contact_complete.html')

@app.route('/contact_complete', methods=['POST'])
def contact_send():
  # 전송 기능 구현 예정
  print('문의 전송 기능 실행~~~')
  return redirect( url_for('contact_complete') )

'''
@app.route('/contact/complete', methods=['GET', 'POST'])
def contact_complete():
  if request.method == 'POST':
    # 문의 전송 기능 구현

    # 문의 완료 시 리다이렉트
    return redirect(url_for('contact_complete'))
  
  # GET 요청 시 페이지 렌더링
  return render_template('contact_complete.html')