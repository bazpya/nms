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
