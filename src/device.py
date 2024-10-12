from abc import ABC
from ncclient import manager as NetConfConnection
import xml.dom.minidom as XML
from src.decorator import with_connection


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

    @with_connection
    def get_hostname(self, connection: NetConfConnection) -> str:
        response = connection.get_config("running")
        xml = XML.parseString(response.xml)
        # xml_str = xml.toxml()
        hostname_tags = xml.getElementsByTagName("hostname")
        first_occurrence = hostname_tags[0]
        return first_occurrence.firstChild.nodeValue

    @with_connection
    def dump_capabilities(self, connection: NetConfConnection) -> None:
        with open("./sample/capabilities.txt", "w") as output_file:
            for line in connection.server_capabilities:
                output_file.write(f"{line}\n")

    @with_connection
    def dump_config(self, connection: NetConfConnection) -> None:
        with open("./sample/config.xml", "w") as output_file:
            response = connection.get_config("running")
            output_file.write(response.xml)
