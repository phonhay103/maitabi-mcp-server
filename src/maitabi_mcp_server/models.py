"""Pydantic input models for Maitabi MCP Server tools."""

from enum import IntEnum
from typing import Annotated, Optional
from pydantic import BaseModel, Field


class TravelType(IntEnum):
    """Category ID for Maitabi general tours (www.maitabi.jp)."""

    DOMESTIC_MOUNTAIN = 1  # Domestic Mountain Climbing / Trekking
    DOMESTIC_TRAVEL = 2  # Domestic Travel / Hiking
    MOUNTAIN_BUS = 3  # Mountain Bus
    OVERSEAS_MOUNTAIN = 4  # Overseas Mountain Climbing / Trekking
    OVERSEAS_TRAVEL = 5  # Overseas Travel


class DeparturePoint(IntEnum):
    """Point of departure for Maitabi bus tours (bus.maitabi.jp)."""

    TOKYO = 1  # Departure from Tokyo (Takebashi / Shinjuku)
    OSAKA_KYOTO = 2  # Departure from Osaka / Kyoto
    NAGOYA = 3  # Departure from Nagoya


class TourStyle(IntEnum):
    """Tour style ID for mountain bus tours."""

    ROUND_TRIP_BUS = 1  # Round-trip bus only
    OUTBOUND_BUS = 2  # Outbound bus only
    INBOUND_BUS = 3  # Inbound bus only
    ROUND_TRIP_LODGE = 4  # Round-trip bus with mountain lodge
    OUTBOUND_LODGE = 5  # Outbound bus with mountain lodge
    OVERNIGHT_DAY_TRIP = 6  # Overnight day-trip / round-trip overnight bus
    TAXI_PLAN = 7  # Taxi plan


class ReturnDayOption(IntEnum):
    """Return date option ID for mountain bus tours relative to departure."""

    DAY_1 = 1  # 1 day after departure (overnight day-trip)
    DAY_2 = 2  # 2 days after departure (1 night stay)
    DAY_3 = 3  # 3 days after departure (2 nights stay)
    DAY_4 = 4  # 4 days after departure (3 nights stay)
    DAY_5 = 5  # 5 days after departure (4 nights stay)


class BusSeatType(IntEnum):
    """Bus seat configuration ID for mountain bus tours."""

    STANDARD = 1  # Standard seat
    PREMIUM = 2  # Premium seat
    OUTBOUND_PREMIUM_INBOUND_STANDARD = 3  # Outbound Premium, Inbound Standard
    OUTBOUND_STANDARD_INBOUND_PREMIUM = 4  # Outbound Standard, Inbound Premium
    DOUBLE_SEAT = 5  # Double seat option
    TAXI = 6  # Taxi option


class ListFiltersInput(BaseModel):
    """Input schema for fetching bus tour filter options."""

    departure: Annotated[
        DeparturePoint,
        Field(
            default=DeparturePoint.TOKYO,
            description="Departure point: 1=Tokyo (Takebashi/Shinjuku), 2=Osaka/Kyoto, 3=Nagoya",
        ),
    ]
    month: Annotated[
        Optional[int],
        Field(
            default=None,
            ge=1,
            le=12,
            description="Departure month (1-12). Defaults to current month if omitted.",
        ),
    ]
    day: Annotated[
        Optional[int],
        Field(default=None, ge=1, le=31, description="Departure day (1-31)"),
    ] = None
    area: Annotated[
        Optional[int],
        Field(
            default=None,
            ge=0,
            description="Area/direction ID (e.g., 18=Tateyama Murodo, 10=Kamikochi, 0=All)",
        ),
    ] = None
    style: Annotated[
        Optional[TourStyle],
        Field(
            default=None,
            description="Tour style: 1=Round-trip bus, 2=Outbound bus, 3=Inbound bus, 4=Round-trip lodge, 5=Outbound lodge, 6=Overnight day-trip, 7=Taxi plan",
        ),
    ] = None
    return_day: Annotated[
        Optional[ReturnDayOption],
        Field(
            default=None,
            description="Return date option: 1=1 day after departure, 2=2 days after, 3=3 days after, 4=4 days after, 5=5 days after",
        ),
    ] = None
    bus_sheet: Annotated[
        Optional[BusSeatType],
        Field(
            default=None,
            description="Bus seat type: 1=Standard, 2=Premium, 3=Outbound Premium / Inbound Standard, 4=Outbound Standard / Inbound Premium, 5=Double seat, 6=Taxi",
        ),
    ] = None
    stay1: Annotated[
        Optional[int],
        Field(
            default=None,
            ge=1,
            description="Mountain lodge ID for night 1 (e.g., 5=Enzanso, 2=Nishiho Sanso)",
        ),
    ] = None
    stay2: Annotated[
        Optional[int],
        Field(default=None, ge=1, description="Mountain lodge ID for night 2"),
    ] = None
    stay3: Annotated[
        Optional[int],
        Field(default=None, ge=1, description="Mountain lodge ID for night 3"),
    ] = None
    course_cd: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=50,
            description="Maitabi course code (e.g., 'S104C21')",
        ),
    ] = None
    keyword: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=100,
            description="Search keyword in Japanese (e.g., '立山', '上高地')",
        ),
    ] = None


