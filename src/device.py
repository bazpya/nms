from abc import ABC
import re as Regex
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
        self._connection = None

    @with_connection
    def get_hostname(self, connection: NetConfConnection) -> str:
        filter = """
            <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"> 
             <system xmlns="http://openconfig.net/yang/system">
              <config>
               <hostname />
              </config>
             </system>
            </filter>
        """
        response = connection.get_config(source="running", filter=filter)
        xml = XML.parseString(response.xml)
        tag = xml.getElementsByTagName("hostname")[0]
        return tag.firstChild.nodeValue

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
        models = []
        for capability in capabilities:
            module = Regex.search("module=(.*)&", capability)
            if module is not None:
                models.append(module.groups(0)[0])
        for model in models:
            schema = connection.get_schema(identifier=model)
            with open(f"./dump/schema/{model}.yang", "w") as dump_file:
                dump_file.write(schema.data)

    @with_connection
    def dump_config(self, connection: NetConfConnection) -> None:
        with open("./dump/config.xml", "w") as output_file:
            response = connection.get_config("running")
            output_file.write(response.xml)
