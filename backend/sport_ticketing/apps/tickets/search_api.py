from apps.tickets.elastic_sync import (es, INDEX_NAME)

def search_tickets(filters):
    query = {"bool": {"must": [], "filter": []}}

    if filters.get("sport"):
        query["bool"]["filter"].append({"match": {"sport": filters["sport"]}})
    if filters.get("city"):
        query["bool"]["filter"].append({"match": {"city": filters["city"]}})
    if filters.get("venue"):
        query["bool"]["filter"].append({"match": {"venue": filters["venue"]}})
    if filters.get("keyword"):
        query["bool"]["must"].append({
            "multi_match": {
                "query": filters["keyword"],
                "fields": ["sport", "team_home", "team_away", "city", "venue"]
            }
        })

    return es.search(index=INDEX_NAME, query=query)
