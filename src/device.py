from abc import ABC
import re as Regex
from ncclient import manager as NetConfConnection
import xml.dom.minidom as XML
from src.xml_repository import XmlRepository


class Device(ABC):
    """Abstract super-class of any network device.

    Being unspecific about device type, it models their commonalities.
    e.g getting the hostname is common among them all.
    Specifics of router, firewall, switch, etc. are to be implemented
    in sub-classes.
    """

    def __init__(
        self,
        url: str,
        port: int,
        username: str,
        password: str,
    ) -> None:
        self._url = url
        self._port = port
        self._username = username
        self._password = password
        self._connection = None

    # ==========================  Properties  ==========================

    @property
    def is_connected(self) -> bool:
        if self._connection is None:
            return False
        return self._connection._session.connected

    # ==========================  Decorators  ==========================

    def with_connection(target_func):
        # baztodo: Add docstring
        def wrapper(self: "Device", *args, **kwargs):
            # Reuse connection if it's still open
            if self.is_connected:
                connection = self._connection
                return target_func(self, connection, *args, **kwargs)
            # baztodo: Exception handling here
            with NetConfConnection.connect(
                host=self._url,
                port=self._port,
                username=self._username,
                password=self._password,
                hostkey_verify=False,
                device_params={"name": "default"},
                allow_agent=False,
                look_for_keys=False,
            ) as connection:
                self._connection = connection
                return target_func(self, connection, *args, **kwargs)

        return wrapper

    # ==========================  Public Interface  ==========================

    @with_connection
    def get_hostname(self, connection: NetConfConnection) -> str:
        filter = XmlRepository.get_hostname()
        response = connection.get_config(source="running", filter=filter)
        xml_string = response.xml
        xml_tree = XML.parseString(xml_string)
        tag = xml_tree.getElementsByTagName("hostname")[0]
        return tag.firstChild.nodeValue

    @with_connection
    def add_loopback(
        self,
        connection: NetConfConnection,
        suffix: int = None,
    ) -> int:
        suffix = suffix or self.pick_unused_loopback_suffix()
        self.validate_loopback_suffix(suffix)
        config_subtree = XmlRepository.add_loopback().format(
            name=f"Loopback{suffix}",
        )
        connection.edit_config(
            target="candidate",
            config=config_subtree,
            default_operation="merge",
        )
        connection.commit()
        return suffix

    @with_connection
    def is_loopback_up(
        self,
        connection: NetConfConnection,
        suffix: int,
    ) -> bool:
        filter_subtree = XmlRepository.get_loopback_status().format(
            name=f"Loopback{suffix}",
        )
        response = connection.get(filter=filter_subtree)
        xml_string = response.xml
        xml_tree = XML.parseString(xml_string)
        tag = xml_tree.getElementsByTagName("oper-status")[0]
        text = tag.firstChild.nodeValue
        return text == "UP"

    @with_connection
    def set_loopback_status(
        self,
        connection: NetConfConnection,
        suffix: int,
        enable: bool = True,
    ) -> bool:
        status_str = "true" if enable else "false"
        config_subtree = XmlRepository.set_loopback_status().format(
            name=f"Loopback{suffix}",
            status=status_str,
        )
        connection.edit_config(
            target="candidate",
            config=config_subtree,
            default_operation="merge",
        )
        validation_res = connection.validate()
        commit_res = connection.commit()
        is_up = self.is_loopback_up(suffix)
        return is_up

    @with_connection
    def delete_loopback(
        self,
        connection: NetConfConnection,
        suffix: int,
    ) -> list[int]:
        name_to_delete = f"Loopback{suffix}"
        config_subtree = XmlRepository.delete_loopback().format(
            name=name_to_delete,
        )
        connection.edit_config(
            target="candidate",
            config=config_subtree,
            default_operation="merge",
        )
        validation_res = connection.validate()
        commit_res = connection.commit()
        return self.list_loopback_suffixes()

    @with_connection
    def list_interfaces(
        self,
        connection: NetConfConnection,
        loopback_only=True,
    ) -> list[str]:
        filter = XmlRepository.list_interfaces()
        response = connection.get_config(source="running", filter=filter)
        xml_string = response.xml
        xml_tree = XML.parseString(xml_string)
        tags = xml_tree.getElementsByTagName("interface-name")
        names = [x.firstChild.nodeValue for x in tags]
        if loopback_only:
            return [x for x in names if x.startswith("Loopback")]
        return names

    def list_loopback_suffixes(self) -> list[int]:
        names = self.list_interfaces(loopback_only=True)
        suffixes = [x.strip("Loopback") for x in names]
        suffixes = [int(x) for x in suffixes]
        return suffixes

    @with_connection
    def get_capabilities(self, connection: NetConfConnection) -> list[str]:
        return [x for x in connection.server_capabilities]

    def dump_capabilities(self) -> None:
        capabilities = self.get_capabilities()
        with open("./dump/capabilities.txt", "w") as output_file:
            for item in capabilities:
                output_file.write(f"{item}\n")

    @with_connection
    def dump_schemas(self, connection: NetConfConnection) -> None:
        capabilities = self.get_capabilities()
        models = set()
        for capability in capabilities:
            module = Regex.search("module=([^&]*)", capability)
            if module is not None:
                models.add(module.group(1))
        for model in models:
            schema = connection.get_schema(identifier=model)
            with open(f"./dump/schema/{model}.yang", "w") as dump_file:
                dump_file.write(schema.data)

    @with_connection
    def dump_config(self, connection: NetConfConnection) -> None:
        with open("./dump/config.xml", "w") as output_file:
            response = connection.get_config("running")
            output_file.write(response.xml)

    # ==========================  Private Logic  ==========================

    def validate_loopback_suffix(self, suffix: int):
        if not isinstance(suffix, int):
            raise TypeError("Loopback suffix needs to be an integer")
        if suffix <= 0:
            raise ValueError("Loopback suffix may not be less than 1")
        if suffix > 999:  # baztodo: Document arbitrary assumtion
            raise ValueError("Loopback suffix may not exceed 999")

    def pick_unused_loopback_suffix(self) -> int:
        used_suffixes = self.list_loopback_suffixes()
        suffix = self.pick_unused_number(used_suffixes)
        return suffix

    def pick_unused_number(self, used: list[int]) -> int:
        for i in range(1, 1000):
            if i not in used:
                return i
        else:
            raise RuntimeError("Couldn't pick an unused number")

    # ==========================  Test Points  ==========================

    # These are handles to the internal state of the instance to make
    # it easy to probe into it and test for state changes

    @with_connection
    def _outer_connection_getter(
        self, connection: NetConfConnection
    ) -> tuple[object, object]:
        inner_connection = self._inner_connection_getter()
        outer_connection = connection
        return [outer_connection, inner_connection]

    @with_connection
    def _inner_connection_getter(self, connection: NetConfConnection) -> object:
        return connection
