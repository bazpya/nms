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
              <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"/>
            </filter>
        """
