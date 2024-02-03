# 하나의 패키지 인식
# __name__은 현재 __name__이 작성된 파일명을 문자열로 저장하고 있거나
# __main__이란 문자열 값을 저장

# 다른 곳에서 생성된 Blueprint를 __init__.py에 등록
# Flask App에 관리되는 Blueprint가 있다는것을 알리기 위함
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
db = SQLAlchemy()
DB_NAME = 'database.db'
def create_app():
    app = Flask(__name__)
    # app.config는 생성될 App의 비밀 키 값
    # 일종의 암호화 또는 쿠키및 세션 데이터 보호를 할때 사용되는 값
    # 실제로 배포할때는 누구에게도 알려줘서 안된다
    app.config['SECRET_KEY'] = 'semicircle_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    # 블루프린트 인스턴스 가져오기
    from .views import views
    from .auth import auth

    # 플라스크 앱에 등록하기
    # url_prefix - url접두사 해당 블루프린트를 이용할때 기본적으로 붙을 url을 적는다
    # 현재는 딱히 구분할 필요가 없기에 모두 / 문자열로 입력
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # DB에 사용할 모델 불러오기
    from .models import User, Note 
    with app.app_context():
        db.create_all()

    return app

# 데이터 베이스 생성 함수
# def create_database(app):
#     # db파일이 확인 안될때만 생성
#     if not path.exists('diary/' + DB_NAME):
#         db.create_all(app = app)
#         print('>>> Create DB')