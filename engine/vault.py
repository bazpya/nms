from os import getenv


class Vault:
    def __init__(self) -> None:
        self.keys = [
            "nms_device_url",
            "nms_netconf_port",
            "nms_username",
            "nms_password",
        ]
        self._values_dict = {}
        for key in self.keys:
            value = self._getEnvOrRaise(key)
            self._values_dict[key] = value

    def _getEnvOrRaise(self, key: str):
        value = getenv(key, default=None)
        if value is None:
            raise RuntimeError(f"Could not find {key} in environment variables")
        return value

    def get(self) -> dict[str, str]:
        return self._values_dict
