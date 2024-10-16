# Assignment

Described in [assignment.txt](./assignment.txt).  
Repository name purposefully vague since its publicly visible.

### Assumptions

Things that aren't explicitly mentioned, naturally lead to assumtions. But it's important to clarify them.

#### Only target running config

Modification of startup-config followed by a reboot requires admin access to the device. The assignment strongly suggests using an always-on sandbox which as mentioned [here](https://developer.cisco.com/docs/sandbox/getting-started/#what-is-devnet-sandbox) blocks admin access. Our focus seems to be on modification of the running config.

#### Unique Identifiers

In my development environment the app only connects to a single Cisco virtual sandbox but an actual product may connect to numerous remote devices. The app needs to be able to tell them apart by some uniquely identifiable piece of information.  
Such identifier already exist on all of those devices and thats their URL. However, for simplicity and ease of handling, I assign numerical IDs to devices. This simplifies passing of such IDs to/from our API endpoints.
The application logic uses those IDs to look up credentials and URLs for target devices.

# Design

The app is laid out in a modular way such that all interaction with network devices and the logic to handle them is responsibility of the "engine".  
The API on the other hand is responsible for presenting functionality of the engine to the outside world via a number of endpoints.
This modular design brings about some important benefits.
To name a few:  
1- The application logic encapsulated in the engine can be taken elsewhere and reused in any other application architecture since it has no knowledge of the consuming code. It doesn't care whether it's serving a number of API endpoints or any other purpose.
2- Automated testing of the application logic can be done without all bells and whistles of an end-to-end scenario via api endpoints. This drammatically simplifies and accelerates development.
3- The API layer is so thin that there's so little to be tested in integration and/or end-to-end scenarios. Those are the most expensive tests in terms of time and complexity. It's best to minimise them.

## 1 Engine

This is where the logic of the application sits. It interacts with network equipment to collect information about their operational status, configuration, etc. and also to remotely modify their configuration.

### Two Approaches to Workflow

At the time of writing, I can think of two different approaches to remote configuration of equipment as described below.

#### 1- Pull-Edit-Push

In this approach, as the name suggests, the following steps are taken:

- Fetch the entire device config.
- Modify the XML config locally.
- Replace device config by pushing onto it.

##### Pros:  

Using a variety of performant libraries, one can quickly traverse the data structure representing the config and make changes to it while keeping the skeleton intact and hence valid. This reduces chances of invalidating the config.

##### Cons:

This increases chances of collision. There's no guarantee that the device config stays the same between our pull and push operations. We don't even know how far apart those two operations well be in time.  
In case config changes meanwhile, pushing our modified version can lead to unpredictable consequences.  
A solution to such problem could be these steps:  

1- Fetch the entire device config.  
2- Modify the XML config locally.  
3- Just before pushing, lock config on the device.  
4- Fetch the latest config again.  
5- Compare with the previously fetched config.  
6- If they agree proceed, else, resolve discrepancies.  
7- Push the config onto the device.  
8- Unlock config on the device.

This clearly involves much complexity and risk of unanticipated issues.

#### 2- Merge Segments

In this approach, the following steps are taken:

1- Obtain the schema of the configuration data structure corresponding to the target device.  
2- Based on the schema, build the required segment of the config.  
3- Send the segment to the device and ask it to merge on the remote side.

##### Pros:

This reduces complexity of the application logic since verification, validation and comparison of configs is eliminated from it. In fact the heavy lifting is done once up-front when we prepare segments of the config for different operations.
The concern of mismatch with the latest state of the device is also reduced in this approach.

##### Cons:

Requires careful preparation of config segments up-front. Those need to be validated against relevant schemas in advance. This increases the initial complexity of the project.

I chose the second approach since the limited scope of work hardly justifies all complexities of the first approach. Figuring out appropriate XML structure for the operations of this assignment should be manageable.

### Choice of library:

Python is heavily used for task automation, so unsurprisingly there are quite a few libraries in its ecosystem for this sort of task.  
They seem to belong to two general categories:  
- Those that communicate with network equipment via CLI and parse the text they retrieve in response.
- Those that connect to network equipment via NetConf with payloads of XML format.

Having a breaf look I found the following:

#### [paramiko](https://www.paramiko.org/)

Basic CLI screen scraper over SSH. A lot needs to be built on top if it to make it suitable for high level apps.

#### [netmiko](https://pynet.twb-tech.com/blog/netmiko-python-library.html)

Built upon paramiko. Slightly improved screen scraper. Still basic for our use-case.

#### [ncclient](https://ncclient.readthedocs.io/en/latest/)

NetConf based with XML output. Seems to fit the purpose.

#### [NAPALM](https://napalm.readthedocs.io/en/latest/)

Feature rich, multi-vendor with structured output in JSON format.  
Its NetConf feature seems to be experimental and unreliable according to the documentation. I quote directly from their official website:  
--- " Using iosxr_netconf and a config_encoding="xml" for NAPALM configuration operations is entirely experimental. There is a very good chance XML configurations will not work properly and that only small subsections of the configuration will be configurable using merge operations." ---.

#### [bazpy](https://pypi.org/project/bazpy/)

This is a tiny Python library of handy functions and classes. I maintain it as a personal project.

### Object Oriented Design

There's an ocean of material about advantages of the OO paradigm, although the emphasis on it seems to have been declining for quite a while.  
The gist of it is modularity such that each module represents a phenomenon (thing) in real world. This leads to a sensible separation of concerns which, if adhered to, brings many benefits.  
Here for brevity, I'll suffice to only naming some of them:
- Understandability
- Reusability
- Testability in isolation
- Overall maintainability

In this project, device and its subclasses represent network equipment. They encapsulate all the complexity of establishing a link over network and interacting with the device. Therefore, none of those complexities leak out to the consuming code of this model. All the consuming code needs to do is to provide enough information to uniquely identify the target device and the device representation takes care of everything else internally. The device model exposes an interface for interaction with the remote device. The interface consists of methods used for modification of config and retrieval of information about it.  
Network equipment have a lot in common, namely hostname, interfaces, virtual interfaces (loopbacks), their administrative status, schemas, and so on.
The abstract class Device, captures these commonalities but cannot be instaniated since it doesn't represent any real-world device.  
Further down the inheritance hierarchy we have concrete implementations of Router, Firewall, Switch, etc. Anything specific to those devices goes into their corresponding class.

### Secret Management

Although, Cisco virtual Sandboxes are shared resource and publicly available, we should treat them similarly to production environment for the purpose of this demonstration.  
The credentials that our app uses to authenticate with remote parties need to be delivered to the app via secure means.  
There are sophisticated tools for this, some of which are cloud based, but for simplicity we will focus on the delivery via environment variables.  
It is common to assign credentials to environment variables within the shell where we launch the app. This is usually achieved by .env files.  
Thats the reason we have a .env file in the source. In that file, the actual values have been replaced with placeholders.
Having access to the environment, the app can happily consume the secrets.  
For our development environment only one set of credentials is used and that is associated with device id of 0.  
However, in a production environment with many target devices, many sets of credentials may be used each of which correspond to the unique id of a target device.

### Technical Nuances

#### Data structure to locally represent config

We could convert XML to other data structures e.g. Python dictionary for ease of handling within our code.
A faithful translation back and forth to completely preserve all metadata in the XML tree would require enormous amount of work and testing so I dropped the idea and kept the XML in place.

#### Reusable Connection Establishment

All interaction with the remote device requires a connection to it in the underlying layers. This means that establishment and teardown of such connection need to take place in multiple areas of code.  
The code that takes care of the connection is implemented in the form of a context manager, associated with the "with" keyword, wrapped in a decorator called "@with_connection".  
Every method decorated with this decorator will receive a parameter called "connection" which is a handle to the underlying NcClient connection.  
After the scope of the current method is gracefully closed or disrupted for whatever reason, the context manager makes sure that the connection is dropped and resources are freed up again.

#### Reusable Connections for Nested Workflows

Imagine a method call on a device object which establishes a connection to the device. Within that method there's invocation of other methods which in turn require connections to the same device.  
Since the outmost scope is still open and its connection is alive, we can utilise it for nested operations to avoid unnecessary establishment of new connections and handshake overhead.  
That's implemented in the "@with_connection" attribute where we keep a reference to the connection in a private field called "_connection" and reuse it if its still alive.

#### Further Steps - Engine

For further development of the engine, it would be nice to:

- Loosen coupling of Device and ncclient further to be able to test Device behaviour with mocked ncclient.
- Investigate async mode for ncclient.  
- Experiment with 'XPATH' for traversal of the config structure.

### Tests

Unit vs Integration tests.
Schema discovery tests.
Skipped tests.

## 2 API

The API layer, according to best practices explained above, is so thin that it contains no application logic. But there are some aspects of it that need mentioning.

### Choice of Library

There are several well-known libraries / frameworks for building web API's in Python ecosystem namely Django, Flask, FastApi, etc.
For this project I used FastApi mainly due to these considerations:
- It requires almost no boiler-plate which makes development of a POC fast indeed
- It supports async operation contrary to Django (AFAIK) which allows for development into a much more sophisticated product
- It comes with Swagger built into it for documentation and manual testing
- It comes with Redoc built into it OpenApi documentation

### Testing

We can use any tool to hit the endpoints but why not use the toolset that come with the framework itself?  
After launching the API if we navigate to /docs in our browser, a Swagger page appears. On that page there are segments for each of the endpoints with forms and fields that help us interact with them.  
Corresponding to every interaction on that page a CURL command is also generated and shown in case one would like to take it to a shell terminal.

### Further Steps - API

For further development of the API, it would be nice to:

- Add user authentication based on Bearer, JWT, etc.
- Use behavioural testing tools e.g SpecFlow to automate end-to-end test scenarios

# Challenges

Some of the challenges that came up during development. 

## Obtaining YANG Schemas

I found two main sources of reliable YANG schemas for the device,  
namely:

### Publicly available repositories like [this](https://github.com/YangModels/yang/tree/main/vendor/cisco/xr):  

In order to pick the relevant YANG files we need accurate software version information from the device. That in turn requires some sort of successful communication with the device which needs appropriate XML structure. That requires the YANG schemas in the first place.

### Device Itself:

Being able to perform basic communication with the device we can use OpenConfig schemas to query the device for its capabilities.  
That is rather straighforward. Then, based on the capabilities we can use common NetConf interactions to download schemas from the device itself.  
Then we can either use tools like [Pyang](https://pypi.org/project/pyang/) or by manual labour build XML payloads based on the downloaded schemas.

I tooke the second approach and downloaded YANG files from the device. The functions to do that are still in the engine for future use.

## Sandbox Unresponsive

It happened sometimes that after sending a config segment to the device for merge, the device went into an unresponsive state for a long time. The coma took well above an hour in some cases.  
I suspect it had to do with the specific payloads that I sent. This slowed down the development and testing process.

## Others Changed my Sandbox

As mentioned earlier Cisco sandboxes are share resource meaning that other developers are interacting with them all the time.  
This can bring about surprises every now and then especially during testing where you realise someone else is also adding and removing loopback interfaces.

# Baztodo

A temporary todo list for my next steps:

- Group tests into local, with_remote with skipIf/skipUnless decorators

- Type hinting everywhere

- Exception handling
