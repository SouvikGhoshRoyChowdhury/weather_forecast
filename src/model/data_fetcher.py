import json

import httpx
from httpx import Response

from src.exception.validation import ValidationError


async def get_weather_latlon(lat: float, lon: float) -> dict:
    """
    Method to get Weather Information From https://www.7timer.info API provided
    latitude and longitude as parameter
    @param lat: Latitude in float
    @param lon: Longitude in float
    @return Response from API in json format
    """

    # As per https://www.7timer.info/ API Document precise Latitude and Longitude upto three decimal point
    lat = "%.3f" % lat
    lon = "%.3f" % lon

    # API Endpoint, Default parameters are product = civil and output = json
    url = f"https://www.7timer.info/bin/api.pl?lon={float(lon)})&lat={float(lat)}&product=civil&output=json"

    # Making request using Asynchronus Client to speed the process
    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url, follow_redirects=True)
        print(resp.is_redirect)
        if resp.text == "ERR: invalid coordinate" or resp.text == "":
            raise ValidationError(resp.content, status_code=resp.status_code)
    data = resp.json()
    return data
