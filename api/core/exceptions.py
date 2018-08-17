from werkzeug.exceptions import UnprocessableEntity


class ModelException(Exception):
    pass


class ValidationException(UnprocessableEntity):
    def __init__(self, errors):
        response = dict(message="Validation Failed", errors=errors)
        super().__init__(response=response)
