from django.core.management.base import (
    BaseCommand,
)

from apps.tickets.repositories import (
    TicketRepository,
)

from apps.tickets.elastic_sync import (
    es,
    INDEX_NAME,
    recreate_index,
    index_ticket_category,
)


class Command(BaseCommand):

    help = (
        "Synchronize searchable ticket "
        "categories from PostgreSQL "
        "to Elasticsearch."
    )

    def handle(
        self,
        *args,
        **options,
    ):

        self.stdout.write(
            "Recreating Elasticsearch index..."
        )

        recreate_index()

        batch_size = 500
        offset = 0
        total = 0

        while True:

            rows = (
                TicketRepository
                .search_tickets({
                    "limit": batch_size,
                    "offset": offset,
                })
            )

            if not rows:
                break

            for row in rows:

                index_ticket_category(
                    row,
                    refresh=False,
                )

            total += len(rows)

            offset += batch_size

            if len(rows) < batch_size:
                break

        es.indices.refresh(
            index=INDEX_NAME
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Elasticsearch sync "
                f"completed. "
                f"{total} documents indexed."
            )
        )