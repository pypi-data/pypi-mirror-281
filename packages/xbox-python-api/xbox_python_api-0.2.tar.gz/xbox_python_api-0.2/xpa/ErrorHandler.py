class XboxApiError(Exception):
    status_code = None

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class XboxApiBadRequestError(XboxApiError):
    status_code = 400


class XboxApiAuthError(XboxApiError):
    status_code = 401


class XboxApiForbiddenError(XboxApiError):
    status_code = 403


class XboxApiNotFoundError(XboxApiError):
    status_code = 404


class XboxApiRateLimitError(XboxApiError):
    status_code = 429


class XboxApiRequestError(XboxApiError):
    status_code = 500


class XboxApiServerError(XboxApiError):
    status_code = 503
