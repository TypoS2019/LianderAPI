#!/usr/bin/env python
# -*- coding: utf-8 -*-
import structlog
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from app.core.initializers.error_handling import initialize_error_handling
from app.core.initializers.logging import initialize_logging
from app.core.initializers.validation import initialize_validation_middleware
# Enable logging
from app_config import get_setting
initialize_logging()
logger = structlog.get_logger(__name__)
import uvicorn
from fastapi import FastAPI
from app.core.initializers.headers import initialize_metadata_header_middleware
from app.core.initializers.mounting import mount_api_version
from app.core.initializers.monitoring import initialize_prometheus_middleware
from app.versions.v1 import app as v1

# Create and configure new application instance
app = FastAPI()

initialize_error_handling(app)
initialize_metadata_header_middleware(app)
initialize_validation_middleware(app)
initialize_prometheus_middleware(app)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Activate enabled API versions
mount_api_version(app, v1)


# Redirect users to the docs
@app.get('/')
def redirect_to_docs():
    redirect_url = '/api/v1/sample/docs'  # replace with docs URL or use app.url_path_for()
    return RedirectResponse(url=redirect_url)


if __name__ == '__main__':
    # Run the application
    uvicorn.run(app, host=get_setting('NETWORK_INTERFACE'), port=get_setting('NETWORK_PORT'))
