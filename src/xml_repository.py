class XmlRepository:
    def get_hostname() -> str:
        return """
            <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"> 
             <system xmlns="http://openconfig.net/yang/system">
              <config>
               <hostname />
              </config>
             </system>
            </filter>
        """

    def list_interfaces() -> str:
        return """
            <filter>
              <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
                <interface-configuration>
                  <interface-name/>
                </interface-configuration>
              </interface-configurations>
            </filter>
        """

    def add_loopback() -> str:
        return """
            <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
              <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
                <interface-configuration>
                  <active>act</active>
                  <interface-name>{name}</interface-name>
                  <interface-virtual></interface-virtual>
                </interface-configuration>
              </interface-configurations>
            </config>
        """

    def get_loopback_status() -> str:
        return """
            <filter>
              <interfaces xmlns="http://openconfig.net/yang/interfaces">
                <interface>
                  <name>{name}</name>
                  <state>
                    <oper-status/>
                  </state>
                </interface>
              </interfaces>
            </filter>
        """

    def set_loopback_status() -> str:
        return """
            <config>
              <interfaces xmlns="http://openconfig.net/yang/interfaces">
                <interface>
                  <name>{name}</name>
                  <config>
                    <name>{name}</name>
                    <enabled>{status}</enabled>
                  </config>
                </interface>
              </interfaces>
            </config>
        """
