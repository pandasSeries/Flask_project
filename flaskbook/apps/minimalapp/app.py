# 이메일 주소 형식 체크용 validate_email과 EmailNotValidError를 import
from email_validator import validate_email, EmailNotValidError
from flask import Flask, render_template, url_for, current_app, g, request, redirect, flash
import logging
from flask_debugtoolbar import DebugToolbarExtension
import os
from flask_mail import Mail, Message


# flask 클래스를 인스턴스화한다
# 앱에 경로를 인식해야 .env가 밖에서 인식
# template_folder를 인식못하면 app객체안에서 지정한다
app = Flask(r'C:\Users\mark8\OneDrive\바탕 화면\flask_project\flaskbook\apps\minimalapp\app.py',
            template_folder = r'C:\Users\mark8\OneDrive\바탕 화면\flask_project\flaskbook\apps\minimalapp\templates')
# 세션을 사용하려면 세션 정보 보안을위해 secre_key값 설정
app.config['SECRET_KEY'] = '2AZSMss3p5QPbcY2hBsJ'
# 로그 레벨 지정하기
app.logger.setLevel(logging.DEBUG)
# 로그 출력
app.logger.critical('fatal error')
app.logger.error('error')
app.logger.warning('warning')
app.logger.info('info')
app.logger.debug('debug')

# 리다이렉트를 중단하지않도록 한다
# 리다이렉트를 중단하지 않도록 하는 config설정
# 리다이렉트를 하면 요청한값을 flask-debugtoolbar에서 확인 할수 없게되므로
# 디폴트는 True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# DebugToolbarExtension에 애플리케이션을 설정
# 개발자에게 편리한 기능 
toolbar = DebugToolbarExtension(app)

# Mail클래스의 config를 추가
# Mail클래스의 config를 환경변수로부터 얻는다
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# flask-mail 확장을 등록
# flask-mail확장을 앱에 등록
mail = Mail(app)

# url과 실행할 함수를 매핑
@app.route('/')
def index():
    return 'Hello, Flaskbook! nice to meet ya'
# 엔드포인트를 지정하지 않으면 함수명이 엔드포인트
#@app.get('/hello') = @app.route('/hello', methods=['GET'])

# rule에 변수 지정
@app.route('/hello/<name>', # 컨버터 <name : string>
methods = ['GET', 'POST'],
endpoint = 'hello-endpoint')
def hello(name):
    return ('hello {}!'.format(name))

# show_name 엔드포인트 작성
@app.route('/name/<name>')
def show_name(name):
    # 변수를 템플릿 엔진에 건넨다
    return render_template('index.html', name=name)

# 문의 폼의 엔드포인트 만들기
# 문의 폼 화면을 표시하는 엔드포인트
# 이메일을 보내 문의 완료 화면을 표시하는 엔드포인트

@app.route('/contact')
# 문의 폼 화면을 반환하는 contact 엔드포인트를 만든다
def contact():
    # 데이터를 받고 html에 데이터를 그린다
    return render_template('contact.html')
   
# 문의 폼 처리, 문의 완료 화면을 반환하는 contact_complete 엔드포인트를 만든다
# methods = ['GET', 'POST']를 지정하여 GET, POST메서드를 허가
@app.route('/contact/complete', methods=['GET', 'POST'])
def contact_complete():
    # request.method 속성을 이용하여 요청된 메서드 확인
    if request.method == 'POST':

        # 폼의 값 얻기
        username = request.form['username']
        email = request.form['email']
        description = request.form['description']

        # 입력 체크
        is_valid = True

        # 사용자명, 이메일 주소, 문의 내용 입력란이 비어있으면 flash에 오류메시지 설정
        # flash 메시지는 여러개 설정할수있으나 브라우저 또는 웹서버의 쿠키 크기의 제한을 초과하는 경우는 flash 메시지 이용불가

        if not username:
            flash('사용자명은 필수입니다')
            is_valid = False

        if not email:
            flash('메일 주소는 필수입니다')
            is_valid = False

        try:
            # 이메일 주소의 형식인지 여부를 validate_email함수로 확인
            # 형식이 정확하지 않는 경우는 예외가 발생하므로 try-except로 감싼다
            validate_email(email)
        except EmailNotValidError:
            flash('메일 주소의 형식으로 입력하세요')
            is_valid = False
        if not description:
            flash('문의 내용은 필수입니다')
            is_valid = False
        if not is_valid:
            return redirect(url_for('contact'))
        # 이메일을 보낸다(나중에 구현할 부분)
        # 이메일을 보내는 처리로서 이메일 송신함수를 호출하는 처리 추가
        # send_email 함수 호출
        send_email(
            email,
            '문의 감사합니다',
            'contact_mail',
            username=username,
            description=description
        )
        # contact 엔드포인트로 리다이렉트한다 ?
        # POST값에 문제가 없는 경우는 Flash 메시지에 '문의해 주셔서 감사합니다'를 설정
        # 문의완료 화면으로 리다이렉트한다
        flash('문의해 주셔서 감사합니다.')
        return redirect(url_for('contact_complete'))

    return render_template('contact_complete.html')
# 이메일을 보내는 함수
# 이메일은 텍스트 이메일과 HTML이메일 양쪽을 작성하여 송신
# HTML이메일을 수신할수 없는 경우 텍스트 이메일 송신
def send_email(to, subject, template, **kwargs):
    # 메일을 송신하는 함수
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
#with app.test_request_context('/users?updated=true'):
#     # /
#   print(url_for('index'))
#  print(request.args.get('updated'))
#     # /hello/world
#     print(url_for('hello-endpoint', name = 'world'))
#     # /name/AK?page=1
#     print(url_for('show_name', name='AK', page = '1'))
