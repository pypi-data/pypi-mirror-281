from corehttp.runtime.policies import (
    BearerTokenCredentialPolicy,
    NetworkTraceLoggingPolicy,
)

from lseg_analytics.auth.machine_token_credential import MachineTokenCredential
from lseg_analytics_basic_client import AnalyticsAPIClient

from .config import load_config

__all__ = [
    "Client",
]


class Client:
    @classmethod
    def reload(cls):
        cls._instance = None

    def __new__(cls):
        if not getattr(cls, "_instance", None):
            cfg = load_config()
            authentication_policy = None
            if cfg.auth:
                authentication_policy = BearerTokenCredentialPolicy(
                    credential=MachineTokenCredential(
                        client_id=cfg.auth.client_id,
                        client_secret=cfg.auth.client_secret,
                        auth_endpoint=cfg.auth.token_endpoint,
                        scopes=cfg.auth.scopes,
                    ),
                    scopes=cfg.auth.scopes,
                )
            logging_policy = NetworkTraceLoggingPolicy()
            logging_policy.enable_http_logger = True
            cls._instance = AnalyticsAPIClient(
                endpoint=cfg.base_url,
                username=cfg.username,
                authentication_policy=authentication_policy,
                logging_policy=logging_policy,
            )
            if cfg.headers:
                for key, value in cfg.headers.items():
                    cls._instance._config.headers_policy.add_header(key, value)
        return cls._instance
