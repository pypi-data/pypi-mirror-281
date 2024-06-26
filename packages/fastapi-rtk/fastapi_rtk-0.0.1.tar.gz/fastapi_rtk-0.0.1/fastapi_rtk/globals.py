from typing import Any, Dict

from .auth import AuthConfigurator
from .models import User


class G:
    """
    Represents the global configuration for the application.

    This global configuration is used to store the current user, OAuth clients, and other global settings.

    It also allows to override the default authentication configurator.

    Attributes:
        user (User | None): The currently authenticated user, if any.
        auth (AuthConfigurator): The authentication configurator.
        config (Dict[str, Any]): The global configuration.
    """

    user: User | None = None
    auth: AuthConfigurator = AuthConfigurator()
    config: Dict[str, Any] = {}


g = G()
