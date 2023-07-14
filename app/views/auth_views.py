
from flask import Blueprint, request, render_template, flash, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from app.models import User
from app import db
from app.forms import UserCreateForm, UserLoginForm


            # 우리가 부를 이름, flask 프레임워크가 찾을 이름, 라우팅주소    
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/signup/', methods=(['GET', 'POST']))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 이미 있는 id가 아닌지 확인
        user = User.query.filter_by(username=form.username.data)
        # db에 username이 없다면
        if not user:
            # form에서 받은 데이터로 user라는 객체를 만들어서
            user = User(username=form.username.data, password=form.password1.data, email=form.email.data)
            # db의 user 테이블에 추가
            db.session.add(user)
            # db에 커밋
            db.session.commit()
            return redirect(url_for('basic.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('user/signup.html', form=form)


# /login/ URL과 매핑되는 login 함수는 signup 함수와 비슷하게 동작합니다. POST 방식에는 로그인을 수행하고, GET 요청에는 로그인 화면을 보여줍니다.
@auth.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
				# 폼 입력으로 받은 username으로 데이터베이스에 해당 사용자가 있는지를 검사한다. 만약 사용자가 없으면 "존재하지 않는 사용자입니다."라는 오류를 발생시키고, 사용자가 있다면 폼 입력으로 받은 password와 check_password_hash 함수를 사용하여 데이터베이스의 비밀번호와 일치하는지를 비교합니다.
        user = User.query.filter_by(username=form.username.data).first()
        
        # 로그인 자체가 막혀림 
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
            
        # 아무 문제가 없으면 
        if error is None:
            # 사용자도 존재하고 비밀번호도 일치한다면 플라스크 서버의 나를 위한 저장소인 세션(session)에 사용자 정보를 저장합니다.

						# 세션에 user_id라는 객체 생성
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('basic.index'))
                
        # 에러메시지를 flash 한테 넘깁니다
        # 문제가 있으면 그 문제를 form_errors.html로 보내버리는 역할 
        flash(error)
    return render_template('auth/login.html', form=form)


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@auth.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('basic.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view