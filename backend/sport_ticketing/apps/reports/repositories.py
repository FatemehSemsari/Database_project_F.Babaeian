from django.db import connection
from apps.reports import sql


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [
        column[0]
        for column in cursor.description
    ]
    return dict(zip(columns, row))


class ReportRepository:
    @staticmethod
    def get_user_ticket(ticket_id, user_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.GET_USER_TICKET_REPORT_TARGET,
                [
                    ticket_id,
                    user_id,
                ],
            )
            return dict_fetchone(cursor)

    @staticmethod
    def get_user_reservation(reservation_id, user_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.GET_USER_RESERVATION_REPORT_TARGET,
                [
                    reservation_id,
                    user_id,
                ],
            )
            return dict_fetchone(cursor)

    @staticmethod
    def create_report(user_id, ticket_id, reservation_id, issue_type, message):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.CREATE_REPORT,
                [
                    user_id,
                    ticket_id,
                    reservation_id,
                    issue_type,
                    message,
                ],
            )
            return dict_fetchone(cursor)