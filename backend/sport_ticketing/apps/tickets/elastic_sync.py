from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "tickets_search"

def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            mappings={
                "properties": {
                    "ticket_id": {"type": "integer"},
                    "sport": {"type": "text"},
                    "team_home": {"type": "text"},
                    "team_away": {"type": "text"},
                    "city": {"type": "text"},
                    "venue": {"type": "text"},
                    "match_time": {"type": "date"},
                    "price": {"type": "integer"},
                    "section": {"type": "text"},
                    "remaining_capacity": {"type": "integer"}
                }
            }
        )

def index_ticket(ticket):
    es.index(index=INDEX_NAME, id=ticket["ticket_id"], document=ticket)

def update_ticket(ticket):
    es.index(index=INDEX_NAME, id=ticket["ticket_id"], document=ticket)

def delete_ticket_from_es(ticket_id):
    es.delete(index=INDEX_NAME, id=ticket_id, ignore=[404])
