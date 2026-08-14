from django.db import connection
from apps.support import sql


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [
        column[0]
        for column in cursor.description
    ]
    return dict(zip(columns, row))


def dict_fetchall(cursor):
    columns = [
        column[0]
        for column in cursor.description
    ]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class SupportRepository:

    @staticmethod
    def list_cancelled_tickets(limit, offset):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.LIST_CANCELLED_TICKETS,
                [
                    limit,
                    offset,
                ],
            )
            return dict_fetchall(cursor)


    @staticmethod
    def list_suspicious_payments(limit, offset):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.LIST_SUSPICIOUS_PAYMENTS,
                [
                    limit,
                    offset,
                ],
            )
            return dict_fetchall(cursor)


    @staticmethod
    def list_reports(status=None, issue_type=None, limit=50, offset=0):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.LIST_SUPPORT_REPORTS,
                [
                    status,
                    status,
                    issue_type,
                    issue_type,
                    limit,
                    offset,
                ],
            )
            return dict_fetchall(cursor)


    @staticmethod
    def update_report(report_id, support_user_id, status=None, support_response=None):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.UPDATE_SUPPORT_REPORT,
                [
                    status,
                    support_response,
                    support_user_id,
                    report_id,
                ],
            )
            return dict_fetchone(cursor)


    @staticmethod
    def list_reservations(reservation_status=None, support_review_status=None, limit=50, offset=0):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.LIST_SUPPORT_RESERVATIONS,
                [
                    reservation_status,
                    reservation_status,
                    support_review_status,
                    support_review_status,
                    limit,
                    offset,
                ],
            )
            return dict_fetchall(cursor)


    @staticmethod
    def get_reservation_for_update(reservation_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.GET_RESERVATION_FOR_SUPPORT_UPDATE,
                [reservation_id],
            )
            return dict_fetchone(cursor)


    @staticmethod
    def approve_reservation(reservation_id, support_user_id, note=None):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.APPROVE_RESERVATION_BY_SUPPORT,
                [
                    support_user_id,
                    note,
                    reservation_id,
                ],
            )
            return dict_fetchone(cursor)


    @staticmethod
    def modify_reservation_expiry(reservation_id, expires_at, support_user_id, note=None):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.MODIFY_RESERVATION_EXPIRY,
                [
                    expires_at,
                    support_user_id,
                    note,
                    reservation_id,
                ],
            )
            return dict_fetchone(cursor)


    @staticmethod
    def sync_inventory_expiry(reservation_id, expires_at):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SYNC_RESERVATION_INVENTORY_EXPIRY,
                [
                    expires_at,
                    reservation_id,
                    reservation_id,
                ],
            )


    @staticmethod
    def cancel_reservation(reservation_id, support_user_id, note=None):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.CANCEL_RESERVATION_BY_SUPPORT,
                [
                    support_user_id,
                    note,
                    reservation_id,
                ],
            )
            return dict_fetchone(cursor)


    @staticmethod
    def release_cancelled_reservation(reservation_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.RELEASE_SUPPORT_CANCELLED_RESERVATION,
                [
                    reservation_id,
                    reservation_id,
                ],
            )