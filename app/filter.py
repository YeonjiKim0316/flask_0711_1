# 필터를 템플릿에서 사용하려면 app/__init__.py 파일의 create_app 함수를 다음처럼 수정해야 한다.
def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M'):
    return value.strftime(fmt)

def format_datetime2(value, fmt='%Y/%m/%d %I:%M %p'):
    return value.strftime(fmt)