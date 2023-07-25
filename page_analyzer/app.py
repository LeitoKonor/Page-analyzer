from flask import (Flask, flash, get_flashed_messages,
                   render_template, request, redirect, url_for)
import os
from dotenv import load_dotenv
from datetime import date
from page_analyzer.url import url_analyzes, url_check, make_check
from page_analyzer.data_base import (get_id, add_into_data_base, get_data,
                                     get_info, check_info, check_result)


app = Flask(__name__)


load_dotenv()


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    notification = get_flashed_messages(with_categories=True)
    return render_template('index.html', notification=notification)


@app.post('/urls')
def post_url():
    input_site = request.form['url']
    check = url_check(input_site)

    if not check.get('valid'):
        message = check.get('message')
        flash(f'{message}', category="alert alert-danger")
        notification = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            notification=notification,
            wrong_url=input_site
        ), 422

    parse = url_analyzes(input_site)
    today = date.today()

    result = get_id(parse)
    if result:
        (url_id, *_) = result
        flash('Страница уже существует', category="alert alert-info")
        return redirect(url_for('show_url', id=url_id))

    else:
        id_info = add_into_data_base(parse, today)
        (url_id, *_) = id_info

        flash('Страница успешно добавлена', category="alert alert-success")
        return redirect(url_for('show_url', id=url_id))


@app.get('/urls')
def get_url():
    data = get_data()
    return render_template('urls.html', data=data)


@app.get('/urls/<int:id>')
def show_url(id):
    notification = get_flashed_messages(with_categories=True)

    (url_id, name, created_at) = get_info(id)
    result = check_info(id)

    return render_template(
        'show_url.html',
        notification=notification,
        url_id=url_id,
        name=name,
        created_at=created_at,
        result=result,
    )


@app.post('/urls/<int:id>/checks')
def url_validation(id):
    url_name = request.form['url_name']

    check = make_check(url_name)

    if check is None:
        flash('Произошла ошибка при проверке', category="alert alert-danger")
        return redirect(url_for('show_url', id=id))

    today = date.today()
    check_result(id, check, today)

    flash('Страница успешно проверена', category='alert alert-success')
    return redirect(url_for('show_url', id=id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
