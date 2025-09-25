import secrets
from pathlib import Path

basedir = Path(__file__).parent.parent # 상위 디렉터리 파일을 잡기 위한 경로 (parent는 ../이거로 보면 됨)

# 전체 환경 공통 설정들...
class BaseConfig:
  SECRET_KEY = secrets.token_urlsafe(32)
  WTF_CSRF_SECRET_KEY = secrets.token_urlsafe(32)
  UPLOAD_FOLDER = str( Path(basedir, "apps","images") )
  LABELS = [
        "unlabeled",
        "person",
        "bicycle",
        "car",
        "motorcycle",
        "airplane",
        "bus",
        "train",
        "truck",
        "boat",
        "traffic light",
        "fire hydrant",
        "street sign",
        "stop sign",
        "parking meter",
        "bench",
        "bird",
        "cat",
        "dog",
        "horse",
        "sheep",
        "cow",
        "elephant",
        "bear",
        "zebra",
        "giraffe",
        "hat",
        "backpack",
        "umbrella",
        "shoe",
        "eye glasses",
        "handbag",
        "tie",
        "suitcase",
        "frisbee",
        "skis",
        "snowboard",
        "sports ball",
        "kite",
        "baseball bat",
        "baseball glove",
        "skateboard",
        "surfboard",
        "tennis racket",
        "bottle",
        "plate",
        "wine glass",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "couch",
        "potted plant",
        "bed",
        "mirror",
        "dining table",
        "window",
        "desk",
        "toilet",
        "door",
        "tv",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "blender",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy bear",
        "hair drier",
        "toothbrush",
    ]

# 로컬환경에서 적용할 환경설정들..
class LocalConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:1234@localhost:3306/flaskdb'
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO=True

# 배포환경에서 적용할 환경설정들..
class DeployConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI='배포 후 사용할 DB주소'
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO=False

config = {
  "local" : LocalConfig,
  "deploy" : DeployConfig
}