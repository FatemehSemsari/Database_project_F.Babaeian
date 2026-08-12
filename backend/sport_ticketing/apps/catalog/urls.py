from django.urls import path
from apps.catalog.views import city_list, venue_list, sport_list, league_list, team_list

urlpatterns = [
    path("cities/", city_list, name="catalog-city-list"),
    path("venues/", venue_list, name="catalog-venue-list"),
    path("sports/", sport_list, name="catalog-sport-list"),
    path("leagues/", league_list, name="catalog-league-list"),
    path("teams/", team_list, name="catalog-team-list"),
]