"""Uniform JSON errors. Never echo request payloads or exception messages."""
from typing import NotRequired
from flask import Flask, Response, jsonify, request
from werkzeug.exceptions import HTTPException
from .contracts.common import Wire, validate_contract

class ErrorDetail(Wire):
    code: str
    message: str
    operation: NotRequired[str]
class ErrorResponse(Wire):
    error: ErrorDetail

def api_error(code: str, message: str, status: int) -> Response:
    detail: ErrorDetail = {"code": code, "message": message}
    if request.endpoint:
        detail["operation"] = request.endpoint
    response = jsonify(validate_contract(ErrorResponse, {"error": detail}))
    response.status_code = status
    return response

def not_implemented(message: str) -> Response:
    """Return 501 for an unavailable operation, never a success-shaped payload."""
    return api_error("not_implemented", message, 501)

def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def http_error(error: HTTPException) -> Response:
        messages = {
            400: ("bad_request", "The request could not be parsed."),
            401: ("authorization_required", "Authorization is required."),
            403: ("access_denied", "Access is denied."),
            404: ("not_found", "The requested API route was not found."),
            405: ("method_not_allowed", "This HTTP method is not supported for this route."),
            409: ("state_conflict", "This operation is not available in the current record state."),
            503: ("service_unavailable", "The review provider is not configured or the local queue is full."),
            413: ("request_too_large", "The request exceeds the configured transport limits."),
            415: ("unsupported_media_type", "The request media type is not supported."),
            422: ("invalid_request", "The supplied request does not match the required schema."),
        }
        status = error.code or 500
        code, message = messages.get(status, ("http_error", "The request could not be completed."))
        response = api_error(code, message, status)
        # Preserve protocol metadata such as Allow, without replacing JSON headers.
        for name, value in error.get_headers():
            if name.lower() not in {"content-type", "content-length"}:
                response.headers[name] = value
        return response

    @app.errorhandler(Exception)
    def unexpected_error(error: Exception) -> Response:
        app.logger.error("Unhandled API exception type: %s", type(error).__name__)
        return api_error("internal_error", "An internal API error interrupted the request.", 500)
