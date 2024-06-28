class PostRequestError(Exception):
    def __init__(self, message="POST request error occurred.", status_code=None):
        super().__init__(message)
        self.status_code = status_code


class GetRequestError(Exception):
    def __init__(self, message="GET request error occurred.", status_code=None):
        super().__init__(message)
        self.status_code = status_code
