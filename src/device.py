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
