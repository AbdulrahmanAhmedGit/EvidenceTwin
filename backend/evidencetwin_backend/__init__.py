"""Flask factory: workspace runtime plus optional contract-only skeleton mode."""
import re
from collections.abc import Mapping
from typing import Any
from flask import Flask, Response, request
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge, Forbidden
from .config import load_config, validate_origins
from .errors import register_error_handlers

API_VERSION = "0.1.0"  # Skeleton contract version, not scientific Core version.

def create_app(config: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(__name__, static_folder=None)
    app.config.from_mapping(load_config())
    if config is not None:
        app.config.update(config)
    validate_origins(app.config["CORS_ALLOWED_ORIGINS"])
    for key in ("MAX_CONTENT_LENGTH", "MAX_FORM_MEMORY_SIZE", "MAX_FORM_PARTS"):
        if type(app.config[key]) is not int or app.config[key] <= 0:
            raise ValueError(f"{key} must be a positive integer")
    auth_hook = app.config["AUTHENTICATE_REQUEST"]
    if auth_hook is not None and not callable(auth_hook):
        raise ValueError("AUTHENTICATE_REQUEST must be a callable or None")
    register_error_handlers(app)

    from .blueprints import BLUEPRINTS
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)

    if app.config["RUNTIME_ENABLED"]:
        from .services.runtime import install_runtime
        install_runtime(app)

    @app.before_request
    def infrastructure_boundary() -> None:
        # Reject a declared oversize body before reading multipart content.
        maximum = app.config["MAX_CONTENT_LENGTH"]
        if request.content_length is not None and request.content_length > maximum:
            raise RequestEntityTooLarge()
        if request.method == "OPTIONS":
            return
        if app.config["RUNTIME_ENABLED"] and request.method in {"POST", "DELETE"}:
            origin = request.headers.get("Origin")
            allowed = {request.host_url.rstrip("/"), *app.config["CORS_ALLOWED_ORIGINS"]}
            if origin is not None and origin not in allowed:
                raise Forbidden()
        public = {"system.health", "system.capabilities"}
        if request.endpoint and request.endpoint not in public and auth_hook is not None:
            if auth_hook() is not None:
                raise TypeError("AUTHENTICATE_REQUEST must return None or raise an HTTP authorization error")

    @app.after_request
    def response_headers(response: Response) -> Response:
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    if app.config["CORS_ALLOWED_ORIGINS"]:
        CORS(app, resources={r"/api/.*": {
            "origins": [re.compile(r"\A" + re.escape(origin) + r"\Z") for origin in app.config["CORS_ALLOWED_ORIGINS"]],
            "methods": ["GET", "HEAD", "POST", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": False,
            "send_wildcard": False,
            "always_send": False,
            "vary_header": True,
        }})
    return app
