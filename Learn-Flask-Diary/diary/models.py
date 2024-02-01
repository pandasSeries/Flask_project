# db 모델 구조 
# 유저와 메모장에 대한 데이터 정의

# user 
#   id : 기본키, email, password, nickname
# note
#   id : 메모 데이터를 구분하기위한 값 기본키, title, content, datetime
from . import db
# flask-login은 Flask에 대한 사용자 세션관리 제공
# 로그인, 로그아웃 및 장기간에 걸친 사용자 세션 기억과 같은 일반적인 작업 처리
# 세션에 활성 사용자의 id를 저장하고 쉽게 로그인 및 로그아웃
# 로그인한 사용자의 보기 제한
# 일반적으로 까다로운 기억 기능 처리
# 쿠키 도둑이 사용자의 세션을 도난하지 않도록 보호
# 나중에 Flask-Principal 또는 기타 인증 확장과 통합할수있다
from flask_login import UserMixin


# 하나의 유저에 여러개의 메모 존재 1:다 relationship
# define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200))
    notes = db.relationship('Note')
# define Note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(2000))
    # 작성된 시간 또는 수정된 시간
    # default로 작성된 시간 기록
    # onupdate는 해당 정보가 수정될때마다 업데이트되도록 하는 인수
    # 모든 데이터는 db기준으로 기록되어야함
    datetime = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    