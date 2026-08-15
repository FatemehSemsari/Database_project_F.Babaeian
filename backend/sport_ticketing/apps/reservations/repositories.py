from django.db import connection

from apps.reservations import sql


def dict_fetchall(cursor):
    columns = [
        column[0]
        for column in cursor.description
    ]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class ReservationRepository:
    @staticmethod
    def get_available_seats(ticket_category_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.GET_AVAILABLE_SEATS,
                [ticket_category_id],
            )
            return dict_fetchall(cursor)

    @staticmethod
    def cleanup_expired_reservations():
        with connection.cursor() as cursor:
            cursor.execute(
                sql.EXPIRE_PENDING_RESERVATIONS
            )
            cursor.execute(
                sql.RELEASE_EXPIRED_INVENTORY
            )

    @staticmethod
    def get_inventory_for_reservation(inventory_id, ticket_category_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.GET_INVENTORY_FOR_RESERVATION,
                [
                    inventory_id,
                    ticket_category_id,
                ],
            )
            row = cursor.fetchone()
            if row is None:
                return None
            columns = [
                column[0]
                for column in cursor.description
            ]
            return dict(zip(columns, row))

    @staticmethod
    def create_reservation(user_id, event_id, total_amount, expires_at):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.CREATE_RESERVATION,
                [
                    user_id,
                    event_id,
                    total_amount,
                    expires_at,
                ],
            )
            row = cursor.fetchone()
            columns = [
                column[0]
                for column in cursor.description
            ]
            return dict(zip(columns, row))

    @staticmethod
    def create_reservation_item(reservation_id, ticket_category_id, price):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.CREATE_RESERVATION_ITEM,
                [
                    reservation_id,
                    ticket_category_id,
                    price,
                ],
            )
            return cursor.fetchone()

    @staticmethod
    def hold_inventory(reservation_id, reserve_key, held_until, inventory_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.HOLD_INVENTORY,
                [
                    reservation_id,
                    reserve_key,
                    held_until,
                    inventory_id,
                ],
            )
            row = cursor.fetchone()
            if row is None:
                return None
            columns = [
                column[0]
                for column in cursor.description
            ]
            return dict(zip(columns, row))


    @staticmethod
    def get_active_user_reservations(user_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.GET_ACTIVE_USER_RESERVATIONS,
                [user_id],
            )
            return dict_fetchall(cursor)


    @staticmethod
    def get_user_reservation_history(user_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.GET_USER_RESERVATION_HISTORY,
                [user_id],
            )
            return dict_fetchall(cursor)

    @staticmethod
    def create_reservation_seat(reservation_id, inventory_id):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.CREATE_RESERVATION_SEAT,
                [
                    reservation_id,
                    inventory_id,
                ],
            )
            row = cursor.fetchone()
            columns = [
                column[0]
                for column in cursor.description
            ]
            return dict(zip(columns, row))