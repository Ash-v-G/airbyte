#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#


from __future__ import annotations

from datetime import datetime
from typing import Dict

_ACCESS_TOKEN = "test_access_token"
_LWA_APP_ID = "amazon_app_id"
_LWA_CLIENT_SECRET = "amazon_client_secret"
_MARKETPLACE_ID = "ATVPDKIKX0DER"
_REFRESH_TOKEN = "amazon_refresh_token"


class ConfigBuilder:
    def __init__(self) -> None:
        self._config: Dict[str, str] = {
            "refresh_token": _REFRESH_TOKEN,
            "lwa_app_id": _LWA_APP_ID,
            "lwa_client_secret": _LWA_CLIENT_SECRET,
            "replication_start_date": "2023-01-01T00:00:00Z",
            "replication_end_date": "2023-01-30T00:00:00Z",
            "aws_environment": "PRODUCTION",
            "region": "US",
            "account_type": "Seller",
        }

    def with_start_date(self, start_date: datetime) -> ConfigBuilder:
        self._config["replication_start_date"] = start_date.isoformat()[:-13] + "Z"
        return self

    def build(self) -> Dict[str, str]:
        return self._config
