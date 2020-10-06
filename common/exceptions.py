class InitException(Exception):
    message = "Initialisation exception occurred"


class ApiException(Exception):
    DEFAULT_CODE = 500
    DEFAULT_ERROR_MESSAGE = "Unhandled Api error occurred"

    def __init__(self, message: str = DEFAULT_ERROR_MESSAGE, code=DEFAULT_CODE, *args, **kwargs):
        self.message = message
        self.code = code
        super().__init__(*args, **kwargs)
