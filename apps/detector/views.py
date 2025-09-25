from flask import Blueprint, render_template, current_app, send_from_directory, redirect, url_for,flash
from flask_login import login_required, current_user # 로그인 유저 아니면 못 들어오게 방지
from pathlib import Path
import uuid # 파일명이 겹치면 덮어쓰기 됨
import cv2
import torch
import torchvision
from PIL import Image
import numpy as np

from apps.detector.forms import UploadImageForm
from apps.app import db
from apps.detector.models import UserImage, UserImageTag
from apps.crud.models import User 

dt = Blueprint(
  "detector",
  __name__,
  template_folder="templates"
)

@dt.route('/')
def index():

  user_images = db.session.query(User, UserImage).join(UserImage) \
                                .filter(User.id == UserImage.user_id).all()
  

  return render_template("detector/index.html", user_images=user_images)

@dt.route('/images/<filename>')
def image_file(filename):
  return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename) # (경로,파일명)

@dt.route('/upload', methods=['GET','POST'])
@login_required # 로그인 안 하면 못 오게 방지
def upload_image():

  form = UploadImageForm()

  if form.validate_on_submit(): # 검사
    file = form.image.data

    # 중복 된 이미지 파일명 방지를 위해 이름을 uuid로 교체
    ext = Path(file.filename).suffix # 확장자만 뽑는 작업 -> file.filename은 xxx.jpg/ exp는 .jpg가 뽑힘
    image_uuid_file_name = str( uuid.uuid4()) + ext # 문자열로 형변환 필요

    # apps/images/uuid.jpg -> 경로
    image_path = Path(current_app.config["UPLOAD_FOLDER"], image_uuid_file_name)
    file.save(image_path)

    # 위 정보를 DB에 저장
    user_image = UserImage(user_id=current_user.id, image_path=image_uuid_file_name)

    db.session.add(user_image) # DB에 insert
    db.session.commit() 
    
    return redirect(url_for('detector.index'))

  return render_template('detector/upload.html', form=form)



# 물체 감지 처리에 필요한 함수들

import random

# 선 색 지정하는 함수
# ai가 객체 탐지를 완료하면 탐지 된 물체 목록들을 labels로 보냄
# 매개 변수 개수만큼 색상 종류들을 뽑아내고 그 색상들 중 하나를 선택해서 리턴 시켜주는 함수
def make_color(labels):
  colors = [ [random.randint(0, 255) for _ in range(3)] for _ in labels   ]
  color = random.choice(colors)

  return color

# 이미지 크기에 따라 선 두께를 리턴 해주는 함수
# 이미지의 너비와 높이 중 큰 값을 기준으로 선 두께를 정함(shape)
def make_line(result_image):
  line = round(max(result_image.shape[0:2]) * 0.002 ) +1
  return line

# 이미지에 박스 그려주는 함수
# c1, c2 : 박스를 그릴 좌표 (왼쪽 위, 오른쪽 아래)
def draw_lines(c1, c2, result_image, line, color):
  cv2.rectangle(result_image, c1, c2, color, thickness=line)
  return cv2

# 이미지에 라벨 넣는 함수
def draw_texts( result_image, line, c1, c2, color, labels, label ):
  display_text = labels[label]
  font = max(line -1, 1) # line -1이 0이면 안 되니까 최소값을 1로 지정 (선 두께)
  t_size = cv2.getTextSize(display_text, 0, fontScale=line/3, thickness=font)[0] # 0은 글꼴 종류(기본 폰트)
  c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3 
  cv2.rectangle(result_image, c1, c2, color, -1) # -1을 하면 채워짐
  cv2.putText(
    result_image,
    display_text,
    ( c1[0], c1[1] -2 ),
    0,
    line / 3,
    [255,255,255],
    thickness=font,
    lineType=cv2.LINE_AA # 안티엘리어싱? 과한 깨진 걸 부드럽게 처리해주는 역활
  )

# 이미지를 가져와서 물체 탐지를 시키고, 라벨이 추가 된 이미지를 생성
# 생성 된 이미지와 라벨들을 리턴 
def exec_detect(target_image_path):
  labels = current_app.config['LABELS']

  # 이미지 가져오기
  image = Image.open(target_image_path)

  # 가져 온 이미지를 모델이 읽을 수 있는 자료형(텐서)으로 변환 /텐서는 숫자 형태인 배열
  image_tensor = torchvision.transforms.functional.to_tensor(image)

  # 모델(ai) 불러오기
  model = torch.load(Path(current_app.root_path, "detector","model.pt"), weights_only=False)

  model = model.eval() # 학습에 불 필요한 모든 것들은 비활성화 처리

  # 예측
  output = model( [image_tensor] )[0]

  # 감지 된 물테들 목록을 저장 할 리스트
  tags = []
  result_image = np.array( image.copy() ) 

  for box, label, score in zip( output['boxes'], output['labels'], output['scores'] ):

    if score > 0.5 and labels[label] not in tags:
      color = make_color(labels)
      line = make_line(result_image)

      c1 = ( int(box[0]), int(box[1]) )
      c2 = ( int(box[2]), int(box[3]) )

      cv2 = draw_lines( c1, c2, result_image, line, color )
      draw_texts( result_image, line, c1, c2, color, labels, label )

      tags.append(labels[label])

  if tags:
    detected_image_file_name = str(uuid.uuid4()) + '.jpg'
    detected_image_file_path = str(
      Path(current_app.config["UPLOAD_FOLDER"], detected_image_file_name)
    )
    cv2.imwrite( detected_image_file_path, cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR) )
  
    return tags, detected_image_file_name
  
  else:
    return tags, None
  
@dt.route('/detect/<image_id>', methods=['POST'])
@login_required
def detect(image_id):

  user_image = db.session.query(UserImage).filter(UserImage.id == image_id).first()

  if user_image is None:
    flash("감지 할 이미지가 없음")
    return redirect( url_for('detector.index') )
  
  target_image_path = Path(current_app.config["UPLOAD_FOLDER"], user_image.image_path)
  tags, detected_file_name = exec_detect(target_image_path)

  if not tags:
    flash("감지 된 결과가 없음")
    return redirect( url_for('detector.index') )

  user_image.is_detected = True # 감지 된 데이터
  user_image.image_path = detected_file_name # 이미지를 감지 된 이미지로 변경
  db.session.add(user_image)

  # 감지 된 라벨들을 DB에 넣는 반복문
  for tag in tags:
    user_image_tag = UserImageTag(user_image_id=user_image.id, tag_name=tag)
    db.session.add(user_image_tag)

  db.session.commit()
  
  return redirect( url_for('detector.index') ) 


















@dt.route('/test')
def test():
  image_path = Path(current_app.config["UPLOAD_FOLDER"], '0d15572c-9903-42c5-a3f7-eaff40cf6974.jpg')

  result, image = exec_detect(image_path)

  print("="*20)
  print(result)
  print(result["boxes"][0])
  print(result["labels"][0])
  print(result["scores"][0])

  copy_image = np.array(image.copy())

  box = result["boxes"][0]

  draw_lines( (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), copy_image, 1, [255,0,0] )
  cv2.imshow("aa",copy_image)
  cv2.waitKey(0)

  return ""