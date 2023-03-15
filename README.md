# Python Assignment: serving a weather API as a microservice
In Solution I used Fast API, [7Timer](https://www.7timer.info/) API and Docker to create it. <br>

# Background
In order to generate forecasts for individual customers, we use a number of features, including: day of the week, maintenance calendar, holiday 
calendar.
A feature that is conspicuously missing from our stack at the moment is weather information. One of the reasons is that B2B gas consumption is 
(almost) independent from weather conditions, and another reason is that obtaining high-quality weather information is not straightforward.
The assignment consists of providing imperfect weather information using the API of http://www.7timer.info/ through a dockerized microservice. 
This can be seen as “wrapping 7Timer API in your own API”. While the information available is probably not good enough, the output of this exercise might be a base we will iterate upon

# Objective
Using the API available in 7Timer and docker, produce a microservice which, given a point in space, returns for the next 48 hours (or at least the 
next full day) a time series with the following data per time point:
- `start_period_utc`: start of time point interval.
- `end_period_utc`: end of time point interval.
- `cloud_cover`: This is what I mean by “imperfect information”: ideally we would have “solar radiation”, but I think it is not available in the API. 
So let’s use cloud_cover as a proxy.
- `temperature`:in celcius.

The result should be a container that upon run locally, allows to access a REST API from the local browser: the input to a GET request should be 
a URL with longitude and latitude as query parameters, and the return an JSON response with the information described above.
It is important that start_period_utc and end_period_utc are returned in unambiguous UTC timezone. The time resolution of the return 
will be determined by the one of the raw data available.
For the code inside the container use FastAPI unless you believe there is a better choice.
The result can be shared either in a public git repo, or through a zip folder including all the files.
It must be reproducible on local using a simple docker or docker compose command

# Bonus Points
- Instead of longitude and latitude, use as input a Spanish postcode (for instance, 04006, 28014 or 47012).
- Somehow estimate the solar radiation from cloud_cover and/or other readily available information.

# Solution
Using the API available in 7Timer This Wrapper Dockerized REST API (microservice) 
- Give Forecast of weather for a given pair of `Latitude` and `Longitude` and also for given `postcode` of    any location.
- It will give data for next 48 hours from the time API is being consumed with below informations as response.
  - `start_period_utc`: start of time point interval.
  - `end_period_utc`: end of time point interval.
  - `cloud_cover`: Cloud Cover information from API in Percentage format.
  - `temperature`:in celcius.
All time considered is `UTC` time here.
- It also handles user input for `Latitude` and `Longitude` of more than three digits after decimal.
- Prevent Invalid Input By Validting Parameters.
- Display error message if non existent `Latitude` and `Longitude` and `postcode` provided.

### Using Docker
if you want to use Docker there are two simple steps
- `docker build -t weather_forecast .`
- `docker run -p 80:80 weather_forecast`

### Without Docker
- `clone repository`
- `cd <directory>`
- `python -m venv venv`
- `activate virtual environment ./venv/Scripts/activate.bat (For Windows)`
- `activate virtual environment source ./venv/Scripts/activate (For Linux)`
- `pip install -r requirements.txt`
- `uvicorn src.main:app --reload --host 0.0.0.0 --port 80`

After running project you can check documentation on http://localhost/docs.


#### visit http://localhost/api/7timer-latlon/?latitude=51.283&longitude=6.083 (sample endpoint)
![SampleLatLonResponse](https://user-images.githubusercontent.com/54988134/225172492-4cd548a8-339f-4918-b627-29deb47ed3fb.PNG)

#### visit http://localhost/api/7timer-postcode/?postcode=04006 (sample endpoint)
![SamplePostCodeResponse](https://user-images.githubusercontent.com/54988134/225172498-ca7db648-46d6-4d29-87a7-8cf0f5b2b14a.PNG)