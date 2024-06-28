from models import *
from config import BASE_URL
from requests import Response
from api import *


def login(username: str, password: str):
    params = AuthLogin(username=username, password=password)
    return _login(params=params)


def _login(params: AuthLogin) -> ReturnAuthLogin:
    """
    登录函数底层
    """

    url: str = f"{BASE_URL}/admin/login"
    json_data: dict = {"loginName": params.username, "password": params.password}
    headers: dict = {"Content-Type": "application/json"}
    try:
        response: Response = send_post_request(url=url, json_data=json_data, headers=headers)
        if response.status_code == 200:
            token = response.json()["token"]
            return ReturnAuthLogin(is_login_success=True, token=token)
        else:
            return ReturnAuthLogin(is_login_success=False)
    except GetRequestError as e:
        print(f"Caught exception: {e}, Status Code: {e.status_code}")
