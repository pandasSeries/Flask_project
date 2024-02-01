# url접속시 위에 만들어진 템플릿 html을 되돌려주도록 만든다
# render_template이랑 같이써서 html을 리턴
from flask import Blueprint, render_template

# blueprint를 이용하면 플라스크 App의 모든 url을 한곳에서 관리 하지 않아도 된다
# 이곳저곳에 뿌려진 url의 정의를 수집하여 한곳으로 모아준다
views = Blueprint('views', __name__)

# 뷰를 정의하여 보여질 페이지와 경로를 정의
# 클라이언트 요청 > 서버의 응답을 간단히
# 데코레이터로 Blueprint.route가 해줄 예정
# 우리는 동작하기위해 필요한 정보만 입력
@views.route('/') # url 끝부분(end point)를 인자로 입력
def home():
    return render_template('home.html') # 클라이언트 요청에 응답할 데이터를 return 시키는 함수 생성