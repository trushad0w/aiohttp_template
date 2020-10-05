class InitException(Exception):
    message = "Initialisation exception occurred"


class ApiException(Exception):
    code = 500
    message = "Unhandled Api error occurred"
