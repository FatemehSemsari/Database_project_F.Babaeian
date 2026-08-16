from datetime import timedelta

from apps.tickets.elastic_sync import (
    es,
    INDEX_NAME,
    create_index,
)


def search_tickets(filters):

    create_index()

    must_queries: list[dict] = []

    filter_queries: list[dict] = [
        {
            "term": {
                "event_status": "scheduled"
            }
        },

        {
            "range": {
                "event_datetime": {
                    "gte": "now"
                }
            }
        },

        {
            "range": {
                "available_count": {
                    "gt": 0
                }
            }
        },
    ]


    keyword = filters.get("keyword")

    if keyword:

        must_queries.append({
            "multi_match": {
                "query": keyword,

                "fields": [
                    "home_team_name^3",
                    "away_team_name^3",
                    "venue_name^2",
                    "city_name^2",
                    "sport_name^2",
                    "league_name",
                    "ticket_category_name",
                    "section_name",
                    "province_name",
                    "country_name",
                ],

                "type": "best_fields",
            }
        })



    sport_id = filters.get(
        "sport_id"
    )

    if sport_id is not None:

        filter_queries.append({
            "term": {
                "sport_id": sport_id
            }
        })


    team_id = filters.get(
        "team_id"
    )

    if team_id is not None:

        filter_queries.append({
            "bool": {
                "should": [
                    {
                        "term": {
                            "home_team_id": (
                                team_id
                            )
                        }
                    },
                    {
                        "term": {
                            "away_team_id": (
                                team_id
                            )
                        }
                    },
                ],
                "minimum_should_match": 1,
            }
        })


    city_id = filters.get(
        "city_id"
    )

    if city_id is not None:

        filter_queries.append({
            "term": {
                "city_id": city_id
            }
        })



    venue_id = filters.get(
        "venue_id"
    )

    if venue_id is not None:

        filter_queries.append({
            "term": {
                "venue_id": venue_id
            }
        })


    ticket_category_id = (
        filters.get(
            "ticket_category_id"
        )
    )

    if ticket_category_id is not None:

        filter_queries.append({
            "term": {
                "ticket_category_id": (
                    ticket_category_id
                )
            }
        })


    date_from = filters.get(
        "date_from"
    )

    date_to = filters.get(
        "date_to"
    )

    event_date_range = {}

    if date_from is not None:
        event_date_range["gte"] = (
            date_from.isoformat()
        )

    if date_to is not None:

        # < beginning of next day
        event_date_range["lt"] = (
            date_to
            + timedelta(days=1)
        ).isoformat()

    if event_date_range:

        filter_queries.append({
            "range": {
                "event_datetime": (
                    event_date_range
                )
            }
        })



    min_price = filters.get(
        "min_price"
    )

    max_price = filters.get(
        "max_price"
    )

    price_range = {}

    if min_price is not None:
        price_range["gte"] = min_price

    if max_price is not None:
        price_range["lte"] = max_price

    if price_range:

        filter_queries.append({
            "range": {
                "current_price": (
                    price_range
                )
            }
        })


    limit = filters.get(
        "limit",
        20,
    )

    offset = filters.get(
        "offset",
        0,
    )


    if keyword:
        sort = [
            {
                "_score": "desc"
            },
            {
                "event_datetime": "asc"
            },
            {
                "current_price": "asc"
            },
        ]

    else:
        sort = [
            {
                "event_datetime": "asc"
            },
            {
                "current_price": "asc"
            },
        ]

    response = es.search(
        index=INDEX_NAME,

        query={
            "bool": {
                "must": must_queries,
                "filter": filter_queries,
            }
        },

        from_=offset,
        size=limit,

        sort=sort,

        track_total_hits=True,
    )

    results = [
        hit["_source"]
        for hit
        in response["hits"]["hits"]
    ]

    total = (
        response["hits"]["total"]["value"]
    )

    return {
        "results": results,
        "total": total,
    }