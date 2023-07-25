import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connecting():
    return psycopg2.connect(DATABASE_URL)


def get_id(url):
    with connecting() as connect:
        with connect.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM urls WHERE name = %s", (url,)
            )
            url_id = cursor.fetchone()
    connect.close()
    return url_id


def get_data():
    with connecting() as connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT urls.id, urls.name, url_checks.created_at, "
                           "url_checks.status_code "
                           "FROM urls LEFT JOIN url_checks "
                           "ON urls.id = url_checks.url_id "
                           "WHERE url_checks.url_id IS NULL OR "
                           "url_checks.id = (SELECT MAX(url_checks.id) "
                           "FROM url_checks "
                           "WHERE url_checks.url_id = urls.id) "
                           "ORDER BY urls.id DESC")
            url_data = cursor.fetchall()
    connect.close()
    return url_data


def get_info(id):
    with connecting() as connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT id, name, created_at FROM urls "
                           "WHERE id = %s", (id,))
            url_info = cursor.fetchone()
    connect.close()
    return url_info


def check_info(id):
    with connecting() as connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM url_checks WHERE url_id = %s", (id,))
            check_result = cursor.fetchall()
    connect.close()
    return check_result


def add_into_database(url, today):
    with connecting() as connect:
        with connect.cursor() as cursor:
            cursor.execute("INSERT INTO urls (name, created_at) "
                           "VALUES (%s, %s) RETURNING id",
                           (url, today))
            result = cursor.fetchone()
    connect.close()
    return result


def check_result(id, data, today_date):
    with connecting() as connect:
        with connect.cursor() as cursor:
            cursor.execute("INSERT INTO url_checks "
                           "(url_id, status_code, h1, title, description, "
                           "created_at) "
                           "VALUES (%s, %s, %s, %s, %s, %s)",
                           (id, data['status_code'], data['h1'],
                            data['title'], data['description'], today_date,))
    connect.close()
