from datetime import datetime, timedelta, timezone
from typing import Any, List, Union

import fastapi
import pytz
from fastapi import APIRouter, Query
from geopy import Nominatim
from pydantic import BaseModel

import src.model.data_fetcher as model
from src.exception.validation import ValidationError

# Initializing router
router = APIRouter()


# Model Class for Response using pydantic
class Item(BaseModel):
    """
    Base Model For Resonse
    """

    start_period_utc: str
    end_period_utc: str
    cloud_cover: str
    temparature_in_celcius: str


# API Endpoint for the weather to search based on Latitude and Longitude
@router.get("/api/7timer-latlon/", tags=["Weather Forecast"], response_model=List[Item])
async def get_weather_latlon(
    latitude: float = Query(
        ...,
        title="Latitude",
        description="Query string for the weather to search based on Latitude",
    ),
    longitude: float = Query(
        ...,
        title="Longitude",
        description="Query string for the weather to search based on Longitude",
    ),
) -> List[Item]:
    """
    Method to get Weather Information From Wrapper of https://www.7timer.info API provided
    latitude and longitude as parameter
    @param lat: Latitude in float
    @param lon: Longitude in float
    @return Filtered response from API in json format
    """

    # Calling model i.e data fetcher class and handling Validation Exceptions
    try:
        response = await model.get_weather_latlon(lat=latitude, lon=longitude)
    except ValidationError as e:
        return fastapi.Response(content=e.error_msg, status_code=e.status_code)

    # Getting utc timezone aware present time
    now_utc = datetime.now(pytz.utc)
    # print(now_utc.strftime("%Y%m%d%H"))

    # Getting utc timezone aware next 48 hours time from present time
    next_48_hours = now_utc + timedelta(hours=48)
    next_48_hours_utc = next_48_hours.replace(tzinfo=pytz.UTC)

    # print(next_48_hours_utc.strftime("%Y%m%d%H"))
    # Getting utc timezone aware init time from API
    init_time = datetime.strptime(response["init"], "%Y%m%d%H")
    init_time_utc = init_time.replace(tzinfo=pytz.UTC)

    # To Check Total number of records
    # total_records = len(response["dataseries"])
    # print(total_records)
    # Getting coverted integer cloud cover into percentage from API Documentation
    cloud_cover_in_percentage = {
        1: "0%-6%",
        2: "6%-19%",
        3: "19%-31%",
        4: "31%-44%",
        5: "44%-56%",
        6: "56%-69%",
        7: "69%-81%",
        8: "81%-94%",
        9: "94%-100%",
    }

    # Iterating over Json Response and filter data as required
    outputs: List[Item] = []
    start_period_utc = init_time_utc
    for data in response["dataseries"]:
        end_period = init_time_utc + timedelta(hours=int(data["timepoint"]))
        end_period_utc = end_period.replace(tzinfo=pytz.UTC)
        now_utc_int = int(now_utc.strftime("%Y%m%d%H"))
        start_period_utc_int = int(start_period_utc.strftime("%Y%m%d%H"))
        if (
            now_utc_int - start_period_utc_int
        ) < 3 and end_period_utc < next_48_hours_utc:
            outputs.append(
                Item(
                    start_period_utc=start_period_utc.strftime("%Y%m%d%H"),
                    end_period_utc=end_period_utc.strftime("%Y%m%d%H"),
                    cloud_cover=cloud_cover_in_percentage.get(
                        data["cloudcover"], "No Cloud Cover Present"
                    ),
                    temparature_in_celcius=data["temp2m"],
                )
            )
        start_period_utc = end_period_utc
    print(len(outputs))
    return outputs


@router.get("/api/7timer-postcode/", tags=["Weather Forecast"])
async def get_weather_postcode(
    postcode: str = Query(
        ...,
        title="Postcode",
        description="String for the weather to search based on Postcode ",
    )
):
    """
    Method to get Weather Information From Wrapper of https://www.7timer.info API provided
    latitude and longitude as parameter
    @param lat: Latitude in float
    @param lon: Longitude in float
    @return Filtered response from API in json format
    """
    # Using Geopy Nominatim to get Latitude and Longitude from postcode
    geolocator = Nominatim(user_agent="WeatherAPI")
    location = geolocator.geocode(postcode)
    lat, lon = location.latitude, location.longitude
    response = await get_weather_latlon(lat, lon)
    return response
