import requests


def get_weather_data(location):
    """

    :param location:
    :return:
    """
    api_url = f"https://063qqrtqth.execute-api.eu-west-2.amazonaws.com/v1/weather?location={location}"
    #TODO complete this method and docstrings
