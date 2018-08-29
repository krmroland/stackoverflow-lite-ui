from werkzeug.exceptions import UnprocessableEntity, NotFound, Unauthorized


class ModelException(Exception):
    pass


class ValidationException(UnprocessableEntity):
    def __init__(self, errors):
        description = dict(message="Validation Failed", errors=errors)
        super().__init__(description=description)


class ModelNotFoundException(NotFound):
    def __init__(self, table=None, id=None):
        error = "Couldn't find a given resource"
        if table:
            error = f"Coudnot find a {table} resource with  id: {id}"

        super().__init__(description=error)


class UnauthorizedException(Unauthorized):
    def __init__(self, description):
        super().__init__(description=description)
