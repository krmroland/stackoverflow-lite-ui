class ModelException(Exception):
    pass


class ValidationException(Exception):
    def __init__(self, error):
        Exception.__init__(self, error)
        self.errors = error
