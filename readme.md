# Assignment

Described in [assignment.txt](./assignment.txt).  
Repository name purposefully vague since its publicly visible.

# Assumptions

## Only target running config

Modification of startup-config followed by a reboot requires admin access to the device. The assignment strongly suggests using an always-on sandbox which as mentioned [here](https://developer.cisco.com/docs/sandbox/getting-started/#what-is-devnet-sandbox) blocks admin access. It seems that the entire focus is on modification of the running config.

# Considerations

## Reuse open connections for nested workflows

Imagine a method call on a device object which establishes a connection to the device. Within that method there's invocation of other methods which in turn require connections to the device.
Since the outmost scope is still open and its connection is alive, we can utilise it for nested operations to avoid unnecessary establishment of new connections and handshake overhead.
That's implemented in the @with_connection attribute where we keep a reference to the connection in a private field called _connection and reuse it if its still alive.
Otherwise we make a new connection.

## Two different approaches

### 1- Pull-Edit-Push

As the name suggests:
- Fetch the entire device config.
- Modify the XML config locally.
- Replace device config by pushing onto it.

Chances of collision:
Just before pushing, should we fetch and verify that the old config is still the same? Or should we use locks in IOS?

#### Pros:
...

#### Cons:
....

### 2- Merge segments
It works as follows:
- Build an XML subtree based on the schemas.
- Edit device config by merging the subtree into it.

#### Pros:
...

#### Cons:
....

## Data structure to locally represent config
We could convert XML to other data structures e.g. Python dictionary for ease of handling within our code.
A faithful translation back and forth to completely preserve all metadata in the XML tree would require enormous amount of work and testing so I dropped the idea and kept the XML in place.

## Choice of library:

Address those mentioned in the assignment.
Which of them is based on NetConf and which based on CLI scraping?

### [paramiko](https://www.paramiko.org/)

Basic CLI screen scraper over SSH.

### [netmiko](https://pynet.twb-tech.com/blog/netmiko-python-library.html)

Built upon paramiko. Slightly improved screen scraper.

### [ncclient](https://ncclient.readthedocs.io/en/latest/)

NetConf based with XML output.

### [NAPALM](https://napalm.readthedocs.io/en/latest/)

Feature rich, multi-vendor with structured output (json).
NetConf feature seems to be experimental and unreliable according to the official website:  
" Using iosxr_netconf and a config_encoding="xml" for NAPALM configuration operations is entirely experimental. There is a very good chance XML configurations will not work properly and that only small subsections of the configuration will be configurable using merge operations.".

### [bazpy](https://pypi.org/project/bazpy/)

My little python library of handy functions and classes.

# Challenges

#### Finding a reliable source of YANG schemas:
- internet repositories:  
Needed accurate software version information from the device which in turn requires some sort of successful RPC communication with the device which needs appropriate XML structure in the first place.
- Device itself:
Querying capabilities on the device is rather straighforward. Based on the capabilities we can use common NetConf interactions to pull schemas for reference.
- Figuring out XML structure based on YANG

# Design Decisions

- Device and its subclasses represent network equipment in an object oriented way. They encapsulate all the complexity of establishing a link over network and interacting with the device. Therefore, none of those complexities leak out to the consuming code of this model.

- Reusability of the abstract class Device

- Extensibility of the hierarchy

# Baz's Todo

Baztodo: Maintain a temporarily todo list here for my next steps:

- Group tests into local, with_remote with skipIf/skipUnless decorators

- Experiment with get_config(source="running", filter=('xpath', "/interfaces/interface/name"))

- Type hinting everywhere

- Message about expected secrets in environment variables

- Secret management

- Exception handling

- Investigate async mode for ncclient.  
