from django.db import connection

from apps.payments import sql


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


class PaymentRepository:

    @staticmethod
    def get_reservation_for_payment(reservation_id, user_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.GET_RESERVATION_FOR_PAYMENT,
                [
                    reservation_id,
                    user_id,
                ],
            )
            return dict_fetchone(cursor)

    @staticmethod
    def get_reservation_inventories_for_update(reservation_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.GET_RESERVATION_INVENTORIES_FOR_UPDATE,
                [
                    reservation_id,
                    reservation_id,
                ],
            )
            return dict_fetchall(cursor)

    @staticmethod
    def expire_reservation(reservation_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.EXPIRE_RESERVATION,
                [reservation_id],
            )

    @staticmethod
    def release_reservation_inventory(reservation_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.RELEASE_RESERVATION_INVENTORY,
                [reservation_id],
            )

    @staticmethod
    def create_successful_payment(reservation_id, amount, method, transaction_ref):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.CREATE_SUCCESSFUL_PAYMENT,
                [
                    reservation_id,
                    amount,
                    method,
                    transaction_ref,
                ],
            )
            return dict_fetchone(cursor)

    @staticmethod
    def mark_reservation_as_paid(reservation_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.MARK_RESERVATION_AS_PAID,
                [reservation_id],
            )
            return dict_fetchone(cursor)

    @staticmethod
    def mark_inventory_as_sold(reservation_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.MARK_RESERVATION_INVENTORY_AS_SOLD,
                [reservation_id],
            )

    @staticmethod
    def issue_tickets(reservation_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.ISSUE_RESERVATION_TICKETS,
                [reservation_id],
            )
            return dict_fetchall(cursor)