class ListDistrictGroupsInput(BaseModel):
    """Input schema for fetching mountain area/district groups."""

    departure: Annotated[
        DeparturePoint,
        Field(
            default=DeparturePoint.TOKYO,
            description="Departure point: 1=Tokyo (Takebashi/Shinjuku), 2=Osaka/Kyoto, 3=Nagoya",
        ),
    ]
    month: Annotated[
        Optional[int],
        Field(
            default=None,
            ge=1,
            le=12,
            description="Departure month (1-12). Defaults to current month if omitted.",
        ),
    ]
    day: Annotated[
        Optional[int],
        Field(default=None, ge=1, le=31, description="Departure day (1-31)"),
    ] = None
    area: Annotated[
        Optional[int],
        Field(
            default=None,
            ge=0,
            description="Area/direction ID (e.g., 18=Tateyama Murodo, 10=Kamikochi, 0=All)",
        ),
    ] = None
    style: Annotated[
        Optional[TourStyle],
        Field(
            default=None,
            description="Tour style: 1=Round-trip bus, 2=Outbound bus, 3=Inbound bus, 4=Round-trip lodge, 5=Outbound lodge, 6=Overnight day-trip, 7=Taxi plan",
        ),
    ] = None
    return_day: Annotated[
        Optional[ReturnDayOption],
        Field(
            default=None,
            description="Return date option: 1=1 day after departure, 2=2 days after, 3=3 days after, 4=4 days after, 5=5 days after",
        ),
    ] = None
    bus_sheet: Annotated[
        Optional[BusSeatType],
        Field(
            default=None,
            description="Bus seat type: 1=Standard, 2=Premium, 3=Outbound Premium / Inbound Standard, 4=Outbound Standard / Inbound Premium, 5=Double seat, 6=Taxi",
        ),
    ] = None
    stay1: Annotated[
        Optional[int],
        Field(
            default=None,
            ge=1,
            description="Mountain lodge ID for night 1 (e.g., 5=Enzanso, 2=Nishiho Sanso)",
        ),
    ] = None
    stay2: Annotated[
        Optional[int],
        Field(default=None, ge=1, description="Mountain lodge ID for night 2"),
    ] = None
    stay3: Annotated[
        Optional[int],
        Field(default=None, ge=1, description="Mountain lodge ID for night 3"),
    ] = None
    course_cd: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=50,
            description="Maitabi course code (e.g., 'S104C21')",
        ),
    ] = None
    keyword: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=100,
            description="Search keyword in Japanese (e.g., '立山', '上高地')",
        ),
    ] = None


class SearchBusToursInput(BaseModel):
    """Input schema for searching mountain bus tours."""

    departure: Annotated[
        DeparturePoint,
        Field(
            default=DeparturePoint.TOKYO,
            description="Departure point: 1=Tokyo (Takebashi/Shinjuku), 2=Osaka/Kyoto, 3=Nagoya",
        ),
    ]
    month: Annotated[
        Optional[int],
        Field(default=None, ge=1, le=12, description="Departure month (1-12)"),
    ]
    day: Annotated[
        Optional[int],
        Field(default=None, ge=1, le=31, description="Departure day (1-31)"),
    ]
    area: Annotated[
        Optional[int],
        Field(
            default=None,
            ge=0,
            description="Area/direction ID (e.g., 18=Tateyama Murodo, 10=Kamikochi, 0=All)",
        ),
    ]
    style: Annotated[
        Optional[TourStyle],
        Field(
            default=None,
            description="Tour style: 1=Round-trip bus, 2=Outbound bus, 3=Inbound bus, 4=Round-trip lodge, 5=Outbound lodge, 6=Overnight day-trip, 7=Taxi plan",
        ),
    ]
    return_day: Annotated[
        Optional[ReturnDayOption],
        Field(
            default=None,
            description="Return date option: 1=1 day after departure, 2=2 days after, 3=3 days after, 4=4 days after, 5=5 days after",
        ),
    ]
    bus_sheet: Annotated[
        Optional[BusSeatType],
        Field(
            default=None,
            description="Bus seat type: 1=Standard, 2=Premium, 3=Outbound Premium / Inbound Standard, 4=Outbound Standard / Inbound Premium, 5=Double seat, 6=Taxi",
        ),
    ]
    stay1: Annotated[
        Optional[int],
        Field(
            default=None,
            ge=1,
            description="Mountain lodge ID for night 1 (e.g., 5=Enzanso, 2=Nishiho Sanso)",
        ),
    ]
    stay2: Annotated[
        Optional[int],
        Field(default=None, ge=1, description="Mountain lodge ID for night 2"),
    ] = None
    stay3: Annotated[
        Optional[int],
        Field(default=None, ge=1, description="Mountain lodge ID for night 3"),
    ] = None
    course_cd: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=50,
            description="Maitabi course code (e.g., 'S104C21')",
        ),
    ]
    keyword: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=100,
            description="Search keyword in Japanese (e.g., '立山', '上高地')",
        ),
    ]
    page: Annotated[int, Field(default=1, ge=1, description="Page number (1-based)")]


