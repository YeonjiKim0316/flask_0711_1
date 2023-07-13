from flask import Blueprint, request, render_template, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from app.models import User
from app import db
from app.forms import UserCreateForm


# 우리가 부를 이름, flask 프레임워크가 찾을 이름, 라우팅주소
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 이미 있는 id가 아닌지 확인
        user = User.query.filter_by(username=form.username.data).first()
        # db에 이 username이 없다면 
        if not user:
            # form에서 받은 데이터로 user라는 객체를 만들어서 
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            # db의 user 테이블에 추가합니다.
            db.session.add(user)
            # db에 커밋합니다
            db.session.commit()
            return redirect(url_for('basic.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)