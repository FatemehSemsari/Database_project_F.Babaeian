from django.db import connection
from apps.accounts import sql


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


class UserRepository:
    @staticmethod
    def exists_by_email_or_phone(email=None, phone=None):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.CHECK_USER_EXISTS_BY_EMAIL_OR_PHONE,
                [email, email, phone, phone],
            )
            row = cursor.fetchone()
        return row is not None

    @staticmethod
    def create_user(
            first_name,
            last_name,
            email,
            phone,
            password_hash,
            role,
            email_verified,
            phone_verified,
    ):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.CREATE_USER,
                [
                    first_name,
                    last_name,
                    email,
                    phone,
                    password_hash,
                    role,
                    email_verified,
                    phone_verified,
                ],
            )
            return dict_fetchone(cursor)

    @staticmethod
    def get_user_by_id(user_id):
        with connection.cursor() as cursor:
            cursor.execute(sql.GET_USER_BY_ID, [user_id])
            return dict_fetchone(cursor)