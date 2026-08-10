"""Pydantic input models for Maitabi MCP Server tools."""

from typing import Annotated, Optional
from pydantic import BaseModel, Field


class ListFiltersInput(BaseModel):
    departure: Annotated[int, Field(default=1, description="Point of departure: 1=Tokyo, 2=Osaka/Kyoto, 3=Nagoya")]
    month: Annotated[Optional[int], Field(default=None, description="Departure month (1-12). Defaults to current month if omitted.")]


class ListDistrictGroupsInput(BaseModel):
    departure: Annotated[int, Field(default=1, description="Point of departure: 1=Tokyo, 2=Osaka/Kyoto, 3=Nagoya")]
    month: Annotated[Optional[int], Field(default=None, description="Departure month (1-12). Defaults to current month if omitted.")]


class SearchBusToursInput(BaseModel):
    departure: Annotated[int, Field(default=1, description="Point of departure: 1=Tokyo, 2=Osaka/Kyoto, 3=Nagoya")]
    month: Annotated[Optional[int], Field(default=None, description="Departure month (1-12)")]
    day: Annotated[Optional[int], Field(default=None, description="Departure day (1-31)")]
    area: Annotated[Optional[int], Field(default=None, description="Area/direction ID (e.g. 18=Tateyama Murodo, 10=Kamikochi)")]
    style: Annotated[Optional[int], Field(default=None, description="Tour style ID (e.g. 6=Night trip/round-trip)")]
    return_day: Annotated[Optional[int], Field(default=None, description="Return date option ID (1=1 day after, 2=2 days after)")]
    bus_sheet: Annotated[Optional[int], Field(default=None, description="Bus seat type ID (1=Standard, 2=Premium)")]
    stay1: Annotated[Optional[int], Field(default=None, description="Mountain lodge ID for night 1")]
    stay2: Annotated[Optional[int], Field(description="Mountain lodge ID for night 2")] = None
    stay3: Annotated[Optional[int], Field(description="Mountain lodge ID for night 3")] = None
    course_cd: Annotated[Optional[str], Field(default=None, description="Course code (e.g. 'S104C21')")]
    keyword: Annotated[Optional[str], Field(default=None, description="Search keyword in Japanese (e.g. '立山')")]
    page: Annotated[int, Field(default=1, description="Page number")]


class GetBusTourDetailInput(BaseModel):
    course_no: Annotated[int, Field(description="Internal course number (e.g. 14241 or 8518)")]


class SearchGeneralToursInput(BaseModel):
    travel_type: Annotated[int, Field(default=1, description="Category ID: 1=Domestic Mountain Climbing/Trekking, 2=Domestic Travel/Hiking, 3=Mountain Bus, 4=Overseas Mountain Climbing/Trekking, 5=Overseas Travel")]
    keyword: Annotated[Optional[str], Field(default=None, description="Search keyword in Japanese (e.g. '富士山', '京都')")]
    year_month: Annotated[Optional[str], Field(default=None, description="Departure year-month string (e.g. '2026-08')")]
    day: Annotated[Optional[int], Field(default=None, description="Departure day (1-31)")]
    page: Annotated[int, Field(default=1, description="Page number")]


class GetGeneralTourDetailInput(BaseModel):
    course_no: Annotated[int, Field(description="Tour course number on www.maitabi.jp (e.g. 1723, 24865)")]


class GetTourCalendarInput(BaseModel):
    year: Annotated[int, Field(description="Year (e.g. 2026)")]
    month: Annotated[int, Field(description="Month (1-12)")]
    travel_type: Annotated[Optional[int], Field(default=None, description="Optional category ID filter (1=Domestic Mountain, 2=Domestic Travel, 3=Mountain Bus, 4=Overseas Mountain, 5=Overseas Travel)")]
