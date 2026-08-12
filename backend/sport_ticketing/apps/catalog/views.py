from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.catalog.serializers import (
    CityListQuerySerializer,
    CityResponseSerializer,
    VenueListQuerySerializer,
    VenueResponseSerializer,
    SportListQuerySerializer,
    SportResponseSerializer,
    LeagueListQuerySerializer,
    LeagueResponseSerializer,
    TeamListQuerySerializer,
    TeamResponseSerializer,
)
from apps.catalog.services import CatalogService


@api_view(["GET"])
@permission_classes([AllowAny])
def city_list(request):
    query_serializer = CityListQuerySerializer(data=request.query_params)
    if not query_serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": query_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    cities = CatalogService.get_cities(
        validated_filters=query_serializer.validated_data
    )
    response_serializer = CityResponseSerializer(cities, many=True)
    return Response(
        {
            "success": True,
            "message": (
                "Cities retrieved successfully."
            ),
            "data": {
                "cities": response_serializer.data,
                "count": len(
                    response_serializer.data
                ),
            },
        },
        status=status.HTTP_200_OK,
    )

@api_view(["GET"])
@permission_classes([AllowAny])
def venue_list(request):
    query_serializer = VenueListQuerySerializer(data=request.query_params)
    if not query_serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": query_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    venues = CatalogService.get_venues(validated_filters=query_serializer.validated_data)
    response_serializer = VenueResponseSerializer(venues, many=True)
    return Response(
        {
            "success": True,
            "message": (
                "Venues retrieved successfully."
            ),
            "data": {
                "venues": response_serializer.data,
                "count": len(
                    response_serializer.data
                ),
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def sport_list(request):
    query_serializer = SportListQuerySerializer(data=request.query_params)
    if not query_serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": query_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    sports = CatalogService.get_sports(validated_filters=query_serializer.validated_data)
    response_serializer = SportResponseSerializer(sports, many=True)
    return Response(
        {
            "success": True,
            "message": "Sports retrieved successfully.",
            "data": {
                "sports": response_serializer.data,
                "count": len(response_serializer.data),
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def league_list(request):
    query_serializer = LeagueListQuerySerializer(data=request.query_params)
    if not query_serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": query_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    leagues = CatalogService.get_leagues(validated_filters=query_serializer.validated_data)
    response_serializer = LeagueResponseSerializer(leagues, many=True)
    return Response(
        {
            "success": True,
            "message": "Leagues retrieved successfully.",
            "data": {
                "leagues": response_serializer.data,
                "count": len(response_serializer.data),
            },
        },
        status=status.HTTP_200_OK,
    )



@api_view(["GET"])
@permission_classes([AllowAny])
def team_list(request):
    query_serializer = TeamListQuerySerializer(data=request.query_params)
    if not query_serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": query_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    teams = CatalogService.get_teams(validated_filters = query_serializer.validated_data)
    response_serializer = TeamResponseSerializer(teams, many=True)
    return Response(
        {
            "success": True,
            "message": "Teams retrieved successfully.",
            "data": {
                "teams": response_serializer.data,
                "count": len(response_serializer.data),
            },
        },
        status=status.HTTP_200_OK,
    )



