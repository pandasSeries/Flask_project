from flask import Flask
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy를 인스턴스화
db = SQLAlchemy()

# create_app 함수를 작성
def create_app():
    # 플라스크 인스턴스 생성
    app = Flask(__name__)

    # 앱의 config 설정을 한다
    app.config.from_mapping(
        SECRET_KEY = '2ASEIEIEDIDISEOEW',
        SQLALCHEMY_DATABASE_URI = 
        f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        # SQL을 콘솔 로그에 출력하는 설정
        SQLALCHEMY_ECHO = True
    )

    # SQLALChemy와 앱을 연계
    db.init_app(app)
    # Migrate와 앱을 연계
    Migrate(app, db)
    # crud 패키지로부터 views를 import한다
    # 이제부터 작성하는 crud패키지로부터 views를 import한다
    from crud import views as crud_views

    # register_blueprint를 사용해 views의 crud를 앱에 등록
    # blueprint라 불리는 기능인 app.register_blueprint함수를 사용해
    # crud 앱을 등록 url_prefix에 /crud를 지정하고 이 views의 
    # 엔드포인트의 모든 url이 crud로부터 시작되게 합니다
    app.register_blueprint(crud_views.crud, url_prefix='/crud')


