# Assignment

Described in [assignment.txt](./assignment.txt).  
Repository name purposefully vague since its publicly visible.

# Assumptions

# Considerations

Look into YANG and device capabilities to form correct XML payloads.
Investigate async mode for ncclient.
Fetch config upon instantiation of a router object.
Modify the config.
Collision of configs:
Config lock in IOS!
Just before applying the new config,
fetch again and check if it still matches the old config.
Otherwise, think about ways to merge.
Should we convert XML to Python dictionary for local processing?
Provide XML filters to the API call or fetch entire config and filter locally?
Type hinting everywhere
Startup-config vs running-config

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

# Design Decisions

- Device and its subclasses represent network equipment in an object oriented way. They encapsulate all the complexity of establishing a link over network and interacting with the device. Therefore, none of those complexities leak out to the consuming code of this model.

- Reusability of the abstract class Device

- Extensibility of the hierarchy

# Further Steps

- Message about expected secrets in environment variables

- Secret management

- Exception handling
