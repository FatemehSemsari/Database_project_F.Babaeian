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

    @staticmethod
    def get_user_by_email(email):
        with connection.cursor() as cursor:
            cursor.execute(sql.GET_USER_BY_EMAIL, [email])
            return dict_fetchone(cursor)

    @staticmethod
    def get_user_by_phone(phone):
        with connection.cursor() as cursor:
            cursor.execute(sql.GET_USER_BY_PHONE, [phone])
            return dict_fetchone(cursor)

    @staticmethod
    def update_profile(user_id,first_name=None,last_name=None):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.UPDATE_USER_PROFILE,
                [
                    first_name,
                    last_name,
                    user_id,
                ],
            )
            return dict_fetchone(cursor)

    @staticmethod
    def get_user_auth_by_id(user_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.GET_USER_AUTH_BY_ID,
                [user_id],
            )
            return dict_fetchone(cursor)

    @staticmethod
    def update_email(user_id, new_email):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.UPDATE_USER_EMAIL,
                [
                    new_email,
                    user_id,
                ],
            )
            return dict_fetchone(cursor)

    @staticmethod
    def update_phone(user_id, new_phone):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.UPDATE_USER_PHONE,
                [
                    new_phone,
                    user_id,
                ],
            )
            return dict_fetchone(cursor)

    @staticmethod
    def update_password(user_id, new_password_hash):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.UPDATE_USER_PASSWORD,
                [
                    new_password_hash,
                    user_id,
                ],
            )
            return cursor.fetchone() is not None