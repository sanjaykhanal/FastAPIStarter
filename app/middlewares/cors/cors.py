import logging
from fastapi.middleware.cors import CORSMiddleware
from config.config import ALLOWED_ORIGINS, ALLOWED_METHODS, ALLOWED_HEADERS



def attach_cors_middleware(app):
    """attach a middleware to handle cors requests"""

    logging.info("Attaching CORS middleware to the application")
    app.add_middleware(
        CORSMiddleware,
        allow_origins = ALLOWED_ORIGINS,
        allow_credentials = True,
        allow_methods = ALLOWED_METHODS,
        allow_headers = ALLOWED_HEADERS
    )
