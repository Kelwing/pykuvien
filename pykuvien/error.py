class MissingAuthError(Exception):
    pass


class HttpError(Exception):
    def __init__(self, message, status_code):
        super(HttpError, self).__init__(message)

        self.status_code = status_code
