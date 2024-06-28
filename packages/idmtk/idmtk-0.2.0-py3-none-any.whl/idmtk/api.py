import requests
from exception import *


def send_post_request(url, json_data, headers=None):
    try:
        response = requests.post(url, json=json_data, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as errh:
        if errh.response.status_code == 400:
            raise PostRequestError("Bad Request Error from server.", status_code=errh.response.status_code)
        else:
            raise PostRequestError(f"HTTP Error occurred: {errh}", status_code=errh.response.status_code)
    except requests.exceptions.ConnectionError as errc:
        raise PostRequestError(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        raise PostRequestError(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        raise PostRequestError(f"Something went wrong: {err}")


def send_get_request(url, params=None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as errh:
        if errh.response.status_code == 404:
            raise GetRequestError("Resource Not Found Error from server.", status_code=errh.response.status_code)
        else:
            raise GetRequestError(f"HTTP Error occurred: {errh}", status_code=errh.response.status_code)
    except requests.exceptions.ConnectionError as errc:
        raise GetRequestError(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        raise GetRequestError(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        raise GetRequestError(f"Something went wrong: {err}")
