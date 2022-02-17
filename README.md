<h1 align="center">
  <br>
  <br>
  Seq-Statck-Reaction
  <br>
</h1>

<h4 align="center">A software for "Bayesian sequential stacking algorithm for concurrently designing molecules and syntheticreaction networks".</h4>

---

## Table of contents[![](./docs/img/pin.svg)](#table-of-contents)
1. [Motivation](#motivation)
2. [More than embedded](#more-than-embedded)
3. [Composition](#composition)
4. [Software build](#software-build)
5. [Software integration](#software-integration)
   - [Multicast router](#mulitcast-router)
   - [Logging service](#logging-service)
   - [Development](#development)
6. [Use cases and benefits](#use-cases-and-benefits)
   - [Distributes solutions](#distributed-solution)
   - [Driverless devices](#driverless-devices)
   - [Real-time solutions](#real-time-solutions)
   - [Digital twin](#digital-twin)
   - [Simulation and test automations](#simulation-and-test-automations)
7. [Examples](#examples)
8. [Licensing](#licensing)
9. [Call for action](#call-for-action)

---

## Motivation[![](./docs/img/pin.svg)](#motivation)

Traditionally, devices are connected clients to stream data to the cloud or fog servers for further processing.
<br><br><a href="/docs/img/mist-network.png"><img src="/docs/img/mist-network.png" alt="IoT-to-Cloud (Nebula) network" style="width:70%;height:70%"/></a><br><br>
Since data is generated and collected at the edge of the network (mist network), it makes sense to change the role of connected Things and provide network accessible (_Public_) services directly on devices. This extends _Cloud_ to the extreme edge and it is a good foothold for robust solutions such as:
* _Increase data privacy_, which is an important factor for sensitive data.
* _Decrease data streaming_, which is a fundamental condition to optimize network communication.
* Develop _autonomous, intelligent and self-aware devices_ by providing network services directly in the environment of data origin.

---
