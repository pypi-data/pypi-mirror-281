from __future__ import annotations

import os
import sys
import logging
from typing import Any

from .dotenv_safe import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Load environment variables and configure the application.

    This function is the main entry point to load environment variables and configure
    the application based on the provided options. Options can be provided via
    environment variables or command-line arguments.

    Raises:
        KeyError: If required environment variables are missing.
        ValueError: If command-line arguments are invalid.
        Exception: If an error occurs during configuration.
    """
    options: dict[str, Any] = {}

    # Check for environment variable configuration
    if "DOTENV_CONFIG_EXAMPLE" in os.environ:
        options["examplePath"] = os.environ["DOTENV_CONFIG_EXAMPLE"]

    if os.environ.get("DOTENV_CONFIG_ALLOW_EMPTY_VALUES") != "false":
        options["allowEmptyValues"] = True

    # Parse command-line arguments
    for val in sys.argv:
        if val.startswith("dotenv_config_"):
            key, value = val[len("dotenv_config_") :].split("=", 1)
            options[key] = value

    # Load configuration
    try:
        config_result = config(options)
        logger.info("Configuration loaded successfully:")
        logger.info(config_result)
    except Exception as e:
        logger.error("Error loading configuration: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
