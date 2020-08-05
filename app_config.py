# -*- coding: utf-8 -*-

"""Contains the application configurations for various deployment scenarios.
"""

import os


class BaseConfig(object):
    """Configuration base.

        This class can be used as the application configuration, or subclassed to
        add or modify the configuration attributes.

        Attributes:
            APP_NAME (str): Application name
            APP_DESCRIPTION (str): Application description
            APP_MAINTAINER (str): Application maintainer
            APP_MAINTAINER_EMAIL (str): Email address of application maintainer
            SHOW_MAINTAINER (bool): Show the maintainer in headers, logs, and errors
            APP_VERSION (str): Latest stable API version published using this application
            APP_VALID_DATE (str): Date up to which responses of the API may be trusted
            NETWORK_PORT (int): HTTP port to which the web server must bind
            LOG_LEVEL (str): Log level (e.g. INFO, DEBUG, ERROR)
            DEBUG (bool): Enables debugging mode
        """
    APP_NAME = os.environ.get('APP_NAME', 'application')
    APP_DESCRIPTION = os.environ.get('APP_DESCRIPTION', """Alliander Life cycle assessment REST API""")
    APP_MAINTAINER = os.environ.get('APP_MAINTAINER', 'OOSE-kobe')
    APP_MAINTAINER_EMAIL = os.environ.get('APP_MAINTAINER_EMAIL', 'developer.or.team.name@alliander.com')
    SHOW_MAINTAINER = os.environ.get('SHOW_MAINTAINER', False)
    APP_VERSION = os.environ.get('APP_VERSION', 'v1')
    APP_VALID_DATE = os.environ.get('APP_VALID_DATE', '2020-12-31')
    NETWORK_INTERFACE = os.environ.get('NETWORK_INTERFACE', '127.0.0.1')
    NETWORK_PORT = os.environ.get('NETWORK_PORT', 8080)
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')

    # The following two parameters determine the active config
    DEPLOYED = os.environ.get('DEPLOYED', False)
    DEBUG = os.environ.get('DEBUG', False)


class LocalConfig(BaseConfig):
    pass


class LocalDebugConfig(LocalConfig):
    DEBUG = True
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')


class DeployedConfig(BaseConfig):
    NETWORK_INTERFACE = os.environ.get('NETWORK_INTERFACE', '0.0.0.0')
    DEPLOYED = True


class DeployedDebugConfig(DeployedConfig):
    DEBUG = True
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')


_active_config = None


def get_active_config():
    """Retrieve the active configuration.

    The active configuration is based on the DEPLOYED and DEBUG
    environment variables. The active config is set once and returned
    for each subsequent call.

    Returns:
        Active configuration
    """
    global _active_config

    is_deployed = os.environ.get('DEPLOYED', False)
    is_debug = os.environ.get('DEBUG', False)

    if _active_config is None:
        if is_deployed:
            if is_debug:
                _active_config = DeployedDebugConfig
            else:
                _active_config = DeployedConfig
        else:
            if is_debug:
                _active_config = LocalDebugConfig
            else:
                _active_config = LocalConfig

    return _active_config


def get_setting(key: str):
    """Return value set for key.

    Args:
        key (str): key of configuration setting

    Returns:
        value if key exists, None otherwise
    """
    active_config = get_active_config()
    return getattr(active_config, key, None)