class GetBusTourDetailInput(BaseModel):
    """Input schema for fetching bus tour detail by course number."""

    course_no: Annotated[
        int,
        Field(
            gt=0,
            description="Internal course number on bus.maitabi.jp (e.g., 14241, 8518)",
        ),
    ]


class SearchGeneralToursInput(BaseModel):
    """Input schema for searching general tours."""

    travel_type: Annotated[
        TravelType,
        Field(
            default=TravelType.DOMESTIC_MOUNTAIN,
            description="Category ID: 1=Domestic Mountain Climbing/Trekking, 2=Domestic Travel/Hiking, 3=Mountain Bus, 4=Overseas Mountain Climbing, 5=Overseas Travel",
        ),
    ]
    keyword: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=100,
            description="Search keyword in Japanese (e.g., '富士山', '京都')",
        ),
    ]
    year_month: Annotated[
        Optional[str],
        Field(
            default=None,
            pattern=r"^\d{4}-(?:0[1-9]|1[0-2])$",
            description="Departure year-month string in 'YYYY-MM' format (e.g., '2026-08')",
        ),
    ]
    day: Annotated[
        Optional[int],
        Field(default=None, ge=1, le=31, description="Departure day of month (1-31)"),
    ]
    page: Annotated[int, Field(default=1, ge=1, description="Page number (1-based)")]
    list_order: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Sort order: 'startDateAsc' (departure earliest), 'saikouStatus' (departure status), 'yoyakuStatus' (availability), 'priceAsc' (price low to high), 'priceDesc' (price high to low)",
        ),
    ] = None
    category_nos1: Annotated[
        Optional[list[int]],
        Field(
            default=None,
            description="Subcategory Nos for Style/Duration (e.g. [36] for Day trip, [259] for Overnight)",
        ),
    ] = None
    category_nos2: Annotated[
        Optional[list[int]],
        Field(
            default=None,
            description="Subcategory Nos for Difficulty/Shoes (e.g. [363] for Grade 1 / Introduction)",
        ),
    ] = None
    category_nos3: Annotated[
        Optional[list[int]],
        Field(
            default=None,
            description="Subcategory Nos for Departure Region (e.g. [13] for Kanto, [15] for Tokai)",
        ),
    ] = None
    category_nos4: Annotated[
        Optional[list[int]],
        Field(
            default=None,
            description="Subcategory Nos for Themes/Tours",
        ),
    ] = None
    category_nos5: Annotated[
        Optional[list[int]],
        Field(
            default=None,
            description="Subcategory Nos for Guides",
        ),
    ] = None


class GetGeneralTourDetailInput(BaseModel):
    """Input schema for fetching general tour detail by course number."""

    course_no: Annotated[
        int,
        Field(
            gt=0,
            description="Tour course number on www.maitabi.jp (e.g., 1723, 24865)",
        ),
    ]


class GetTourCalendarInput(BaseModel):
    """Input schema for fetching tour schedule calendar."""

    year: Annotated[
        int,
        Field(ge=2000, le=2100, description="Year (e.g., 2026)"),
    ]
    month: Annotated[
        int,
        Field(ge=1, le=12, description="Month (1-12)"),
    ]
    travel_type: Annotated[
        Optional[TravelType],
        Field(
            default=None,
            description="Optional category ID filter: 1=Domestic Mountain, 2=Domestic Travel, 3=Mountain Bus, 4=Overseas Mountain, 5=Overseas Travel",
        ),
    ]
