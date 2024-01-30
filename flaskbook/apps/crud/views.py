from flask import Blueprint, render_template

# db를 import 한다
from apps.app import db
# user 클래스를 import한다
from apps.crud.models import User

# Blueprint로 crud앱을 생성
# template_folder와 static_folder를 지정하면 crud 디렉터리내의 templates
# 와 static을 이용가능
crud = Blueprint(
    'crud',
    __name__,
    template_folder = 'templates',
    static_folder='static'
)

# index 엔드포인트를 작성하고 index.html을 반환
# Blueprint를 사용하는 경우는 Blueprint 클래스에서 생성한 앱 crud를 이용
@crud.route('/')
def index():
    return render_template('crud/index.html')

@crud.route('/sql')
def sql():
    db.session.query(User).all()
    return '콘솔 로그를 확인해 주세요'