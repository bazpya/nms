from os import getenv


class CredVault:
    """Responsible for delivering secret credentials to the application logic at runtime.

    It takes those values from environment variables of the shell in which the app is launched.
    Those are exported from the .env file in the project root.
    This Vault is meant to hold a dictionary where the key is unique ID of a device
    and the value is a set of credentials specific to that device.
    In dev environment the ID of 0 is populated for dev-testing purposes.
    """

    def __init__(self) -> None:
        test_values: dict[str, str] = {}
        test_values["url"] = self._getEnvOrRaise("nms_device_url")
        test_values["port"] = self._getEnvOrRaise("nms_netconf_port")
        test_values["username"] = self._getEnvOrRaise("nms_username")
        test_values["password"] = self._getEnvOrRaise("nms_password")

        self._data: dict[int, dict] = {}
        dummy_device_id = 0
        self._data[dummy_device_id] = test_values

    def _getEnvOrRaise(self, key: str):
        value = getenv(key, default=None)
        if value is None:
            raise RuntimeError(f"Could not find {key} in environment variables")
        return value

    def get(self, id: int) -> dict[str, str]:
        creds = self._data.get(id, None)
        if creds is None:
            raise RuntimeError(f"No credentials found for device id of {id}")
        return creds
