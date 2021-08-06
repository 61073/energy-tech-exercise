import requests


def get_weather_degree_days(location):
    """
    Performs a GET request for the Weather API with a specified location, then returns the 'degreeDays' as an integer

    Params:
        location(str): The location given to search the Weather API, must in format expected by API

    Returns:
        num_degree_days(int): Number of degree days returned from the Weather API for the specified location
    """
    api_url = f"https://063qqrtqth.execute-api.eu-west-2.amazonaws.com/v1/weather?location={location}"
    x_api_key = "f661f74e-20a7-4e9f-acfc-041cfb846505"
    response = requests.get(api_url, headers={"x-api-key": x_api_key})
    json_response = response.json()
    response_location = json_response.get("location")
    if response_location:
        try:
            degree_days = response_location.get("degreeDays")
        except Exception:
            raise Exception("degreeDays not found in Weather API location response")
        if degree_days:
            try:
                num_degree_days = int(degree_days)
                return num_degree_days
            except ValueError:
                raise Exception("degreeDays value returned from API could not converted to integer")
        else:
            raise Exception("degreeDays not found in Weather API location response")
    else:
        raise Exception("location not found in Weather API response")
