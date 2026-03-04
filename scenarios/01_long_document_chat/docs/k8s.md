---
linktitle: Kubernetes Documentation
title: Documentation
sitemap:
  priority: 1.0
---

---

title: Concepts
main_menu: true
content_type: concept
weight: 40

---

<!-- overview -->

The Concepts section helps you learn about the parts of the Kubernetes system and the abstractions Kubernetes uses to represent your {{< glossary_tooltip text="cluster" term_id="cluster" length="all" >}}, and helps you obtain a deeper understanding of how Kubernetes works.

## <!-- body -->

title: "Cluster Architecture"
weight: 30
description: >
The architectural concepts behind Kubernetes.

---

A Kubernetes cluster consists of a control plane plus a set of worker machines, called nodes,
that run containerized applications. Every cluster needs at least one worker node in order to run Pods.

The worker node(s) host the Pods that are the components of the application workload.
The control plane manages the worker nodes and the Pods in the cluster. In production
environments, the control plane usually runs across multiple computers and a cluster
usually runs multiple nodes, providing fault-tolerance and high availability.

This document outlines the various components you need to have for a complete and working Kubernetes cluster.

{{< figure src="/images/docs/kubernetes-cluster-architecture.svg" alt="The control plane (kube-apiserver, etcd, kube-controller-manager, kube-scheduler) and several nodes. Each node is running a kubelet and kube-proxy." caption="Figure 1. Kubernetes cluster components." class="diagram-large" >}}

{{< details summary="About this architecture" >}}
The diagram in Figure 1 presents an example reference architecture for a Kubernetes cluster.
The actual distribution of components can vary based on specific cluster setups and requirements.

In the diagram, each node runs the [`kube-proxy`](#kube-proxy) component. You need a
network proxy component on each node to ensure that the
{{< glossary_tooltip text="Service" term_id="service">}} API and associated behaviors
are available on your cluster network. However, some network plugins provide their own,
third party implementation of proxying. When you use that kind of network plugin,
the node does not need to run `kube-proxy`.
{{< /details >}}

## Control plane components

The control plane's components make global decisions about the cluster (for example, scheduling),
as well as detecting and responding to cluster events (for example, starting up a new
{{< glossary_tooltip text="pod" term_id="pod">}} when a Deployment's
`{{< glossary_tooltip text="replicas" term_id="replica" >}}` field is unsatisfied).

Control plane components can be run on any machine in the cluster. However, for simplicity, setup scripts
typically start all control plane components on the same machine, and do not run user containers on this machine.
See [Creating Highly Available clusters with kubeadm](/docs/setup/production-environment/tools/kubeadm/high-availability/)
for an example control plane setup that runs across multiple machines.

### kube-apiserver

{{< glossary_definition term_id="kube-apiserver" length="all" >}}

### etcd

{{< glossary_definition term_id="etcd" length="all" >}}

### kube-scheduler

{{< glossary_definition term_id="kube-scheduler" length="all" >}}

### kube-controller-manager

{{< glossary_definition term_id="kube-controller-manager" length="all" >}}

There are many different types of controllers. Some examples of them are:

- Node controller: Responsible for noticing and responding when nodes go down.
- Job controller: Watches for Job objects that represent one-off tasks, then creates Pods to run those tasks to completion.
- EndpointSlice controller: Populates EndpointSlice objects (to provide a link between Services and Pods).
- ServiceAccount controller: Create default ServiceAccounts for new namespaces.

The above is not an exhaustive list.

### cloud-controller-manager

{{< glossary_definition term_id="cloud-controller-manager" length="short" >}}

The cloud-controller-manager only runs controllers that are specific to your cloud provider.
If you are running Kubernetes on your own premises, or in a learning environment inside your
own PC, the cluster does not have a cloud controller manager.

As with the kube-controller-manager, the cloud-controller-manager combines several logically
independent control loops into a single binary that you run as a single process. You can scale
horizontally (run more than one copy) to improve performance or to help tolerate failures.

The following controllers can have cloud provider dependencies:

- Node controller: For checking the cloud provider to determine if a node has been
  deleted in the cloud after it stops responding
- Route controller: For setting up routes in the underlying cloud infrastructure
- Service controller: For creating, updating and deleting cloud provider load balancers

---

## Node components

Node components run on every node, maintaining running pods and providing the Kubernetes runtime environment.

### kubelet

{{< glossary_definition term_id="kubelet" length="all" >}}

### kube-proxy (optional) {#kube-proxy}

{{< glossary_definition term_id="kube-proxy" length="all" >}}
If you use a [network plugin](#network-plugins) that implements packet forwarding for Services
by itself, and providing equivalent behavior to kube-proxy, then you do not need to run
kube-proxy on the nodes in your cluster.

### Container runtime

{{< glossary_definition term_id="container-runtime" length="all" >}}

## Addons

Addons use Kubernetes resources ({{< glossary_tooltip term_id="daemonset" >}},
{{< glossary_tooltip term_id="deployment" >}}, etc) to implement cluster features.
Because these are providing cluster-level features, namespaced resources for
addons belong within the `kube-system` namespace.

Selected addons are described below; for an extended list of available addons,
please see [Addons](/docs/concepts/cluster-administration/addons/).

### DNS

While the other addons are not strictly required, all Kubernetes clusters should have
[cluster DNS](/docs/concepts/services-networking/dns-pod-service/), as many examples rely on it.

Cluster DNS is a DNS server, in addition to the other DNS server(s) in your environment,
which serves DNS records for Kubernetes services.

Containers started by Kubernetes automatically include this DNS server in their DNS searches.

### Web UI (Dashboard)

[Dashboard](/docs/tasks/access-application-cluster/web-ui-dashboard/) is a general purpose,
web-based UI for Kubernetes clusters. It allows users to manage and troubleshoot applications
running in the cluster, as well as the cluster itself.

### Container resource monitoring

[Container Resource Monitoring](/docs/tasks/debug/debug-cluster/resource-usage-monitoring/)
records generic time-series metrics about containers in a central database, and provides a UI for browsing that data.

### Cluster-level Logging

A [cluster-level logging](/docs/concepts/cluster-administration/logging/) mechanism is responsible
for saving container logs to a central log store with a search/browsing interface.

### Network plugins

[Network plugins](/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins)
are software components that implement the container network interface (CNI) specification.
They are responsible for allocating IP addresses to pods and enabling them to communicate
with each other within the cluster.

## Architecture variations

While the core components of Kubernetes remain consistent, the way they are deployed and
managed can vary. Understanding these variations is crucial for designing and maintaining
Kubernetes clusters that meet specific operational needs.

### Control plane deployment options

The control plane components can be deployed in several ways:

Traditional deployment
: Control plane components run directly on dedicated machines or VMs, often managed as systemd services.

Static Pods
: Control plane components are deployed as static Pods, managed by the kubelet on specific nodes.
This is a common approach used by tools like kubeadm.

Self-hosted
: The control plane runs as Pods within the Kubernetes cluster itself, managed by Deployments
and StatefulSets or other Kubernetes primitives.

Managed Kubernetes services
: Cloud providers often abstract away the control plane, managing its components as part of their service offering.

### Workload placement considerations

The placement of workloads, including the control plane components, can vary based on cluster size,
performance requirements, and operational policies:

- In smaller or development clusters, control plane components and user workloads might run on the same nodes.
- Larger production clusters often dedicate specific nodes to control plane components,
  separating them from user workloads.
- Some organizations run critical add-ons or monitoring tools on control plane nodes.

### Cluster management tools

Tools like kubeadm, kops, and Kubespray offer different approaches to deploying and managing clusters,
each with its own method of component layout and management.

### Customization and extensibility

Kubernetes architecture allows for significant customization:

- Custom schedulers can be deployed to work alongside the default Kubernetes scheduler or to replace it entirely.
- API servers can be extended with CustomResourceDefinitions and API Aggregation.
- Cloud providers can integrate deeply with Kubernetes using the cloud-controller-manager.

The flexibility of Kubernetes architecture allows organizations to tailor their clusters to specific needs,
balancing factors such as operational complexity, performance, and management overhead.

## {{% heading "whatsnext" %}}

Learn more about the following:

- [Nodes](/docs/concepts/architecture/nodes/) and
  [their communication](/docs/concepts/architecture/control-plane-node-communication/)
  with the control plane.
- Kubernetes [controllers](/docs/concepts/architecture/controller/).
- [kube-scheduler](/docs/concepts/scheduling-eviction/kube-scheduler/) which is the default scheduler for Kubernetes.
- Etcd's official [documentation](https://etcd.io/docs/).
- Several [container runtimes](/docs/setup/production-environment/container-runtimes/) in Kubernetes.
- Integrating with cloud providers using [cloud-controller-manager](/docs/concepts/architecture/cloud-controller/).
- [kubectl](/docs/reference/generated/kubectl/kubectl-commands) commands.

---

title: About cgroup v2
content_type: concept
weight: 50

---

<!-- overview -->

On Linux, {{< glossary_tooltip text="control groups" term_id="cgroup" >}}
constrain resources that are allocated to processes.

The {{< glossary_tooltip text="kubelet" term_id="kubelet" >}} and the
underlying container runtime need to interface with cgroups to enforce
[resource management for pods and containers](/docs/concepts/configuration/manage-resources-containers/) which
includes cpu/memory requests and limits for containerized workloads.

There are two versions of cgroups in Linux: cgroup v1 and cgroup v2. cgroup v2 is
the new generation of the `cgroup` API.

<!-- body -->

## What is cgroup v2? {#cgroup-v2}

{{< feature-state for_k8s_version="v1.25" state="stable" >}}

cgroup v2 is the next version of the Linux `cgroup` API. cgroup v2 provides a
unified control system with enhanced resource management
capabilities.

cgroup v2 offers several improvements over cgroup v1, such as the following:

- Single unified hierarchy design in API
- Safer sub-tree delegation to containers
- Newer features like [Pressure Stall Information](https://www.kernel.org/doc/html/latest/accounting/psi.html)
- Enhanced resource allocation management and isolation across multiple resources
  - Unified accounting for different types of memory allocations (network memory, kernel memory, etc)
  - Accounting for non-immediate resource changes such as page cache write backs

Some Kubernetes features exclusively use cgroup v2 for enhanced resource
management and isolation. For example, the
[MemoryQoS](/docs/concepts/workloads/pods/pod-qos/#memory-qos-with-cgroup-v2) feature improves memory QoS
and relies on cgroup v2 primitives.

## Using cgroup v2 {#using-cgroupv2}

The recommended way to use cgroup v2 is to use a Linux distribution that
enables and uses cgroup v2 by default.

To check if your distribution uses cgroup v2, refer to [Identify cgroup version on Linux nodes](#check-cgroup-version).

### Requirements

cgroup v2 has the following requirements:

- OS distribution enables cgroup v2
- Linux Kernel version is 5.8 or later
- Container runtime supports cgroup v2. For example:
  - [containerd](https://containerd.io/) v1.4 and later
  - [cri-o](https://cri-o.io/) v1.20 and later
- The kubelet and the container runtime are configured to use the [systemd cgroup driver](/docs/setup/production-environment/container-runtimes#systemd-cgroup-driver)

### Linux Distribution cgroup v2 support

For a list of Linux distributions that use cgroup v2, refer to the [cgroup v2 documentation](https://github.com/opencontainers/runc/blob/main/docs/cgroup-v2.md)

<!-- the list should be kept in sync with https://github.com/opencontainers/runc/blob/main/docs/cgroup-v2.md -->

- Container Optimized OS (since M97)
- Ubuntu (since 21.10, 22.04+ recommended)
- Debian GNU/Linux (since Debian 11 bullseye)
- Fedora (since 31)
- Arch Linux (since April 2021)
- RHEL and RHEL-like distributions (since 9)

To check if your distribution is using cgroup v2, refer to your distribution's
documentation or follow the instructions in [Identify the cgroup version on Linux nodes](#check-cgroup-version).

You can also enable cgroup v2 manually on your Linux distribution by modifying
the kernel cmdline boot arguments. If your distribution uses GRUB,
`systemd.unified_cgroup_hierarchy=1` should be added in `GRUB_CMDLINE_LINUX`
under `/etc/default/grub`, followed by `sudo update-grub`. However, the
recommended approach is to use a distribution that already enables cgroup v2 by
default.

### Migrating to cgroup v2 {#migrating-cgroupv2}

To migrate to cgroup v2, ensure that you meet the [requirements](#requirements), then upgrade
to a kernel version that enables cgroup v2 by default.

The kubelet automatically detects that the OS is running on cgroup v2 and
performs accordingly with no additional configuration required.

There should not be any noticeable difference in the user experience when
switching to cgroup v2, unless users are accessing the cgroup file system
directly, either on the node or from within the containers.

cgroup v2 uses a different API than cgroup v1, so if there are any
applications that directly access the cgroup file system, they need to be
updated to newer versions that support cgroup v2. For example:

- Some third-party monitoring and security agents may depend on the cgroup filesystem.
  Update these agents to versions that support cgroup v2.
- If you run [cAdvisor](https://github.com/google/cadvisor) as a stand-alone
  DaemonSet for monitoring pods and containers, update it to v0.43.0 or later.
- If you deploy Java applications, prefer to use versions which fully support cgroup v2:
  - [OpenJDK / HotSpot](https://bugs.openjdk.org/browse/JDK-8230305): jdk8u372, 11.0.16, 15 and later
  - [IBM Semeru Runtimes](https://www.ibm.com/support/pages/apar/IJ46681): 8.0.382.0, 11.0.20.0, 17.0.8.0, and later
  - [IBM Java](https://www.ibm.com/support/pages/apar/IJ46681): 8.0.8.6 and later
- If you are using the [uber-go/automaxprocs](https://github.com/uber-go/automaxprocs) package, make sure
  the version you use is v1.5.1 or higher.

## Identify the cgroup version on Linux Nodes {#check-cgroup-version}

The cgroup version depends on the Linux distribution being used and the
default cgroup version configured on the OS. To check which cgroup version your
distribution uses, run the `stat -fc %T /sys/fs/cgroup/` command on
the node:

```shell
stat -fc %T /sys/fs/cgroup/
```

For cgroup v2, the output is `cgroup2fs`.

For cgroup v1, the output is `tmpfs.`

## Deprecation of cgroup v1

{{< feature-state for_k8s_version="v1.35" state="deprecated" >}}

Kubernetes has deprecated cgroup v1.
Removal will follow [Kubernetes deprecation policy](/docs/reference/using-api/deprecation-policy/).

Kubelet will no longer start on a cgroup v1 node by default.
To disable this setting a cluster admin should set `failCgroupV1` to false in the [kubelet configuration file](/docs/tasks/administer-cluster/kubelet-config-file/).

## {{% heading "whatsnext" %}}

- Learn more about [cgroups](https://man7.org/linux/man-pages/man7/cgroups.7.html)
- Learn more about [container runtime](/docs/concepts/architecture/cri)
- Learn more about [cgroup drivers](/docs/setup/production-environment/container-runtimes#cgroup-drivers)

---

title: Cloud Controller Manager
content_type: concept
weight: 40

---

<!-- overview -->

{{< feature-state state="beta" for_k8s_version="v1.11" >}}

Cloud infrastructure technologies let you run Kubernetes on public, private, and hybrid clouds.
Kubernetes believes in automated, API-driven infrastructure without tight coupling between
components.

{{< glossary_definition term_id="cloud-controller-manager" length="all" prepend="The cloud-controller-manager is">}}

The cloud-controller-manager is structured using a plugin
mechanism that allows different cloud providers to integrate their platforms with Kubernetes.

<!-- body -->

## Design

![Kubernetes components](/images/docs/components-of-kubernetes.svg)

The cloud controller manager runs in the control plane as a replicated set of processes
(usually, these are containers in Pods). Each cloud-controller-manager implements
multiple {{< glossary_tooltip text="controllers" term_id="controller" >}} in a single
process.

{{< note >}}
You can also run the cloud controller manager as a Kubernetes
{{< glossary_tooltip text="addon" term_id="addons" >}} rather than as part
of the control plane.
{{< /note >}}

## Cloud controller manager functions {#functions-of-the-ccm}

The controllers inside the cloud controller manager include:

### Node controller

The node controller is responsible for updating {{< glossary_tooltip text="Node" term_id="node" >}} objects
when new servers are created in your cloud infrastructure. The node controller obtains information about the
hosts running inside your tenancy with the cloud provider. The node controller performs the following functions:

1. Update a Node object with the corresponding server's unique identifier obtained from the cloud provider API.
1. Annotating and labelling the Node object with cloud-specific information, such as the region the node
   is deployed into and the resources (CPU, memory, etc) that it has available.
1. Obtain the node's hostname and network addresses.
1. Verifying the node's health. In case a node becomes unresponsive, this controller checks with
   your cloud provider's API to see if the server has been deactivated / deleted / terminated.
   If the node has been deleted from the cloud, the controller deletes the Node object from your Kubernetes
   cluster.

Some cloud provider implementations split this into a node controller and a separate node
lifecycle controller.

### Route controller

The route controller is responsible for configuring routes in the cloud
appropriately so that containers on different nodes in your Kubernetes
cluster can communicate with each other.

Depending on the cloud provider, the route controller might also allocate blocks
of IP addresses for the Pod network.

### Service controller

{{< glossary_tooltip text="Services" term_id="service" >}} integrate with cloud
infrastructure components such as managed load balancers, IP addresses, network
packet filtering, and target health checking. The service controller interacts with your
cloud provider's APIs to set up load balancers and other infrastructure components
when you declare a Service resource that requires them.

## Authorization

This section breaks down the access that the cloud controller manager requires
on various API objects, in order to perform its operations.

### Node controller {#authorization-node-controller}

The Node controller only works with Node objects. It requires full access
to read and modify Node objects.

`v1/Node`:

- get
- list
- create
- update
- patch
- watch
- delete

### Route controller {#authorization-route-controller}

The route controller listens to Node object creation and configures
routes appropriately. It requires Get access to Node objects.

`v1/Node`:

- get

### Service controller {#authorization-service-controller}

The service controller watches for Service object **create**, **update** and **delete** events and then
configures load balancers for those Services appropriately.

To access Services, it requires **list**, and **watch** access. To update Services, it requires
**patch** and **update** access to the `status` subresource.

`v1/Service`:

- list
- get
- watch
- patch
- update

### Others {#authorization-miscellaneous}

The implementation of the core of the cloud controller manager requires access to create Event
objects, and to ensure secure operation, it requires access to create ServiceAccounts.

`v1/Event`:

- create
- patch
- update

`v1/ServiceAccount`:

- create

The {{< glossary_tooltip term_id="rbac" text="RBAC" >}} ClusterRole for the cloud
controller manager looks like:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cloud-controller-manager
rules:
  - apiGroups:
      - ""
    resources:
      - events
    verbs:
      - create
      - patch
      - update
  - apiGroups:
      - ""
    resources:
      - nodes
    verbs:
      - "*"
  - apiGroups:
      - ""
    resources:
      - nodes/status
    verbs:
      - patch
  - apiGroups:
      - ""
    resources:
      - services
    verbs:
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - services/status
    verbs:
      - patch
      - update
  - apiGroups:
      - ""
    resources:
      - serviceaccounts
    verbs:
      - create
  - apiGroups:
      - ""
    resources:
      - persistentvolumes
    verbs:
      - get
      - list
      - update
      - watch
```

## {{% heading "whatsnext" %}}

- [Cloud Controller Manager Administration](/docs/tasks/administer-cluster/running-cloud-controller/#cloud-controller-manager)
  has instructions on running and managing the cloud controller manager.

- To upgrade a HA control plane to use the cloud controller manager, see
  [Migrate Replicated Control Plane To Use Cloud Controller Manager](/docs/tasks/administer-cluster/controller-manager-leader-migration/).

- Want to know how to implement your own cloud controller manager, or extend an existing project?

  - The cloud controller manager uses Go interfaces, specifically, `CloudProvider` interface defined in
    [`cloud.go`](https://github.com/kubernetes/cloud-provider/blob/release-1.21/cloud.go#L42-L69)
    from [kubernetes/cloud-provider](https://github.com/kubernetes/cloud-provider) to allow
    implementations from any cloud to be plugged in.
  - The implementation of the shared controllers highlighted in this document (Node, Route, and Service),
    and some scaffolding along with the shared cloudprovider interface, is part of the Kubernetes core.
    Implementations specific to cloud providers are outside the core of Kubernetes and implement
    the `CloudProvider` interface.
  - For more information about developing plugins,
    see [Developing Cloud Controller Manager](/docs/tasks/administer-cluster/developing-cloud-controller-manager/).---
    reviewers:

* dchen1107
* liggitt
  title: Communication between Nodes and the Control Plane
  content_type: concept
  weight: 20
  aliases:
* master-node-communication

---

<!-- overview -->

This document catalogs the communication paths between the {{< glossary_tooltip term_id="kube-apiserver" text="API server" >}}
and the Kubernetes {{< glossary_tooltip text="cluster" term_id="cluster" length="all" >}}.
The intent is to allow users to customize their installation to harden the network configuration
such that the cluster can be run on an untrusted network (or on fully public IPs on a cloud
provider).

<!-- body -->

## Node to Control Plane

Kubernetes has a "hub-and-spoke" API pattern. All API usage from nodes (or the pods they run)
terminates at the API server. None of the other control plane components are designed to expose
remote services. The API server is configured to listen for remote connections on a secure HTTPS
port (typically 443) with one or more forms of client
[authentication](/docs/reference/access-authn-authz/authentication/) enabled.
One or more forms of [authorization](/docs/reference/access-authn-authz/authorization/) should be
enabled, especially if [anonymous requests](/docs/reference/access-authn-authz/authentication/#anonymous-requests)
or [service account tokens](/docs/reference/access-authn-authz/authentication/#service-account-tokens)
are allowed.

Nodes should be provisioned with the public root {{< glossary_tooltip text="certificate" term_id="certificate" >}} for the cluster such that they can
connect securely to the API server along with valid client credentials. A good approach is that the
client credentials provided to the kubelet are in the form of a client certificate. See
[kubelet TLS bootstrapping](/docs/reference/access-authn-authz/kubelet-tls-bootstrapping/)
for automated provisioning of kubelet client certificates.

{{< glossary_tooltip text="Pods" term_id="pod" >}} that wish to connect to the API server can do so securely by leveraging a service account so
that Kubernetes will automatically inject the public root certificate and a valid bearer token
into the pod when it is instantiated.
The `kubernetes` service (in `default` namespace) is configured with a virtual IP address that is
redirected (via `{{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}}`) to the HTTPS endpoint on the API server.

The control plane components also communicate with the API server over the secure port.

As a result, the default operating mode for connections from the nodes and pod running on the
nodes to the control plane is secured by default and can run over untrusted and/or public
networks.

## Control plane to node

There are two primary communication paths from the control plane (the API server) to the nodes.
The first is from the API server to the {{< glossary_tooltip text="kubelet" term_id="kubelet" >}} process which runs on each node in the cluster.
The second is from the API server to any node, pod, or service through the API server's _proxy_
functionality.

### API server to kubelet

The connections from the API server to the kubelet are used for:

- Fetching logs for pods.
- Attaching (usually through `kubectl`) to running pods.
- Providing the kubelet's port-forwarding functionality.

These connections terminate at the kubelet's HTTPS endpoint. By default, the API server does not
verify the kubelet's serving certificate, which makes the connection subject to man-in-the-middle
attacks and **unsafe** to run over untrusted and/or public networks.

To verify this connection, use the `--kubelet-certificate-authority` flag to provide the API
server with a root certificate bundle to use to verify the kubelet's serving certificate.

If that is not possible, use [SSH tunneling](#ssh-tunnels) between the API server and kubelet if
required to avoid connecting over an
untrusted or public network.

Finally, [Kubelet authentication and/or authorization](/docs/reference/access-authn-authz/kubelet-authn-authz/)
should be enabled to secure the kubelet API.

### API server to nodes, pods, and services

The connections from the API server to a node, pod, or service default to plain HTTP connections
and are therefore neither authenticated nor encrypted. They can be run over a secure HTTPS
connection by prefixing `https:` to the node, pod, or service name in the API URL, but they will
not validate the certificate provided by the HTTPS endpoint nor provide client credentials. So
while the connection will be encrypted, it will not provide any guarantees of integrity. These
connections **are not currently safe** to run over untrusted or public networks.

### SSH tunnels

Kubernetes supports [SSH tunnels](https://www.ssh.com/academy/ssh/tunneling) to protect the control plane to nodes communication paths. In this
configuration, the API server initiates an SSH tunnel to each node in the cluster (connecting to
the SSH server listening on port 22) and passes all traffic destined for a kubelet, node, pod, or
service through the tunnel.
This tunnel ensures that the traffic is not exposed outside of the network in which the nodes are
running.

{{< note >}}
SSH tunnels are currently deprecated, so you shouldn't opt to use them unless you know what you
are doing. The [Konnectivity service](#konnectivity-service) is a replacement for this
communication channel.
{{< /note >}}

### Konnectivity service

{{< feature-state for_k8s_version="v1.18" state="beta" >}}

As a replacement to the SSH tunnels, the Konnectivity service provides TCP level proxy for the
control plane to cluster communication. The Konnectivity service consists of two parts: the
Konnectivity server in the control plane network and the Konnectivity agents in the nodes network.
The Konnectivity agents initiate connections to the Konnectivity server and maintain the network
connections.
After enabling the Konnectivity service, all control plane to nodes traffic goes through these
connections.

Follow the [Konnectivity service task](/docs/tasks/extend-kubernetes/setup-konnectivity/) to set
up the Konnectivity service in your cluster.

## {{% heading "whatsnext" %}}

- Read about the [Kubernetes control plane components](/docs/concepts/architecture/#control-plane-components)
- Learn more about [Hubs and Spoke model](https://book.kubebuilder.io/multiversion-tutorial/conversion-concepts.html#hubs-spokes-and-other-wheel-metaphors)
- Learn how to [Secure a Cluster](/docs/tasks/administer-cluster/securing-a-cluster/)
- Learn more about the [Kubernetes API](/docs/concepts/overview/kubernetes-api/)
- [Set up Konnectivity service](/docs/tasks/extend-kubernetes/setup-konnectivity/)
- [Use Port Forwarding to Access Applications in a Cluster](/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)
- Learn how to [Fetch logs for Pods](/docs/tasks/debug/debug-application/debug-running-pod/#examine-pod-logs), [use kubectl port-forward](/docs/tasks/access-application-cluster/port-forward-access-application-cluster/#forward-a-local-port-to-a-port-on-the-pod)---
  title: Controllers
  content_type: concept
  weight: 30

---

<!-- overview -->

In robotics and automation, a _control loop_ is
a non-terminating loop that regulates the state of a system.

Here is one example of a control loop: a thermostat in a room.

When you set the temperature, that's telling the thermostat
about your _desired state_. The actual room temperature is the
_current state_. The thermostat acts to bring the current state
closer to the desired state, by turning equipment on or off.

{{< glossary_definition term_id="controller" length="short">}}

<!-- body -->

## Controller pattern

A controller tracks at least one Kubernetes resource type.
These {{< glossary_tooltip text="objects" term_id="object" >}}
have a spec field that represents the desired state. The
controller(s) for that resource are responsible for making the current
state come closer to that desired state.

The controller might carry the action out itself; more commonly, in Kubernetes,
a controller will send messages to the
{{< glossary_tooltip text="API server" term_id="kube-apiserver" >}} that have
useful side effects. You'll see examples of this below.

{{< comment >}}
Some built-in controllers, such as the namespace controller, act on objects
that do not have a spec. For simplicity, this page omits explaining that
detail.
{{< /comment >}}

### Control via API server

The {{< glossary_tooltip term_id="job" >}} controller is an example of a
Kubernetes built-in controller. Built-in controllers manage state by
interacting with the cluster API server.

Job is a Kubernetes resource that runs a
{{< glossary_tooltip term_id="pod" >}}, or perhaps several Pods, to carry out
a task and then stop.

(Once [scheduled](/docs/concepts/scheduling-eviction/), Pod objects become part of the
desired state for a kubelet).

When the Job controller sees a new task it makes sure that, somewhere
in your cluster, the kubelets on a set of Nodes are running the right
number of Pods to get the work done.
The Job controller does not run any Pods or containers
itself. Instead, the Job controller tells the API server to create or remove
Pods.
Other components in the
{{< glossary_tooltip text="control plane" term_id="control-plane" >}}
act on the new information (there are new Pods to schedule and run),
and eventually the work is done.

After you create a new Job, the desired state is for that Job to be completed.
The Job controller makes the current state for that Job be nearer to your
desired state: creating Pods that do the work you wanted for that Job, so that
the Job is closer to completion.

Controllers also update the objects that configure them.
For example: once the work is done for a Job, the Job controller
updates that Job object to mark it `Finished`.

(This is a bit like how some thermostats turn a light off to
indicate that your room is now at the temperature you set).

### Direct control

In contrast with Job, some controllers need to make changes to
things outside of your cluster.

For example, if you use a control loop to make sure there
are enough {{< glossary_tooltip text="Nodes" term_id="node" >}}
in your cluster, then that controller needs something outside the
current cluster to set up new Nodes when needed.

Controllers that interact with external state find their desired state from
the API server, then communicate directly with an external system to bring
the current state closer in line.

(There actually is a [controller](https://github.com/kubernetes/autoscaler/)
that horizontally scales the nodes in your cluster.)

The important point here is that the controller makes some changes to bring about
your desired state, and then reports the current state back to your cluster's API server.
Other control loops can observe that reported data and take their own actions.

In the thermostat example, if the room is very cold then a different controller
might also turn on a frost protection heater. With Kubernetes clusters, the control
plane indirectly works with IP address management tools, storage services,
cloud provider APIs, and other services by
[extending Kubernetes](/docs/concepts/extend-kubernetes/) to implement that.

## Desired versus current state {#desired-vs-current}

Kubernetes takes a cloud-native view of systems, and is able to handle
constant change.

Your cluster could be changing at any point as work happens and
control loops automatically fix failures. This means that,
potentially, your cluster never reaches a stable state.

As long as the controllers for your cluster are running and able to make
useful changes, it doesn't matter if the overall state is stable or not.

## Design

As a tenet of its design, Kubernetes uses lots of controllers that each manage
a particular aspect of cluster state. Most commonly, a particular control loop
(controller) uses one kind of resource as its desired state, and has a different
kind of resource that it manages to make that desired state happen. For example,
a controller for Jobs tracks Job objects (to discover new work) and Pod objects
(to run the Jobs, and then to see when the work is finished). In this case
something else creates the Jobs, whereas the Job controller creates Pods.

It's useful to have simple controllers rather than one, monolithic set of control
loops that are interlinked. Controllers can fail, so Kubernetes is designed to
allow for that.

{{< note >}}
There can be several controllers that create or update the same kind of object.
Behind the scenes, Kubernetes controllers make sure that they only pay attention
to the resources linked to their controlling resource.

For example, you can have Deployments and Jobs; these both create Pods.
The Job controller does not delete the Pods that your Deployment created,
because there is information ({{< glossary_tooltip term_id="label" text="labels" >}})
the controllers can use to tell those Pods apart.
{{< /note >}}

## Ways of running controllers {#running-controllers}

Kubernetes comes with a set of built-in controllers that run inside
the {{< glossary_tooltip term_id="kube-controller-manager" >}}. These
built-in controllers provide important core behaviors.

The Deployment controller and Job controller are examples of controllers that
come as part of Kubernetes itself ("built-in" controllers).
Kubernetes lets you run a resilient control plane, so that if any of the built-in
controllers were to fail, another part of the control plane will take over the work.

You can find controllers that run outside the control plane, to extend Kubernetes.
Or, if you want, you can write a new controller yourself.
You can run your own controller as a set of Pods,
or externally to Kubernetes. What fits best will depend on what that particular
controller does.

## {{% heading "whatsnext" %}}

- Read about the [Kubernetes control plane](/docs/concepts/architecture/#control-plane-components)
- Discover some of the basic [Kubernetes objects](/docs/concepts/overview/working-with-objects/)
- Learn more about the [Kubernetes API](/docs/concepts/overview/kubernetes-api/)
- If you want to write your own controller, see
  [Kubernetes extension patterns](/docs/concepts/extend-kubernetes/#extension-patterns)
  and the [sample-controller](https://github.com/kubernetes/sample-controller) repository.

---

title: Garbage Collection
content_type: concept
weight: 70

---

<!-- overview -->

{{<glossary_definition term_id="garbage-collection" length="short">}} This
allows the clean up of resources like the following:

- [Terminated pods](/docs/concepts/workloads/pods/pod-lifecycle/#pod-garbage-collection)
- [Completed Jobs](/docs/concepts/workloads/controllers/ttlafterfinished/)
- [Objects without owner references](#owners-dependents)
- [Unused containers and container images](#containers-images)
- [Dynamically provisioned PersistentVolumes with a StorageClass reclaim policy of Delete](/docs/concepts/storage/persistent-volumes/#delete)
- [Stale or expired CertificateSigningRequests (CSRs)](/docs/reference/access-authn-authz/certificate-signing-requests/#request-signing-process)
- {{<glossary_tooltip text="Nodes" term_id="node">}} deleted in the following scenarios:
  - On a cloud when the cluster uses a [cloud controller manager](/docs/concepts/architecture/cloud-controller/)
  - On-premises when the cluster uses an addon similar to a cloud controller
    manager
- [Node Lease objects](/docs/concepts/architecture/nodes/#heartbeats)

## Owners and dependents {#owners-dependents}

Many objects in Kubernetes link to each other through [_owner references_](/docs/concepts/overview/working-with-objects/owners-dependents/).
Owner references tell the control plane which objects are dependent on others.
Kubernetes uses owner references to give the control plane, and other API
clients, the opportunity to clean up related resources before deleting an
object. In most cases, Kubernetes manages owner references automatically.

Ownership is different from the [labels and selectors](/docs/concepts/overview/working-with-objects/labels/)
mechanism that some resources also use. For example, consider a
{{<glossary_tooltip text="Service" term_id="service">}} that creates
`EndpointSlice` objects. The Service uses _labels_ to allow the control plane to
determine which `EndpointSlice` objects are used for that Service. In addition
to the labels, each `EndpointSlice` that is managed on behalf of a Service has
an owner reference. Owner references help different parts of Kubernetes avoid
interfering with objects they don’t control.

{{< note >}}
Cross-namespace owner references are disallowed by design.
Namespaced dependents can specify cluster-scoped or namespaced owners.
A namespaced owner **must** exist in the same namespace as the dependent.
If it does not, the owner reference is treated as absent, and the dependent
is subject to deletion once all owners are verified absent.

Cluster-scoped dependents can only specify cluster-scoped owners.
In v1.20+, if a cluster-scoped dependent specifies a namespaced kind as an owner,
it is treated as having an unresolvable owner reference, and is not able to be garbage collected.

In v1.20+, if the garbage collector detects an invalid cross-namespace `ownerReference`,
or a cluster-scoped dependent with an `ownerReference` referencing a namespaced kind, a warning Event
with a reason of `OwnerRefInvalidNamespace` and an `involvedObject` of the invalid dependent is reported.
You can check for that kind of Event by running
`kubectl get events -A --field-selector=reason=OwnerRefInvalidNamespace`.
{{< /note >}}

## Cascading deletion {#cascading-deletion}

Kubernetes checks for and deletes objects that no longer have owner
references, like the pods left behind when you delete a ReplicaSet. When you
delete an object, you can control whether Kubernetes deletes the object's
dependents automatically, in a process called _cascading deletion_. There are
two types of cascading deletion, as follows:

- Foreground cascading deletion
- Background cascading deletion

You can also control how and when garbage collection deletes resources that have
owner references using Kubernetes {{<glossary_tooltip text="finalizers" term_id="finalizer">}}.

### Foreground cascading deletion {#foreground-deletion}

In foreground cascading deletion, the owner object you're deleting first enters
a _deletion in progress_ state. In this state, the following happens to the
owner object:

- The Kubernetes API server sets the object's `metadata.deletionTimestamp`
  field to the time the object was marked for deletion.
- The Kubernetes API server also sets the `metadata.finalizers` field to
  `foregroundDeletion`.
- The object remains visible through the Kubernetes API until the deletion
  process is complete.

After the owner object enters the _deletion in progress_ state, the controller
deletes dependents it knows about. After deleting all the dependent objects it knows about,
the controller deletes the owner object. At this point, the object is no longer visible in the
Kubernetes API.

During foreground cascading deletion, the only dependents that block owner
deletion are those that have the `ownerReference.blockOwnerDeletion=true` field
and are in the garbage collection controller cache. The garbage collection controller
cache may not contain objects whose resource type cannot be listed / watched successfully,
or objects that are created concurrent with deletion of an owner object.
See [Use foreground cascading deletion](/docs/tasks/administer-cluster/use-cascading-deletion/#use-foreground-cascading-deletion)
to learn more.

### Background cascading deletion {#background-deletion}

In background cascading deletion, the Kubernetes API server deletes the owner
object immediately and the garbage collector controller (custom or default)
cleans up the dependent objects in the background.
If a finalizer exists, it ensures that objects are not deleted until all necessary clean-up tasks are completed.
By default, Kubernetes uses background cascading deletion unless
you manually use foreground deletion or choose to orphan the dependent objects.

See [Use background cascading deletion](/docs/tasks/administer-cluster/use-cascading-deletion/#use-background-cascading-deletion)
to learn more.

### Orphaned dependents

When Kubernetes deletes an owner object, the dependents left behind are called
_orphan_ objects. By default, Kubernetes deletes dependent objects. To learn how
to override this behaviour, see [Delete owner objects and orphan dependents](/docs/tasks/administer-cluster/use-cascading-deletion/#set-orphan-deletion-policy).

## Garbage collection of unused containers and images {#containers-images}

The {{<glossary_tooltip text="kubelet" term_id="kubelet">}} performs garbage
collection on unused images every five minutes and on unused containers every
minute. You should avoid using external garbage collection tools, as these can
break the kubelet behavior and remove containers that should exist.

To configure options for unused container and image garbage collection, tune the
kubelet using a [configuration file](/docs/tasks/administer-cluster/kubelet-config-file/)
and change the parameters related to garbage collection using the
[`KubeletConfiguration`](/docs/reference/config-api/kubelet-config.v1beta1/)
resource type.

### Container image lifecycle

Kubernetes manages the lifecycle of all images through its _image manager_,
which is part of the kubelet, with the cooperation of
{{< glossary_tooltip text="cadvisor" term_id="cadvisor" >}}. The kubelet
considers the following disk usage limits when making garbage collection
decisions:

- `HighThresholdPercent`
- `LowThresholdPercent`

Disk usage above the configured `HighThresholdPercent` value triggers garbage
collection, which deletes images in order based on the last time they were used,
starting with the oldest first. The kubelet deletes images
until disk usage reaches the `LowThresholdPercent` value.

#### Garbage collection for unused container images {#image-maximum-age-gc}

You can specify the maximum time a local image can be unused for,
regardless of disk usage. This is a kubelet setting that you configure for each node.

To configure the setting, you need to set a value for the `imageMaximumGCAge`
field in the kubelet configuration file.

The value is specified as a Kubernetes {{< glossary_tooltip text="duration" term_id="duration" >}}.
See [duration](/docs/reference/glossary/?all=true#term-duration) in the glossary
for more details.

For example, you can set the configuration field to `12h45m`,
which means 12 hours and 45 minutes.

{{< note >}}
This feature does not track image usage across kubelet restarts. If the kubelet
is restarted, the tracked image age is reset, causing the kubelet to wait the full
`imageMaximumGCAge` duration before qualifying images for garbage collection
based on image age.
{{< /note>}}

### Container garbage collection {#container-image-garbage-collection}

The kubelet garbage collects unused containers based on the following variables,
which you can define:

- `MinAge`: the minimum age at which the kubelet can garbage collect a
  container. Disable by setting to `0`.
- `MaxPerPodContainer`: the maximum number of dead containers each Pod
  can have. Disable by setting to less than `0`.
- `MaxContainers`: the maximum number of dead containers the cluster can have.
  Disable by setting to less than `0`.

In addition to these variables, the kubelet garbage collects unidentified and
deleted containers, typically starting with the oldest first.

`MaxPerPodContainer` and `MaxContainers` may potentially conflict with each other
in situations where retaining the maximum number of containers per Pod
(`MaxPerPodContainer`) would go outside the allowable total of global dead
containers (`MaxContainers`). In this situation, the kubelet adjusts
`MaxPerPodContainer` to address the conflict. A worst-case scenario would be to
downgrade `MaxPerPodContainer` to `1` and evict the oldest containers.
Additionally, containers owned by pods that have been deleted are removed once
they are older than `MinAge`.

{{<note>}}
The kubelet only garbage collects the containers it manages.
{{</note>}}

## Configuring garbage collection {#configuring-gc}

You can tune garbage collection of resources by configuring options specific to
the controllers managing those resources. The following pages show you how to
configure garbage collection:

- [Configuring cascading deletion of Kubernetes objects](/docs/tasks/administer-cluster/use-cascading-deletion/)
- [Configuring cleanup of finished Jobs](/docs/concepts/workloads/controllers/ttlafterfinished/)

## {{% heading "whatsnext" %}}

- Learn more about [ownership of Kubernetes objects](/docs/concepts/overview/working-with-objects/owners-dependents/).
- Learn more about Kubernetes [finalizers](/docs/concepts/overview/working-with-objects/finalizers/).
- Learn about the [TTL controller](/docs/concepts/workloads/controllers/ttlafterfinished/) that cleans up finished Jobs.---
  title: Leases
  api_metadata:

* apiVersion: "coordination.k8s.io/v1"
  kind: "Lease"
  content_type: concept
  weight: 30

---

<!-- overview -->

Distributed systems often have a need for _leases_, which provide a mechanism to lock shared resources
and coordinate activity between members of a set.
In Kubernetes, the lease concept is represented by [Lease](/docs/reference/kubernetes-api/cluster-resources/lease-v1/)
objects in the `coordination.k8s.io` {{< glossary_tooltip text="API Group" term_id="api-group" >}},
which are used for system-critical capabilities such as node heartbeats and component-level leader election.

<!-- body -->

## Node heartbeats {#node-heart-beats}

Kubernetes uses the Lease API to communicate kubelet node heartbeats to the Kubernetes API server.
For every `Node` , there is a `Lease` object with a matching name in the `kube-node-lease`
namespace. Under the hood, every kubelet heartbeat is an **update** request to this `Lease` object, updating
the `spec.renewTime` field for the Lease. The Kubernetes control plane uses the time stamp of this field
to determine the availability of this `Node`.

See [Node Lease objects](/docs/concepts/architecture/nodes/#node-heartbeats) for more details.

## Leader election

Kubernetes also uses Leases to ensure only one instance of a component is running at any given time.
This is used by control plane components like `kube-controller-manager` and `kube-scheduler` in
HA configurations, where only one instance of the component should be actively running while the other
instances are on stand-by.

Read [coordinated leader election](/docs/concepts/cluster-administration/coordinated-leader-election)
to learn about how Kubernetes builds on the Lease API to select which component instance
acts as leader.

## API server identity

{{< feature-state feature_gate_name="APIServerIdentity" >}}

Starting in Kubernetes v1.26, each `kube-apiserver` uses the Lease API to publish its identity to the
rest of the system. While not particularly useful on its own, this provides a mechanism for clients to
discover how many instances of `kube-apiserver` are operating the Kubernetes control plane.
Existence of kube-apiserver leases enables future capabilities that may require coordination between
each kube-apiserver.

You can inspect Leases owned by each kube-apiserver by checking for lease objects in the `kube-system` namespace
with the name `apiserver-<sha256-hash>`. Alternatively you can use the label selector `apiserver.kubernetes.io/identity=kube-apiserver`:

```shell
kubectl -n kube-system get lease -l apiserver.kubernetes.io/identity=kube-apiserver
```

```
NAME                                        HOLDER                                                                           AGE
apiserver-07a5ea9b9b072c4a5f3d1c3702        apiserver-07a5ea9b9b072c4a5f3d1c3702_0c8914f7-0f35-440e-8676-7844977d3a05        5m33s
apiserver-7be9e061c59d368b3ddaf1376e        apiserver-7be9e061c59d368b3ddaf1376e_84f2a85d-37c1-4b14-b6b9-603e62e4896f        4m23s
apiserver-1dfef752bcb36637d2763d1868        apiserver-1dfef752bcb36637d2763d1868_c5ffa286-8a9a-45d4-91e7-61118ed58d2e        4m43s

```

The SHA256 hash used in the lease name is based on the OS hostname as seen by that API server. Each kube-apiserver should be
configured to use a hostname that is unique within the cluster. New instances of kube-apiserver that use the same hostname
will take over existing Leases using a new holder identity, as opposed to instantiating new Lease objects. You can check the
hostname used by kube-apiserver by checking the value of the `kubernetes.io/hostname` label:

```shell
kubectl -n kube-system get lease apiserver-07a5ea9b9b072c4a5f3d1c3702 -o yaml
```

```yaml
apiVersion: coordination.k8s.io/v1
kind: Lease
metadata:
  creationTimestamp: "2023-07-02T13:16:48Z"
  labels:
    apiserver.kubernetes.io/identity: kube-apiserver
    kubernetes.io/hostname: master-1
  name: apiserver-07a5ea9b9b072c4a5f3d1c3702
  namespace: kube-system
  resourceVersion: "334899"
  uid: 90870ab5-1ba9-4523-b215-e4d4e662acb1
spec:
  holderIdentity: apiserver-07a5ea9b9b072c4a5f3d1c3702_0c8914f7-0f35-440e-8676-7844977d3a05
  leaseDurationSeconds: 3600
  renewTime: "2023-07-04T21:58:48.065888Z"
```

Expired leases from kube-apiservers that no longer exist are garbage collected by new kube-apiservers after 1 hour.

You can disable API server identity leases by disabling the `APIServerIdentity`
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/).

## Workloads {#custom-workload}

Your own workload can define its own use of Leases. For example, you might run a custom
{{< glossary_tooltip term_id="controller" text="controller" >}} where a primary or leader member
performs operations that its peers do not. You define a Lease so that the controller replicas can select
or elect a leader, using the Kubernetes API for coordination.
If you do use a Lease, it's a good practice to define a name for the Lease that is obviously linked to
the product or component. For example, if you have a component named Example Foo, use a Lease named
`example-foo`.

If a cluster operator or another end user could deploy multiple instances of a component, select a name
prefix and pick a mechanism (such as hash of the name of the Deployment) to avoid name collisions
for the Leases.

You can use another approach so long as it achieves the same outcome: different software products do
not conflict with one another.

---

reviewers:

- jpbetz
  title: Mixed Version Proxy
  content_type: concept
  weight: 220

---

<!-- overview -->

{{< feature-state feature_gate_name="UnknownVersionInteroperabilityProxy" >}}

Kubernetes {{< skew currentVersion >}} includes an alpha feature that lets an
{{< glossary_tooltip text="API Server" term_id="kube-apiserver" >}}
proxy resource requests to other _peer_ API servers. It also lets clients get
a holistic view of resources served across the entire cluster through discovery.
This is useful when there are multiple
API servers running different versions of Kubernetes in one cluster
(for example, during a long-lived rollout to a new release of Kubernetes).

This enables cluster administrators to configure highly available clusters that can be upgraded
more safely, by :

1. ensuring that controllers relying on discovery to show a comprehensive list of resources
   for important tasks always get the complete view of all resources. We call this complete cluster wide
   discovery- _Peer-aggregated discovery_
1. directing resource requests (made during the upgrade) to the correct kube-apiserver.
   This proxying prevents users from seeing unexpected 404 Not Found errors that stem
   from the upgrade process. This mechanism is called the _Mixed Version Proxy_.

## Enabling Peer-aggregated Discovery and Mixed Version Proxy

Ensure that `UnknownVersionInteroperabilityProxy` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/#UnknownVersionInteroperabilityProxy)
is enabled when you start the {{< glossary_tooltip text="API Server" term_id="kube-apiserver" >}}:

```shell
kube-apiserver \
--feature-gates=UnknownVersionInteroperabilityProxy=true \
# required command line arguments for this feature
--peer-ca-file=<path to kube-apiserver CA cert>
--proxy-client-cert-file=<path to aggregator proxy cert>,
--proxy-client-key-file=<path to aggregator proxy key>,
--requestheader-client-ca-file=<path to aggregator CA cert>,
# requestheader-allowed-names can be set to blank to allow any Common Name
--requestheader-allowed-names=<valid Common Names to verify proxy client cert against>,

# optional flags for this feature
--peer-advertise-ip=`IP of this kube-apiserver that should be used by peers to proxy requests`
--peer-advertise-port=`port of this kube-apiserver that should be used by peers to proxy requests`

# …and other flags as usual
```

### Proxy transport and authentication between API servers {#transport-and-authn}

- The source kube-apiserver reuses the
  [existing APIserver client authentication flags](/docs/tasks/extend-kubernetes/configure-aggregation-layer/#kubernetes-apiserver-client-authentication)
  `--proxy-client-cert-file` and `--proxy-client-key-file` to present its identity that
  will be verified by its peer (the destination kube-apiserver). The destination API server
  verifies that peer connection based on the configuration you specify using the
  `--requestheader-client-ca-file` command line argument.

- To authenticate the destination server's serving certs, you must configure a certificate
  authority bundle by specifying the `--peer-ca-file` command line argument to the **source** API server.

### Configuration for peer API server connectivity

To set the network location of a kube-apiserver that peers will use to proxy requests, use the
`--peer-advertise-ip` and `--peer-advertise-port` command line arguments to kube-apiserver or specify
these fields in the API server configuration file.
If these flags are unspecified, peers will use the value from either `--advertise-address` or
`--bind-address` command line argument to the kube-apiserver.
If those too, are unset, the host's default interface is used.

## Peer-aggregated discovery

When you enable the feature, discovery requests are automatically enabled to serve
a comprehensive discovery document (listing all resources served by any apiserver in the cluster)
by default.

If you would like to request
a non peer-aggregated discovery document, you can indicate so by adding the following Accept header to the discovery request:

```
application/json;g=apidiscovery.k8s.io;v=v2;as=APIGroupDiscoveryList;profile=nopeer
```

{{< note >}}
Peer-aggregated discovery is only supported
for [Aggregated Discovery](/docs/concepts/overview/kubernetes-api/#aggregated-discovery) requests
to the `/apis` endpoint and not for [Unaggregated (Legacy) Discovery](/docs/concepts/overview/kubernetes-api/#unaggregated-discovery) requests.
{{< /note >}}

## Mixed version proxying

When you enable mixed version proxying, the [aggregation layer](/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)
loads a special filter that does the following:

- When a resource request reaches an API server that cannot serve that API
  (either because it is at a version pre-dating the introduction of the API or the API is turned off on the API server)
  the API server attempts to send the request to a peer API server that can serve the requested API.
  It does so by identifying API groups / versions / resources that the local server doesn't recognise,
  and tries to proxy those requests to a peer API server that is capable of handling the request.
- If the peer API server fails to respond, the _source_ API server responds with 503 ("Service Unavailable") error.

### How it works under the hood

When an API Server receives a resource request, it first checks which API servers can
serve the requested resource. This check happens using the non peer-aggregated discovery document.

- If the resource is listed in the non peer-aggregated discovery document retrieved from the API server that received the request(for example, `GET /api/v1/pods/some-pod`), the request is handled locally.

- If the resource in a request (for example, `GET /apis/resource.k8s.io/v1beta1/resourceclaims`) is not found in the non peer-aggregated discovery document retrieved from the API server trying to handle the request (the _handling API server_), likely because the `resource.k8s.io/v1beta1` API was introduced in a newer Kubernetes version and the _handling API server_ is running an older version that does not support it, then the _handling API server_ fetches the peer API servers that do serve the relevant API group / version / resource (`resource.k8s.io/v1beta1/resourceclaims` in this case) by checking the non peer-aggregated discovery documents from all peer API servers. The _handling API server_ then proxies the request to one of the matching peer kube-apiservers that are aware of the requested resource.

- If there is no peer known for that API group / version / resource, the handling API server
  passes the request to its own handler chain which should eventually return a 404 ("Not Found") response.

- If the handling API server has identified and selected a peer API server, but that peer fails
  to respond (for reasons such as network connectivity issues, or a data race between the request
  being received and a controller registering the peer's info into the control plane), then the handling
  API server responds with a 503 ("Service Unavailable") error.

---

reviewers:

- caesarxuchao
- dchen1107
  title: Nodes
  api_metadata:
- apiVersion: "v1"
  kind: "Node"
  content_type: concept
  weight: 10

---

<!-- overview -->

Kubernetes runs your {{< glossary_tooltip text="workload" term_id="workload" >}}
by placing containers into Pods to run on _Nodes_.
A node may be a virtual or physical machine, depending on the cluster. Each node
is managed by the
{{< glossary_tooltip text="control plane" term_id="control-plane" >}}
and contains the services necessary to run
{{< glossary_tooltip text="Pods" term_id="pod" >}}.

Typically you have several nodes in a cluster; in a learning or resource-limited
environment, you might have only one node.

The [components](/docs/concepts/architecture/#node-components) on a node include the
{{< glossary_tooltip text="kubelet" term_id="kubelet" >}}, a
{{< glossary_tooltip text="container runtime" term_id="container-runtime" >}}, and the
{{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}}.

<!-- body -->

## Management

There are two main ways to have Nodes added to the
{{< glossary_tooltip text="API server" term_id="kube-apiserver" >}}:

1. The kubelet on a node self-registers to the control plane
2. You (or another human user) manually add a Node object

After you create a Node {{< glossary_tooltip text="object" term_id="object" >}},
or the kubelet on a node self-registers, the control plane checks whether the new Node object
is valid. For example, if you try to create a Node from the following JSON manifest:

```json
{
  "kind": "Node",
  "apiVersion": "v1",
  "metadata": {
    "name": "10.240.79.157",
    "labels": {
      "name": "my-first-k8s-node"
    }
  }
}
```

Kubernetes creates a Node object internally (the representation). Kubernetes checks
that a kubelet has registered to the API server that matches the `metadata.name`
field of the Node. If the node is healthy (i.e. all necessary services are running),
then it is eligible to run a Pod. Otherwise, that node is ignored for any cluster activity
until it becomes healthy.

{{< note >}}
Kubernetes keeps the object for the invalid Node and continues checking to see whether
it becomes healthy.

You, or a {{< glossary_tooltip term_id="controller" text="controller">}}, must explicitly
delete the Node object to stop that health checking.
{{< /note >}}

The name of a Node object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

### Node name uniqueness

The [name](/docs/concepts/overview/working-with-objects/names#names) identifies a Node. Two Nodes
cannot have the same name at the same time. Kubernetes also assumes that a resource with the same
name is the same object. In the case of a Node, it is implicitly assumed that an instance using the
same name will have the same state (e.g. network settings, root disk contents) and attributes like
node labels. This may lead to inconsistencies if an instance was modified without changing its name.
If the Node needs to be replaced or updated significantly, the existing Node object needs to be
removed from API server first and re-added after the update.

### Self-registration of Nodes

When the kubelet flag `--register-node` is true (the default), the kubelet will attempt to
register itself with the API server. This is the preferred pattern, used by most distros.

For self-registration, the kubelet is started with the following options:

- `--kubeconfig` - Path to credentials to authenticate itself to the API server.
- `--cloud-provider` - How to talk to a {{< glossary_tooltip text="cloud provider" term_id="cloud-provider" >}}
  to read metadata about itself.
- `--register-node` - Automatically register with the API server.
- `--register-with-taints` - Register the node with the given list of
  {{< glossary_tooltip text="taints" term_id="taint" >}} (comma separated `<key>=<value>:<effect>`).

  No-op if `register-node` is false.

- `--node-ip` - Optional comma-separated list of the IP addresses for the node.
  You can only specify a single address for each address family.
  For example, in a single-stack IPv4 cluster, you set this value to be the IPv4 address that the
  kubelet should use for the node.
  See [configure IPv4/IPv6 dual stack](/docs/concepts/services-networking/dual-stack/#configure-ipv4-ipv6-dual-stack)
  for details of running a dual-stack cluster.

  If you don't provide this argument, the kubelet uses the node's default IPv4 address, if any;
  if the node has no IPv4 addresses then the kubelet uses the node's default IPv6 address.

- `--node-labels` - {{< glossary_tooltip text="Labels" term_id="label" >}} to add when registering the node
  in the cluster (see label restrictions enforced by the
  [NodeRestriction admission plugin](/docs/reference/access-authn-authz/admission-controllers/#noderestriction)).
- `--node-status-update-frequency` - Specifies how often kubelet posts its node status to the API server.

When the [Node authorization mode](/docs/reference/access-authn-authz/node/) and
[NodeRestriction admission plugin](/docs/reference/access-authn-authz/admission-controllers/#noderestriction)
are enabled, kubelets are only authorized to create/modify their own Node resource.

{{< note >}}
As mentioned in the [Node name uniqueness](#node-name-uniqueness) section,
when Node configuration needs to be updated, it is a good practice to re-register
the node with the API server. For example, if the kubelet is being restarted with
a new set of `--node-labels`, but the same Node name is used, the change will
not take effect, as labels are only set (or modified) upon Node registration with the API server.

Pods already scheduled on the Node may misbehave or cause issues if the Node
configuration will be changed on kubelet restart. For example, an already running
Pod may be tainted against the new labels assigned to the Node, while other
Pods, that are incompatible with that Pod will be scheduled based on this new
label. Node re-registration ensures all Pods will be drained and properly
re-scheduled.
{{< /note >}}

### Manual Node administration

You can create and modify Node objects using
{{< glossary_tooltip text="kubectl" term_id="kubectl" >}}.

When you want to create Node objects manually, set the kubelet flag `--register-node=false`.

You can modify Node objects regardless of the setting of `--register-node`.
For example, you can set labels on an existing Node or mark it unschedulable.

You can set optional node role(s) for nodes by adding one or more `node-role.kubernetes.io/<role>: <role>` labels to the node where characters of `<role>`
are limited by the [syntax](/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set) rules for labels.

Kubernetes ignores the label value for node roles; by convention, you can set it to the same string you used for the node role in the label key.

You can use labels on Nodes in conjunction with node selectors on Pods to control
scheduling. For example, you can constrain a Pod to only be eligible to run on
a subset of the available nodes.

Marking a node as unschedulable prevents the scheduler from placing new pods onto
that Node but does not affect existing Pods on the Node. This is useful as a
preparatory step before a node reboot or other maintenance.

To mark a Node unschedulable, run:

```shell
kubectl cordon $NODENAME
```

See [Safely Drain a Node](/docs/tasks/administer-cluster/safely-drain-node/)
for more details.

{{< note >}}
Pods that are part of a {{< glossary_tooltip term_id="daemonset" >}} tolerate
being run on an unschedulable Node. DaemonSets typically provide node-local services
that should run on the Node even if it is being drained of workload applications.
{{< /note >}}

## Node status

A Node's status contains the following information:

- [Addresses](/docs/reference/node/node-status/#addresses)
- [Conditions](/docs/reference/node/node-status/#condition)
- [Capacity and Allocatable](/docs/reference/node/node-status/#capacity)
- [Info](/docs/reference/node/node-status/#info)

You can use `kubectl` to view a Node's status and other details:

```shell
kubectl describe node <insert-node-name-here>
```

See [Node Status](/docs/reference/node/node-status/) for more details.

## Node heartbeats

Heartbeats, sent by Kubernetes nodes, help your cluster determine the
availability of each node, and to take action when failures are detected.

For nodes there are two forms of heartbeats:

- Updates to the [`.status`](/docs/reference/node/node-status/) of a Node.
- [Lease](/docs/concepts/architecture/leases/) objects
  within the `kube-node-lease`
  {{< glossary_tooltip term_id="namespace" text="namespace">}}.
  Each Node has an associated Lease object.

## Node controller

The node {{< glossary_tooltip text="controller" term_id="controller" >}} is a
Kubernetes control plane component that manages various aspects of nodes.

The node controller has multiple roles in a node's life. The first is assigning a
CIDR block to the node when it is registered (if CIDR assignment is turned on).

The second is keeping the node controller's internal list of nodes up to date with
the cloud provider's list of available machines. When running in a cloud
environment and whenever a node is unhealthy, the node controller asks the cloud
provider if the VM for that node is still available. If not, the node
controller deletes the node from its list of nodes.

The third is monitoring the nodes' health. The node controller is
responsible for:

- In the case that a node becomes unreachable, updating the `Ready` condition
  in the Node's `.status` field. In this case the node controller sets the
  `Ready` condition to `Unknown`.
- If a node remains unreachable: triggering
  [API-initiated eviction](/docs/concepts/scheduling-eviction/api-eviction/)
  for all of the Pods on the unreachable node. By default, the node controller
  waits 5 minutes between marking the node as `Unknown` and submitting
  the first eviction request.

By default, the node controller checks the state of each node every 5 seconds.
This period can be configured using the `--node-monitor-period` flag on the
`kube-controller-manager` component.

### Rate limits on eviction

In most cases, the node controller limits the eviction rate to
`--node-eviction-rate` (default 0.1) per second, meaning it won't evict pods
from more than 1 node per 10 seconds.

The node eviction behavior changes when a node in a given availability zone
becomes unhealthy. The node controller checks what percentage of nodes in the zone
are unhealthy (the `Ready` condition is `Unknown` or `False`) at the same time:

- If the fraction of unhealthy nodes is at least `--unhealthy-zone-threshold`
  (default 0.55), then the eviction rate is reduced.
- If the cluster is small (i.e. has less than or equal to
  `--large-cluster-size-threshold` nodes - default 50), then evictions are stopped.
- Otherwise, the eviction rate is reduced to `--secondary-node-eviction-rate`
  (default 0.01) per second.

The reason these policies are implemented per availability zone is because one
availability zone might become partitioned from the control plane while the others remain
connected. If your cluster does not span multiple cloud provider availability zones,
then the eviction mechanism does not take per-zone unavailability into account.

A key reason for spreading your nodes across availability zones is so that the
workload can be shifted to healthy zones when one entire zone goes down.
Therefore, if all nodes in a zone are unhealthy, then the node controller evicts at
the normal rate of `--node-eviction-rate`. The corner case is when all zones are
completely unhealthy (none of the nodes in the cluster are healthy). In such a
case, the node controller assumes that there is some problem with connectivity
between the control plane and the nodes, and doesn't perform any evictions.
(If there has been an outage and some nodes reappear, the node controller does
evict pods from the remaining nodes that are unhealthy or unreachable).

The node controller is also responsible for evicting pods running on nodes with
`NoExecute` taints, unless those pods tolerate that taint.
The node controller also adds {{< glossary_tooltip text="taints" term_id="taint" >}}
corresponding to node problems like node unreachable or not ready. This means
that the scheduler won't place Pods onto unhealthy nodes.

## Resource capacity tracking {#node-capacity}

Node objects track information about the Node's resource capacity: for example, the amount
of memory available and the number of CPUs.
Nodes that [self register](#self-registration-of-nodes) report their capacity during
registration. If you [manually](#manual-node-administration) add a Node, then
you need to set the node's capacity information when you add it.

The Kubernetes {{< glossary_tooltip text="scheduler" term_id="kube-scheduler" >}} ensures that
there are enough resources for all the Pods on a Node. The scheduler checks that the sum
of the requests of containers on the node is no greater than the node's capacity.
That sum of requests includes all containers managed by the kubelet, but excludes any
containers started directly by the container runtime, and also excludes any
processes running outside of the kubelet's control.

{{< note >}}
If you want to explicitly reserve resources for non-Pod processes, see
[reserve resources for system daemons](/docs/tasks/administer-cluster/reserve-compute-resources/#system-reserved).
{{< /note >}}

## Node topology

{{< feature-state feature_gate_name="TopologyManager" >}}

If you have enabled the `TopologyManager`
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/), then
the kubelet can use topology hints when making resource assignment decisions.
See [Control Topology Management Policies on a Node](/docs/tasks/administer-cluster/topology-manager/)
for more information.

## {{% heading "whatsnext" %}}

Learn more about the following:

- [Components](/docs/concepts/architecture/#node-components) that make up a node.
- [API definition for Node](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#node-v1-core).
- [Node](https://git.k8s.io/design-proposals-archive/architecture/architecture.md#the-kubernetes-node)
  section of the architecture design document.
- [Graceful/non-graceful node shutdown](/docs/concepts/cluster-administration/node-shutdown/).
- [Node autoscaling](/docs/concepts/cluster-administration/node-autoscaling/) to
  manage the number and size of nodes in your cluster.
- [Taints and Tolerations](/docs/concepts/scheduling-eviction/taint-and-toleration/).
- [Node Resource Managers](/docs/concepts/policy/node-resource-managers/).
- [Resource Management for Windows nodes](/docs/concepts/configuration/windows-resource-management/).

---

title: Kubernetes Self-Healing
content_type: concept
weight: 50
feature:
title: Self-healing
anchor: Automated recovery from damage
description: >
Kubernetes restarts containers that crash, replaces entire Pods where needed,
reattaches storage in response to wider failures, and can integrate with
node autoscalers to self-heal even at the node level.

---

<!-- overview -->

Kubernetes is designed with self-healing capabilities that help maintain the health and availability of workloads.
It automatically replaces failed containers, reschedules workloads when nodes become unavailable, and ensures that the desired state of the system is maintained.

<!-- body -->

## Self-Healing capabilities {#self-healing-capabilities}

- **Container-level restarts:** If a container inside a Pod fails, Kubernetes restarts it based on the [`restartPolicy`](/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy).

- **Replica replacement:** If a Pod in a [Deployment](/docs/concepts/workloads/controllers/deployment/) or [StatefulSet](/docs/concepts/workloads/controllers/statefulset/) fails, Kubernetes creates a replacement Pod to maintain the specified number of replicas.
  If a Pod that is part of a [DaemonSet](/docs/concepts/workloads/controllers/daemonset/) fails, the control plane
  creates a replacement Pod to run on the same node.

- **Persistent storage recovery:** If a node is running a Pod with a PersistentVolume (PV) attached, and the node fails, Kubernetes can reattach the volume to a new Pod on a different node.

- **Load balancing for Services:** If a Pod behind a [Service](/docs/concepts/services-networking/service/) fails, Kubernetes automatically removes it from the Service's endpoints to route traffic only to healthy Pods.

Here are some of the key components that provide Kubernetes self-healing:

- **[kubelet](/docs/concepts/architecture/#kubelet):** Ensures that containers are running, and restarts those that fail.

- **Deployment (via ReplicaSet), ReplicaSet, StatefulSet and DaemonSet controllers:** Maintain the desired number of Pod replicas.

- **PersistentVolume controller:** Manages volume attachment and detachment for stateful workloads.

## Considerations {#considerations}

- **Storage Failures:** If a persistent volume becomes unavailable, recovery steps may be required.

- **Application Errors:** Kubernetes can restart containers, but underlying application issues must be addressed separately.

## {{% heading "whatsnext" %}}

- Read more about [Pods](/docs/concepts/workloads/pods/)
- Learn about [Kubernetes Controllers](/docs/concepts/architecture/controller/)
- Explore [PersistentVolumes](/docs/concepts/storage/persistent-volumes/)
- Read about [node autoscaling](/docs/concepts/cluster-administration/node-autoscaling/). Node autoscaling
  also provides automatic healing if or when nodes fail in your cluster.

---

title: Cluster Administration
reviewers:

- davidopp
- lavalamp
  weight: 100
  content_type: concept
  description: >
  Lower-level detail relevant to creating or administering a Kubernetes cluster.
  no_list: true
  card:
  name: setup
  weight: 60
  anchors:
  - anchor: "#securing-a-cluster"
    title: Securing a cluster

---

<!-- overview -->

The cluster administration overview is for anyone creating or administering a Kubernetes cluster.
It assumes some familiarity with core Kubernetes [concepts](/docs/concepts/).

<!-- body -->

## Planning a cluster

See the guides in [Setup](/docs/setup/) for examples of how to plan, set up, and configure
Kubernetes clusters. The solutions listed in this article are called _distros_.

{{< note  >}}
Not all distros are actively maintained. Choose distros which have been tested with a recent
version of Kubernetes.
{{< /note >}}

Before choosing a guide, here are some considerations:

- Do you want to try out Kubernetes on your computer, or do you want to build a high-availability,
  multi-node cluster? Choose distros best suited for your needs.
- Will you be using **a hosted Kubernetes cluster**, such as
  [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/), or **hosting your own cluster**?
- Will your cluster be **on-premises**, or **in the cloud (IaaS)**? Kubernetes does not directly
  support hybrid clusters. Instead, you can set up multiple clusters.
- **If you are configuring Kubernetes on-premises**, consider which
  [networking model](/docs/concepts/cluster-administration/networking/) fits best.
- Will you be running Kubernetes on **"bare metal" hardware** or on **virtual machines (VMs)**?
- Do you **want to run a cluster**, or do you expect to do **active development of Kubernetes project code**?
  If the latter, choose an actively-developed distro. Some distros only use binary releases, but
  offer a greater variety of choices.
- Familiarize yourself with the [components](/docs/concepts/overview/components/) needed to run a cluster.

## Managing a cluster

- Learn how to [manage nodes](/docs/concepts/architecture/nodes/).

  - Read about [Node autoscaling](/docs/concepts/cluster-administration/node-autoscaling/).

- Learn how to set up and manage the [resource quota](/docs/concepts/policy/resource-quotas/) for shared clusters.

## Securing a cluster

- [Generate Certificates](/docs/tasks/administer-cluster/certificates/) describes the steps to
  generate certificates using different tool chains.

- [Kubernetes Container Environment](/docs/concepts/containers/container-environment/) describes
  the environment for Kubelet managed containers on a Kubernetes node.

- [Controlling Access to the Kubernetes API](/docs/concepts/security/controlling-access) describes
  how Kubernetes implements access control for its own API.

- [Authenticating](/docs/reference/access-authn-authz/authentication/) explains authentication in
  Kubernetes, including the various authentication options.

- [Authorization](/docs/reference/access-authn-authz/authorization/) is separate from
  authentication, and controls how HTTP calls are handled.

- [Using Admission Controllers](/docs/reference/access-authn-authz/admission-controllers/)
  explains plug-ins which intercepts requests to the Kubernetes API server after authentication
  and authorization.

- [Admission Webhook Good Practices](/docs/concepts/cluster-administration/admission-webhooks-good-practices/)
  provides good practices and considerations when designing mutating admission
  webhooks and validating admission webhooks.

- [Using Sysctls in a Kubernetes Cluster](/docs/tasks/administer-cluster/sysctl-cluster/)
  describes to an administrator how to use the `sysctl` command-line tool to set kernel parameters
  .

- [Auditing](/docs/tasks/debug/debug-cluster/audit/) describes how to interact with Kubernetes'
  audit logs.

### Securing the kubelet

- [Control Plane-Node communication](/docs/concepts/architecture/control-plane-node-communication/)
- [TLS bootstrapping](/docs/reference/access-authn-authz/kubelet-tls-bootstrapping/)
- [Kubelet authentication/authorization](/docs/reference/access-authn-authz/kubelet-authn-authz/)

## Optional Cluster Services

- [DNS Integration](/docs/concepts/services-networking/dns-pod-service/) describes how to resolve
  a DNS name directly to a Kubernetes service.

- [Logging and Monitoring Cluster Activity](/docs/concepts/cluster-administration/logging/)
  explains how logging in Kubernetes works and how to implement it.

---

title: Installing Addons
content_type: concept
weight: 150

---

<!-- overview -->

{{% thirdparty-content %}}

Add-ons extend the functionality of Kubernetes.

This page lists some of the available add-ons and links to their respective
installation instructions. The list does not try to be exhaustive.

<!-- body -->

## Networking and Network Policy

- [ACI](https://www.github.com/noironetworks/aci-containers) provides integrated
  container networking and network security with Cisco ACI.
- [Antrea](https://antrea.io/) operates at Layer 3/4 to provide networking and
  security services for Kubernetes, leveraging Open vSwitch as the networking
  data plane. Antrea is a [CNCF project at the Sandbox level](https://www.cncf.io/projects/antrea/).
- [Calico](https://www.tigera.io/project-calico/) is a networking and network
  policy provider. Calico supports a flexible set of networking options so you
  can choose the most efficient option for your situation, including non-overlay
  and overlay networks, with or without BGP. Calico uses the same engine to
  enforce network policy for hosts, pods, and (if using Istio & Envoy)
  applications at the service mesh layer.
- [Canal](https://projectcalico.docs.tigera.io/getting-started/kubernetes/flannel/flannel)
  unites Flannel and Calico, providing networking and network policy.
- [Cilium](https://github.com/cilium/cilium) is a networking, observability,
  and security solution with an eBPF-based data plane. Cilium provides a
  simple flat Layer 3 network with the ability to span multiple clusters
  in either a native routing or overlay/encapsulation mode, and can enforce
  network policies on L3-L7 using an identity-based security model that is
  decoupled from network addressing. Cilium can act as a replacement for
  kube-proxy; it also offers additional, opt-in observability and security features.
  Cilium is a [CNCF project at the Graduated level](https://www.cncf.io/projects/cilium/).
- [CNI-Genie](https://github.com/cni-genie/CNI-Genie) enables Kubernetes to seamlessly
  connect to a choice of CNI plugins, such as Calico, Canal, Flannel, or Weave.
  CNI-Genie is a [CNCF project at the Sandbox level](https://www.cncf.io/projects/cni-genie/).
- [Contiv](https://contivpp.io/) provides configurable networking (native L3 using BGP,
  overlay using vxlan, classic L2, and Cisco-SDN/ACI) for various use cases and a rich
  policy framework. Contiv project is fully [open sourced](https://github.com/contiv).
  The [installer](https://github.com/contiv/install) provides both kubeadm and
  non-kubeadm based installation options.
- [Contrail](https://www.juniper.net/us/en/products-services/sdn/contrail/contrail-networking/),
  based on [Tungsten Fabric](https://tungsten.io), is an open source, multi-cloud
  network virtualization and policy management platform. Contrail and Tungsten
  Fabric are integrated with orchestration systems such as Kubernetes, OpenShift,
  OpenStack and Mesos, and provide isolation modes for virtual machines, containers/pods
  and bare metal workloads.
- [Flannel](https://github.com/flannel-io/flannel#deploying-flannel-manually) is
  an overlay network provider that can be used with Kubernetes.
- [Gateway API](/docs/concepts/services-networking/gateway/) is an open source project managed by
  the [SIG Network](https://github.com/kubernetes/community/tree/master/sig-network) community and
  provides an expressive, extensible, and role-oriented API for modeling service networking.
- [Knitter](https://github.com/ZTE/Knitter/) is a plugin to support multiple network
  interfaces in a Kubernetes pod.
- [Multus](https://github.com/k8snetworkplumbingwg/multus-cni) is a Multi plugin for
  multiple network support in Kubernetes to support all CNI plugins
  (e.g. Calico, Cilium, Contiv, Flannel), in addition to SRIOV, DPDK, OVS-DPDK and
  VPP based workloads in Kubernetes.
- [OVN-Kubernetes](https://github.com/ovn-org/ovn-kubernetes/) is a networking
  provider for Kubernetes based on [OVN (Open Virtual Network)](https://github.com/ovn-org/ovn/),
  a virtual networking implementation that came out of the Open vSwitch (OVS) project.
  OVN-Kubernetes provides an overlay based networking implementation for Kubernetes,
  including an OVS based implementation of load balancing and network policy.
- [Nodus](https://github.com/akraino-edge-stack/icn-nodus) is an OVN based CNI
  controller plugin to provide cloud native based Service function chaining(SFC).
- [NSX-T](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/index.html) Container Plug-in (NCP)
  provides integration between VMware NSX-T and container orchestrators such as
  Kubernetes, as well as integration between NSX-T and container-based CaaS/PaaS
  platforms such as Pivotal Container Service (PKS) and OpenShift.
- [Nuage](https://github.com/nuagenetworks/nuage-kubernetes/blob/v5.1.1-1/docs/kubernetes-1-installation.rst)
  is an SDN platform that provides policy-based networking between Kubernetes
  Pods and non-Kubernetes environments with visibility and security monitoring.
- [Romana](https://github.com/romana) is a Layer 3 networking solution for pod
  networks that also supports the [NetworkPolicy](/docs/concepts/services-networking/network-policies/) API.
- [Spiderpool](https://github.com/spidernet-io/spiderpool) is an underlay and RDMA
  networking solution for Kubernetes. Spiderpool is supported on bare metal, virtual machines,
  and public cloud environments.
- [Terway](https://github.com/AliyunContainerService/terway/) is a suite of CNI plugins
  based on AlibabaCloud's VPC and ECS network products. It provides native VPC networking
  and network policies in AlibabaCloud environments.
- [Weave Net](https://github.com/rajch/weave#using-weave-on-kubernetes)
  provides networking and network policy, will carry on working on both sides
  of a network partition, and does not require an external database.

## Service Discovery

- [CoreDNS](https://coredns.io) is a flexible, extensible DNS server which can
  be [installed](https://github.com/coredns/helm)
  as the in-cluster DNS for pods.

## Visualization &amp; Control

- [Dashboard](https://github.com/kubernetes/dashboard#kubernetes-dashboard)
  is a dashboard web interface for Kubernetes.
- [Headlamp](https://headlamp.dev/) is an extensible Kubernetes UI that can be
  deployed in-cluster or used as a desktop application.

## Infrastructure

- [KubeVirt](https://kubevirt.io/user-guide/#/installation/installation) is an add-on
  to run virtual machines on Kubernetes. Usually run on bare-metal clusters.
- The
  [node problem detector](https://github.com/kubernetes/node-problem-detector)
  runs on Linux nodes and reports system issues as either
  [Events](/docs/reference/kubernetes-api/cluster-resources/event-v1/) or
  [Node conditions](/docs/concepts/architecture/nodes/#condition).

## Instrumentation

- [kube-state-metrics](/docs/concepts/cluster-administration/kube-state-metrics)

## Legacy Add-ons

There are several other add-ons documented in the deprecated
[cluster/addons](https://git.k8s.io/kubernetes/cluster/addons) directory.

## Well-maintained ones should be linked to here. PRs welcome!

title: Admission Webhook Good Practices
description: >
Recommendations for designing and deploying admission webhooks in Kubernetes.
content_type: concept
weight: 60

---

<!-- overview -->

This page provides good practices and considerations when designing
_admission webhooks_ in Kubernetes. This information is intended for
cluster operators who run admission webhook servers or third-party applications
that modify or validate your API requests.

Before reading this page, ensure that you're familiar with the following
concepts:

- [Admission controllers](/docs/reference/access-authn-authz/admission-controllers/)
- [Admission webhooks](/docs/reference/access-authn-authz/extensible-admission-controllers/#what-are-admission-webhooks)

<!-- body -->

## Importance of good webhook design {#why-good-webhook-design-matters}

Admission control occurs when any create, update, or delete request
is sent to the Kubernetes API. Admission controllers intercept requests that
match specific criteria that you define. These requests are then sent to
mutating admission webhooks or validating admission webhooks. These webhooks are
often written to ensure that specific fields in object specifications exist or
have specific allowed values.

Webhooks are a powerful mechanism to extend the Kubernetes API. Badly-designed
webhooks often result in workload disruptions because of how much control
the webhooks have over objects in the cluster. Like other API extension
mechanisms, webhooks are challenging to test at scale for compatibility with
all of your workloads, other webhooks, add-ons, and plugins.

Additionally, with every release, Kubernetes adds or modifies the API with new
features, feature promotions to beta or stable status, and deprecations. Even
stable Kubernetes APIs are likely to change. For example, the `Pod` API changed
in v1.29 to add the
[Sidecar containers](/docs/concepts/workloads/pods/sidecar-containers/) feature.
While it's rare for a Kubernetes object to enter a broken state because of a new
Kubernetes API, webhooks that worked as expected with earlier versions of an API
might not be able to reconcile more recent changes to that API. This can result
in unexpected behavior after you upgrade your clusters to newer versions.

This page describes common webhook failure scenarios and how to avoid them by
cautiously and thoughtfully designing and implementing your webhooks.

## Identify whether you use admission webhooks {#identify-admission-webhooks}

Even if you don't run your own admission webhooks, some third-party applications
that you run in your clusters might use mutating or validating admission
webhooks.

To check whether your cluster has any mutating admission webhooks, run the
following command:

```shell
kubectl get mutatingwebhookconfigurations
```

The output lists any mutating admission controllers in the cluster.

To check whether your cluster has any validating admission webhooks, run the
following command:

```shell
kubectl get validatingwebhookconfigurations
```

The output lists any validating admission controllers in the cluster.

## Choose an admission control mechanism {#choose-admission-mechanism}

Kubernetes includes multiple admission control and policy enforcement options.
Knowing when to use a specific option can help you to improve latency and
performance, reduce management overhead, and avoid issues during version
upgrades. The following table describes the mechanisms that let you mutate or
validate resources during admission:

<!-- This table is HTML because it uses unordered lists for readability. -->
<table>
  <caption>Mutating and validating admission control in Kubernetes</caption>
  <thead>
    <tr>
      <th>Mechanism</th>
      <th>Description</th>
      <th>Use cases</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="/docs/reference/access-authn-authz/extensible-admission-controllers/">Mutating admission webhook</a></td>
      <td>Intercept API requests before admission and modify as needed using
        custom logic.</td>
      <td><ul>
        <li>Make critical modifications that must happen before resource
          admission.</li>
        <li>Make complex modifications that require advanced logic, like calling
          external APIs.</li>
      </ul></td>
    </tr>
    <tr>
      <td><a href="/docs/reference/access-authn-authz/mutating-admission-policy/">Mutating admission policy</a></td>
      <td>Intercept API requests before admission and modify as needed using
        Common Expression Language (CEL) expressions.</td>
      <td><ul>
        <li>Make critical modifications that must happen before resource
          admission.</li>
        <li>Make simple modifications, such as adjusting labels or replica
        counts.</li>
      </ul></td>
    </tr>
    <tr>
      <td><a href="/docs/reference/access-authn-authz/extensible-admission-controllers/">Validating admission webhook</a></td>
      <td>Intercept API requests before admission and validate against complex
        policy declarations.</td>
      <td><ul>
        <li>Validate critical configurations before resource admission.</li>
        <li>Enforce complex policy logic before admission.</li>
      </ul></td>
    </tr>
    <tr>
      <td><a href="/docs/reference/access-authn-authz/validating-admission-policy/">Validating admission policy</a></td>
      <td>Intercept API requests before admission and validate against CEL
        expressions.</td>
      <td><ul>
        <li>Validate critical configurations before resource admission.</li>
        <li>Enforce policy logic using CEL expressions.</li>
      </ul></td>
    </tr>
  </tbody>
</table>

In general, use _webhook_ admission control when you want an extensible way to
declare or configure the logic. Use built-in CEL-based admission control when
you want to declare simpler logic without the overhead of running a webhook
server. The Kubernetes project recommends that you use CEL-based admission
control when possible.

### Use built-in validation and defaulting for CustomResourceDefinitions {#no-crd-validation-defaulting}

If you use
{{< glossary_tooltip text="CustomResourceDefinitions" term_id="customresourcedefinition" >}},
don't use admission webhooks to validate values in CustomResource specifications
or to set default values for fields. Kubernetes lets you define validation rules
and default field values when you create CustomResourceDefinitions.

To learn more, see the following resources:

- [Validation rules](/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#validation-rules)
- [Defaulting](/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#defaulting)

## Performance and latency {#performance-latency}

This section describes recommendations for improving performance and reducing
latency. In summary, these are as follows:

- Consolidate webhooks and limit the number of API calls per webhook.
- Use audit logs to check for webhooks that repeatedly do the same action.
- Use load balancing for webhook availability.
- Set a small timeout value for each webhook.
- Consider cluster availability needs during webhook design.

### Design admission webhooks for low latency {#design-admission-webhooks-low-latency}

Mutating admission webhooks are called in sequence. Depending on the mutating
webhook setup, some webhooks might be called multiple times. Every mutating
webhook call adds latency to the admission process. This is unlike validating
webhooks, which get called in parallel.

When designing your mutating webhooks, consider your latency requirements and
tolerance. The more mutating webhooks there are in your cluster, the greater the
chance of latency increases.

Consider the following to reduce latency:

- Consolidate webhooks that perform a similar mutation on different objects.
- Reduce the number of API calls made in the mutating webhook server logic.
- Limit the match conditions of each mutating webhook to reduce how many
  webhooks are triggered by a specific API request.
- Consolidate small webhooks into one server and configuration to help with
  ordering and organization.

### Prevent loops caused by competing controllers {#prevent-loops-competing-controllers}

Consider any other components that run in your cluster that might conflict with
the mutations that your webhook makes. For example, if your webhook adds a label
that a different controller removes, your webhook gets called again. This leads
to a loop.

To detect these loops, try the following:

1.  Update your cluster audit policy to log audit events. Use the following
    parameters:

    - `level`: `RequestResponse`
    - `verbs`: `["patch"]`
    - `omitStages`: `RequestReceived`

    Set the audit rule to create events for the specific resources that your
    webhook mutates.

1.  Check your audit events for webhooks being reinvoked multiple times with the
    same patch being applied to the same object, or for an object having
    a field updated and reverted multiple times.

### Set a small timeout value {#small-timeout}

Admission webhooks should evaluate as quickly as possible (typically in
milliseconds), since they add to API request latency. Use a small timeout for
webhooks.

For details, see
[Timeouts](/docs/reference/access-authn-authz/extensible-admission-controllers/#timeouts).

### Use a load balancer to ensure webhook availability {#load-balancer-webhook}

Admission webhooks should leverage some form of load-balancing to provide high
availability and performance benefits. If a webhook is running within the
cluster, you can run multiple webhook backends behind a Service of type
`ClusterIP`.

### Use a high-availability deployment model {#ha-deployment}

Consider your cluster's availability requirements when designing your webhook.
For example, during node downtime or zonal outages, Kubernetes marks Pods as
`NotReady` to allow load balancers to reroute traffic to available zones and
nodes. These updates to Pods might trigger your mutating webhooks. Depending on
the number of affected Pods, the mutating webhook server has a risk of timing
out or causing delays in Pod processing. As a result, traffic won't get
rerouted as quickly as you need.

Consider situations like the preceding example when writing your webhooks.
Exclude operations that are a result of Kubernetes responding to unavoidable
incidents.

## Request filtering {#request-filtering}

This section provides recommendations for filtering which requests trigger
specific webhooks. In summary, these are as follows:

- Limit the webhook scope to avoid system components and read-only requests.
- Limit webhooks to specific namespaces.
- Use match conditions to perform fine-grained request filtering.
- Match all versions of an object.

### Limit the scope of each webhook {#webhook-limit-scope}

Admission webhooks are only called when an API request matches the corresponding
webhook configuration. Limit the scope of each webhook to reduce unnecessary
calls to the webhook server. Consider the following scope limitations:

- Avoid matching objects in the `kube-system` namespace. If you run your own
  Pods in the `kube-system` namespace, use an
  [`objectSelector`](/docs/reference/access-authn-authz/extensible-admission-controllers/#matching-requests-objectselector)
  to avoid mutating a critical workload.
- Don't mutate node leases, which exist as Lease objects in the
  `kube-node-lease` system namespace. Mutating node leases might result in
  failed node upgrades. Only apply validation controls to Lease objects in this
  namespace if you're confident that the controls won't put your cluster at
  risk.
- Don't mutate TokenReview or SubjectAccessReview objects. These are always
  read-only requests. Modifying these objects might break your cluster.
- Limit each webhook to a specific namespace by using a
  [`namespaceSelector`](/docs/reference/access-authn-authz/extensible-admission-controllers/#matching-requests-namespaceselector).

### Filter for specific requests by using match conditions {#filter-match-conditions}

Admission controllers support multiple fields that you can use to match requests
that meet specific criteria. For example, you can use a `namespaceSelector` to
filter for requests that target a specific namespace.

For more fine-grained request filtering, use the `matchConditions` field in your
webhook configuration. This field lets you write multiple CEL expressions that
must evaluate to `true` for a request to trigger your admission webhook. Using
`matchConditions` might significantly reduce the number of calls to your webhook
server.

For details, see
[Matching requests: `matchConditions`](/docs/reference/access-authn-authz/extensible-admission-controllers/#matching-requests-matchconditions).

### Match all versions of an API {#match-all-versions}

By default, admission webhooks run on any API versions that affect a specified
resource. The `matchPolicy` field in the webhook configuration controls this
behavior. Specify a value of `Equivalent` in the `matchPolicy` field or omit
the field to allow the webhook to run on any API version.

For details, see
[Matching requests: `matchPolicy`](/docs/reference/access-authn-authz/extensible-admission-controllers/#matching-requests-matchpolicy).

## Mutation scope and field considerations {#mutation-scope-considerations}

This section provides recommendations for the scope of mutations and any special
considerations for object fields. In summary, these are as follows:

- Patch only the fields that you need to patch.
- Don't overwrite array values.
- Avoid side effects in mutations when possible.
- Avoid self-mutations.
- Fail open and validate the final state.
- Plan for future field updates in later versions.
- Prevent webhooks from self-triggering.
- Don't change immutable objects.

### Patch only required fields {#patch-required-fields}

Admission webhook servers send HTTP responses to indicate what to do with a
specific Kubernetes API request. This response is an AdmissionReview object.
A mutating webhook can add specific fields to mutate before allowing admission
by using the `patchType` field and the `patch` field in the response. Ensure
that you only modify the fields that require a change.

For example, consider a mutating webhook that's configured to ensure that
`web-server` Deployments have at least three replicas. When a request to
create a Deployment object matches your webhook configuration, the webhook
should only update the value in the `spec.replicas` field.

### Don't overwrite array values {#dont-overwrite-arrays}

Fields in Kubernetes object specifications might include arrays. Some arrays
contain key:value pairs (like the `envVar` field in a container specification),
while other arrays are unkeyed (like the `readinessGates` field in a Pod
specification). The order of values in an array field might matter in some
situations. For example, the order of arguments in the `args` field of a
container specification might affect the container.

Consider the following when modifying arrays:

- Whenever possible, use the `add` JSONPatch operation instead of `replace` to
  avoid accidentally replacing a required value.
- Treat arrays that don't use key:value pairs as sets.
- Ensure that the values in the field that you modify aren't required to be
  in a specific order.
- Don't overwrite existing key:value pairs unless absolutely necessary.
- Use caution when modifying label fields. An accidental modification might
  cause label selectors to break, resulting in unintended behavior.

### Avoid side effects {#avoid-side-effects}

Ensure that your webhooks operate only on the content of the AdmissionReview
that's sent to them, and do not make out-of-band changes. These additional
changes, called _side effects_, might cause conflicts during admission if they
aren't reconciled properly. The `.webhooks[].sideEffects` field should
be set to `None` if a webhook doesn't have any side effect.

If side effects are required during the admission evaluation, they must be
suppressed when processing an AdmissionReview object with `dryRun` set to
`true`, and the `.webhooks[].sideEffects` field should be set to `NoneOnDryRun`.

For details, see
[Side effects](/docs/reference/access-authn-authz/extensible-admission-controllers/#side-effects).

### Avoid self-mutations {#avoid-self-mutation}

A webhook running inside the cluster might cause deadlocks for its own
deployment if it is configured to intercept resources required to start its own
Pods.

For example, a mutating admission webhook is configured to admit **create** Pod
requests only if a certain label is set in the Pod (such as `env: prod`).
The webhook server runs in a Deployment that doesn't set the `env` label.

When a node that runs the webhook server Pods becomes unhealthy, the webhook
Deployment tries to reschedule the Pods to another node. However, the existing
webhook server rejects the requests since the `env` label is unset. As a
result, the migration cannot happen.

Exclude the namespace where your webhook is running with a
[`namespaceSelector`](/docs/reference/access-authn-authz/extensible-admission-controllers/#matching-requests-namespaceselector).

### Avoid dependency loops {#avoid-dependency-loops}

Dependency loops can occur in scenarios like the following:

- Two webhooks check each other's Pods. If both webhooks become unavailable
  at the same time, neither webhook can start.
- Your webhook intercepts cluster add-on components, such as networking plugins
  or storage plugins, that your webhook depends on. If both the webhook and the
  dependent add-on become unavailable, neither component can function.

To avoid these dependency loops, try the following:

- Use
  [ValidatingAdmissionPolicies](/docs/reference/access-authn-authz/validating-admission-policy/)
  to avoid introducing dependencies.
- Prevent webhooks from validating or mutating other webhooks. Consider
  [excluding specific namespaces](/docs/reference/access-authn-authz/extensible-admission-controllers/#matching-requests-namespaceselector)
  from triggering your webhook.
- Prevent your webhooks from acting on dependent add-ons by using an
  [`objectSelector`](/docs/reference/access-authn-authz/extensible-admission-controllers/#matching-requests-objectselector).

### Fail open and validate the final state {#fail-open-validate-final-state}

Mutating admission webhooks support the `failurePolicy` configuration field.
This field indicates whether the API server should admit or reject the request
if the webhook fails. Webhook failures might occur because of timeouts or errors
in the server logic.

By default, admission webhooks set the `failurePolicy` field to Fail. The API
server rejects a request if the webhook fails. However, rejecting requests by
default might result in compliant requests being rejected during webhook
downtime.

Let your mutating webhooks "fail open" by setting the `failurePolicy` field to
Ignore. Use a validating controller to check the state of requests to ensure
that they comply with your policies.

This approach has the following benefits:

- Mutating webhook downtime doesn't affect compliant resources from deploying.
- Policy enforcement occurs during validating admission control.
- Mutating webhooks don't interfere with other controllers in the cluster.

### Plan for future updates to fields {#plan-future-field-updates}

In general, design your webhooks under the assumption that Kubernetes APIs might
change in a later version. Don't write a server that takes the stability of an
API for granted. For example, the release of sidecar containers in Kubernetes
added a `restartPolicy` field to the Pod API.

### Prevent your webhook from triggering itself {#prevent-webhook-self-trigger}

Mutating webhooks that respond to a broad range of API requests might
unintentionally trigger themselves. For example, consider a webhook that
responds to all requests in the cluster. If you configure the webhook to create
Event objects for every mutation, it'll respond to its own Event object
creation requests.

To avoid this, consider setting a unique label in any resources that your
webhook creates. Exclude this label from your webhook match conditions.

### Don't change immutable objects {#dont-change-immutable-objects}

Some Kubernetes objects in the API server can't change. For example, when you
deploy a {{< glossary_tooltip text="static Pod" term_id="static-pod" >}}, the
kubelet on the node creates a
{{< glossary_tooltip text="mirror Pod" term_id="mirror-pod" >}} in the API
server to track the static Pod. However, changes to the mirror Pod don't
propagate to the static Pod.

Don't attempt to mutate these objects during admission. All mirror Pods have the
`kubernetes.io/config.mirror` annotation. To exclude mirror Pods while reducing
the security risk of ignoring an annotation, allow static Pods to only run in
specific namespaces.

## Mutating webhook ordering and idempotence {#ordering-idempotence}

This section provides recommendations for webhook order and designing idempotent
webhooks. In summary, these are as follows:

- Don't rely on a specific order of execution.
- Validate mutations before admission.
- Check for mutations being overwritten by other controllers.
- Ensure that the set of mutating webhooks is idempotent, not just the
  individual webhooks.

### Don't rely on mutating webhook invocation order {#dont-rely-webhook-order}

Mutating admission webhooks don't run in a consistent order. Various factors
might change when a specific webhook is called. Don't rely on your webhook
running at a specific point in the admission process. Other webhooks could still
mutate your modified object.

The following recommendations might help to minimize the risk of unintended
changes:

- [Validate mutations before admission](#validate-mutations)
- Use a reinvocation policy to observe changes to an object by other plugins
  and re-run the webhook as needed. For details, see
  [Reinvocation policy](/docs/reference/access-authn-authz/extensible-admission-controllers/#reinvocation-policy).

### Ensure that the mutating webhooks in your cluster are idempotent {#ensure-mutating-webhook-idempotent}

Every mutating admission webhook should be _idempotent_. The webhook should be
able to run on an object that it already modified without making additional
changes beyond the original change.

Additionally, all of the mutating webhooks in your cluster should, as a
collection, be idempotent. After the mutation phase of admission control ends,
every individual mutating webhook should be able to run on an object without
making additional changes to the object.

Depending on your environment, ensuring idempotence at scale might be
challenging. The following recommendations might help:

- Use validating admission controllers to verify the final state of
  critical workloads.
- Test your deployments in a staging cluster to see if any objects get modified
  multiple times by the same webhook.
- Ensure that the scope of each mutating webhook is specific and limited.

The following examples show idempotent mutation logic:

1. For a **create** Pod request, set the field
   `.spec.securityContext.runAsNonRoot` of the Pod to true.

1. For a **create** Pod request, if the field
   `.spec.containers[].resources.limits` of a container is not set, set default
   resource limits.

1. For a **create** Pod request, inject a sidecar container with name
   `foo-sidecar` if no container with the name `foo-sidecar` already exists.

In these cases, the webhook can be safely reinvoked, or admit an object that
already has the fields set.

The following examples show non-idempotent mutation logic:

1. For a **create** Pod request, inject a sidecar container with name
   `foo-sidecar` suffixed with the current timestamp (such as
   `foo-sidecar-19700101-000000`).

   Reinvoking the webhook can result in the same sidecar being injected multiple
   times to a Pod, each time with a different container name. Similarly, the
   webhook can inject duplicated containers if the sidecar already exists in
   a user-provided pod.

1. For a **create**/**update** Pod request, reject if the Pod has label `env`
   set, otherwise add an `env: prod` label to the Pod.

   Reinvoking the webhook will result in the webhook failing on its own output.

1. For a **create** Pod request, append a sidecar container named `foo-sidecar`
   without checking whether a `foo-sidecar` container exists.

   Reinvoking the webhook will result in duplicated containers in the Pod, which
   makes the request invalid and rejected by the API server.

## Mutation testing and validation {#mutation-testing-validation}

This section provides recommendations for testing your mutating webhooks and
validating mutated objects. In summary, these are as follows:

- Test webhooks in staging environments.
- Avoid mutations that violate validations.
- Test minor version upgrades for regressions and conflicts.
- Validate mutated objects before admission.

### Test webhooks in staging environments {#test-in-staging-environments}

Robust testing should be a core part of your release cycle for new or updated
webhooks. If possible, test any changes to your cluster webhooks in a staging
environment that closely resembles your production clusters. At the very least,
consider using a tool like [minikube](https://minikube.sigs.k8s.io/docs/) or
[kind](https://kind.sigs.k8s.io/) to create a small test cluster for webhook
changes.

### Ensure that mutations don't violate validations {#ensure-mutations-dont-violate-validations}

Your mutating webhooks shouldn't break any of the validations that apply to an
object before admission. For example, consider a mutating webhook that sets the
default CPU request of a Pod to a specific value. If the CPU limit of that Pod
is set to a lower value than the mutated request, the Pod fails admission.

Test every mutating webhook against the validations that run in your cluster.

### Test minor version upgrades to ensure consistent behavior {#test-minor-version-upgrades}

Before upgrading your production clusters to a new minor version, test your
webhooks and workloads in a staging environment. Compare the results to ensure
that your webhooks continue to function as expected after the upgrade.

Additionally, use the following resources to stay informed about API changes:

- [Kubernetes release notes](/releases/)
- [Kubernetes blog](/blog/)

### Validate mutations before admission {#validate-mutations}

Mutating webhooks run to completion before any validating webhooks run. There is
no stable order in which mutations are applied to objects. As a result, your
mutations could get overwritten by a mutating webhook that runs at a later time.

Add a validating admission controller like a ValidatingAdmissionWebhook or a
ValidatingAdmissionPolicy to your cluster to ensure that your mutations
are still present. For example, consider a mutating webhook that inserts the
`restartPolicy: Always` field to specific init containers to make them run as
sidecar containers. You could run a validating webhook to ensure that those
init containers retained the `restartPolicy: Always` configuration after all
mutations were completed.

For details, see the following resources:

- [Validating Admission Policy](/docs/reference/access-authn-authz/validating-admission-policy/)
- [ValidatingAdmissionWebhooks](/docs/reference/access-authn-authz/admission-controllers/#validatingadmissionwebhook)

## Mutating webhook deployment {#mutating-webhook-deployment}

This section provides recommendations for deploying your mutating admission
webhooks. In summary, these are as follows:

- Gradually roll out the webhook configuration and monitor for issues by
  namespace.
- Limit access to edit the webhook configuration resources.
- Limit access to the namespace that runs the webhook server, if the server is
  in-cluster.

### Install and enable a mutating webhook {#install-enable-mutating-webhook}

When you're ready to deploy your mutating webhook to a cluster, use the
following order of operations:

1.  Install the webhook server and start it.
1.  Set the `failurePolicy` field in the MutatingWebhookConfiguration manifest
    to Ignore. This lets you avoid disruptions caused by misconfigured webhooks.
1.  Set the `namespaceSelector` field in the MutatingWebhookConfiguration
    manifest to a test namespace.
1.  Deploy the MutatingWebhookConfiguration to your cluster.

Monitor the webhook in the test namespace to check for any issues, then roll the
webhook out to other namespaces. If the webhook intercepts an API request that
it wasn't meant to intercept, pause the rollout and adjust the scope of the
webhook configuration.

### Limit edit access to mutating webhooks {#limit-edit-access}

Mutating webhooks are powerful Kubernetes controllers. Use RBAC or another
authorization mechanism to limit access to your webhook configurations and
servers. For RBAC, ensure that the following access is only available to trusted
entities:

- Verbs: **create**, **update**, **patch**, **delete**, **deletecollection**
- API group: `admissionregistration.k8s.io/v1`
- API kind: MutatingWebhookConfigurations

If your mutating webhook server runs in the cluster, limit access to create or
modify any resources in that namespace.

## Examples of good implementations {#example-good-implementations}

{{% thirdparty-content %}}

The following projects are examples of "good" custom webhook server
implementations. You can use them as a starting point when designing your own
webhooks. Don't use these examples as-is; use them as a starting point and
design your webhooks to run well in your specific environment.

- [`cert-manager`](https://github.com/cert-manager/cert-manager/tree/master/internal/webhook)
- [Gatekeeper Open Policy Agent (OPA)](https://open-policy-agent.github.io/gatekeeper/website/docs/mutation)

## {{% heading "whatsnext" %}}

- [Use webhooks for authentication and authorization](/docs/reference/access-authn-authz/webhook/)
- [Learn about MutatingAdmissionPolicies](/docs/reference/access-authn-authz/mutating-admission-policy/)
- [Learn about ValidatingAdmissionPolicies](/docs/reference/access-authn-authz/validating-admission-policy/)

---

title: Certificates
content_type: concept
weight: 20

---

<!-- overview -->

## To learn how to generate certificates for your cluster, see [Certificates](/docs/tasks/administer-cluster/certificates/).

title: Compatibility Version For Kubernetes Control Plane Components
reviewers:

- jpbetz
- siyuanfoundation
  content_type: concept
  weight: 70

---

<!-- overview -->

Since release v1.32, we introduced configurable version compatibility and emulation options to Kubernetes control plane components to make upgrades safer by providing more control and increasing the granularity of steps available to cluster administrators.

<!-- body -->

## Emulated Version

The emulation option is set by the `--emulated-version` flag of control plane components. It allows the component to emulate the behavior (APIs, features, ...) of an earlier version of Kubernetes.

When used, the capabilities available will match the emulated version:

- Any capabilities present in the binary version that were introduced after the emulation version will be unavailable.
- Any capabilities removed after the emulation version will be available.

This enables a binary from a particular Kubernetes release to emulate the behavior of a previous version with sufficient fidelity that interoperability with other system components can be defined in terms of the emulated version.

The `--emulated-version` must be <= `binaryVersion`. See the help message of the `--emulated-version` flag for supported range of emulated versions.---
reviewers:

- jpbetz
  title: Coordinated Leader Election
  content_type: concept
  weight: 200

---

<!-- overview -->

{{< feature-state feature_gate_name="CoordinatedLeaderElection" >}}

Kubernetes {{< skew currentVersion >}} includes a beta feature that allows {{<
glossary_tooltip text="control plane" term_id="control-plane" >}} components to
deterministically select a leader via _coordinated leader election_.
This is useful to satisfy Kubernetes version skew constraints during cluster upgrades.
Currently, the only builtin selection strategy is `OldestEmulationVersion`,
preferring the leader with the lowest emulation version, followed by binary
version, followed by creation timestamp.

## Enabling coordinated leader election

Ensure that `CoordinatedLeaderElection` [feature
gate](/docs/reference/command-line-tools-reference/feature-gates/) is enabled
when you start the {{< glossary_tooltip text="API Server"
term_id="kube-apiserver" >}}: and that the `coordination.k8s.io/v1beta1` API group is
enabled.

This can be done by setting flags `--feature-gates="CoordinatedLeaderElection=true"` and
`--runtime-config="coordination.k8s.io/v1beta1=true"`.

## Component configuration

Provided that you have enabled the `CoordinatedLeaderElection` feature gate _and_
have the `coordination.k8s.io/v1beta1` API group enabled, compatible control plane
components automatically use the LeaseCandidate and Lease APIs to elect a leader
as needed.

For Kubernetes {{< skew currentVersion >}}, two control plane components
(kube-controller-manager and kube-scheduler) automatically use coordinated
leader election when the feature gate and API group are enabled. ---
title: Good practices for Dynamic Resource Allocation as a Cluster Admin
content_type: concept
weight: 60

---

<!-- overview -->

This page describes good practices when configuring a Kubernetes cluster
utilizing Dynamic Resource Allocation (DRA). These instructions are for cluster
administrators.

<!-- body -->

## Separate permissions to DRA related APIs

DRA is orchestrated through a number of different APIs. Use authorization tools
(like RBAC, or another solution) to control access to the right APIs depending
on the persona of your user.

In general, DeviceClasses and ResourceSlices should be restricted to admins and
the DRA drivers. Cluster operators that will be deploying Pods with claims will
need access to ResourceClaim and ResourceClaimTemplate APIs; both of these APIs
are namespace scoped.

## DRA driver deployment and maintenance

DRA drivers are third-party applications that run on each node of your cluster
to interface with the hardware of that node and Kubernetes' native DRA
components. The installation procedure depends on the driver you choose, but is
likely deployed as a DaemonSet to all or a selection of the nodes (using node
selectors or similar mechanisms) in your cluster.

### Use drivers with seamless upgrade if available

DRA drivers implement the [`kubeletplugin` package
interface](https://pkg.go.dev/k8s.io/dynamic-resource-allocation/kubeletplugin).
Your driver may support _seamless upgrades_ by implementing a property of this
interface that allows two versions of the same DRA driver to coexist for a short
time. This is only available for kubelet versions 1.33 and above and may not be
supported by your driver for heterogeneous clusters with attached nodes running
older versions of Kubernetes - check your driver's documentation to be sure.

If seamless upgrades are available for your situation, consider using it to
minimize scheduling delays when your driver updates.

If you cannot use seamless upgrades, during driver downtime for upgrades you may
observe that:

- Pods cannot start unless the claims they depend on were already prepared for
  use.
- Cleanup after the last pod which used a claim gets delayed until the driver is
  available again. The pod is not marked as terminated. This prevents reusing
  the resources used by the pod for other pods.
- Running pods will continue to run.

### Confirm your DRA driver exposes a liveness probe and utilize it

Your DRA driver likely implements a gRPC socket for healthchecks as part of DRA
driver good practices. The easiest way to utilize this grpc socket is to
configure it as a liveness probe for the DaemonSet deploying your DRA driver.
Your driver's documentation or deployment tooling may already include this, but
if you are building your configuration separately or not running your DRA driver
as a Kubernetes pod, be sure that your orchestration tooling restarts the DRA
driver on failed healthchecks to this grpc socket. Doing so will minimize any
accidental downtime of the DRA driver and give it more opportunities to self
heal, reducing scheduling delays or troubleshooting time.

### When draining a node, drain the DRA driver as late as possible

The DRA driver is responsible for unpreparing any devices that were allocated to
Pods, and if the DRA driver is {{< glossary_tooltip text="drained"
term_id="drain" >}} before Pods with claims have been deleted, it will not be
able to finalize its cleanup. If you implement custom drain logic for nodes,
consider checking that there are no allocated/reserved ResourceClaim or
ResourceClaimTemplates before terminating the DRA driver itself.

## Monitor and tune components for higher load, especially in high scale environments

Control plane component {{< glossary_tooltip text="kube-scheduler"
term_id="kube-scheduler" >}} and the internal ResourceClaim controller
orchestrated by the component {{< glossary_tooltip
text="kube-controller-manager" term_id="kube-controller-manager" >}} do the
heavy lifting during scheduling of Pods with claims based on metadata stored in
the DRA APIs. Compared to non-DRA scheduled Pods, the number of API server
calls, memory, and CPU utilization needed by these components is increased for
Pods using DRA claims. In addition, node local components like the DRA driver
and kubelet utilize DRA APIs to allocated the hardware request at Pod sandbox
creation time. Especially in high scale environments where clusters have many
nodes, and/or deploy many workloads that heavily utilize DRA defined resource
claims, the cluster administrator should configure the relevant components to
anticipate the increased load.

The effects of mistuned components can have direct or snowballing affects
causing different symptoms during the Pod lifecycle. If the `kube-scheduler`
component's QPS and burst configurations are too low, the scheduler might
quickly identify a suitable node for a Pod but take longer to bind the Pod to
that node. With DRA, during Pod scheduling, the QPS and Burst parameters in the
client-go configuration within `kube-controller-manager` are critical.

The specific values to tune your cluster to depend on a variety of factors like
number of nodes/pods, rate of pod creation, churn, even in non-DRA environments;
see the [SIG Scalability README on Kubernetes scalability
thresholds](https://github.com/kubernetes/community/blob/master/sig-scalability/configs-and-limits/thresholds.md)
for more information. In scale tests performed against a DRA enabled cluster
with 100 nodes, involving 720 long-lived pods (90% saturation) and 80 churn pods
(10% churn, 10 times), with a job creation QPS of 10, `kube-controller-manager`
QPS could be set to as low as 75 and Burst to 150 to meet equivalent metric
targets for non-DRA deployments. At this lower bound, it was observed that the
client side rate limiter was triggered enough to protect the API server from
explosive burst but was high enough that pod startup SLOs were not impacted.
While this is a good starting point, you can get a better idea of how to tune
the different components that have the biggest effect on DRA performance for
your deployment by monitoring the following metrics. For more information on all
the stable metrics in Kubernetes, see the [Kubernetes Metrics
Reference](/docs/reference/instrumentation/metrics/).

### `kube-controller-manager` metrics

The following metrics look closely at the internal ResourceClaim controller
managed by the `kube-controller-manager` component.

- Workqueue Add Rate: Monitor {{< highlight promql "hl_inline=true"  >}} sum(rate(workqueue_adds_total{name="resource_claim"}[5m])) {{< /highlight >}} to gauge how quickly items are added to the ResourceClaim controller.
- Workqueue Depth: Track
  {{< highlight promql "hl_inline=true" >}}sum(workqueue_depth{endpoint="kube-controller-manager",
  name="resource_claim"}){{< /highlight >}} to identify any backlogs in the ResourceClaim
  controller.
- Workqueue Work Duration: Observe {{< highlight promql "hl_inline=true">}}histogram_quantile(0.99,
  sum(rate(workqueue_work_duration_seconds_bucket{name="resource_claim"}[5m]))
  by (le)){{< /highlight >}} to understand the speed at which the ResourceClaim controller
  processes work.

If you are experiencing low Workqueue Add Rate, high Workqueue Depth, and/or
high Workqueue Work Duration, this suggests the controller isn't performing
optimally. Consider tuning parameters like QPS, burst, and CPU/memory
configurations.

If you are experiencing high Workequeue Add Rate, high Workqueue Depth, but
reasonable Workqueue Work Duration, this indicates the controller is processing
work, but concurrency might be insufficient. Concurrency is hardcoded in the
controller, so as a cluster administrator, you can tune for this by reducing the
pod creation QPS, so the add rate to the resource claim workqueue is more
manageable.

### `kube-scheduler` metrics

The following scheduler metrics are high level metrics aggregating performance
across all Pods scheduled, not just those using DRA. It is important to note
that the end-to-end metrics are ultimately influenced by the
`kube-controller-manager`'s performance in creating ResourceClaims from
ResourceClainTemplates in deployments that heavily use ResourceClainTemplates.

- Scheduler End-to-End Duration: Monitor {{< highlight promql "hl_inline=true" >}}histogram_quantile(0.99,
  sum(increase(scheduler_pod_scheduling_sli_duration_seconds_bucket[5m])) by
  (le)){{< /highlight >}}.
- Scheduler Algorithm Latency: Track {{< highlight promql "hl_inline=true" >}}histogram_quantile(0.99,
  sum(increase(scheduler_scheduling_algorithm_duration_seconds_bucket[5m])) by
  (le)){{< /highlight >}}.

### `kubelet` metrics

When a Pod bound to a node must have a ResourceClaim satisfied, kubelet calls
the `NodePrepareResources` and `NodeUnprepareResources` methods of the DRA
driver. You can observe this behavior from the kubelet's point of view with the
following metrics.

- Kubelet NodePrepareResources: Monitor {{< highlight promql "hl_inline=true" >}}histogram_quantile(0.99,
  sum(rate(dra_operations_duration_seconds_bucket{operation_name="PrepareResources"}[5m]))
  by (le)){{< /highlight >}}.
- Kubelet NodeUnprepareResources: Track {{< highlight promql "hl_inline=true" >}}histogram_quantile(0.99,
  sum(rate(dra_operations_duration_seconds_bucket{operation_name="UnprepareResources"}[5m]))
  by (le)){{< /highlight >}}.

### DRA kubeletplugin operations

DRA drivers implement the [`kubeletplugin` package
interface](https://pkg.go.dev/k8s.io/dynamic-resource-allocation/kubeletplugin)
which surfaces its own metric for the underlying gRPC operation
`NodePrepareResources` and `NodeUnprepareResources`. You can observe this
behavior from the point of view of the internal kubeletplugin with the following
metrics.

- DRA kubeletplugin gRPC NodePrepareResources operation: Observe {{< highlight promql "hl_inline=true" >}}histogram_quantile(0.99,
  sum(rate(dra_grpc_operations_duration_seconds_bucket{method_name=~".\*NodePrepareResources"}[5m]))
  by (le)){{< /highlight >}}.
- DRA kubeletplugin gRPC NodeUnprepareResources operation: Observe {{< highlight promql "hl_inline=true" >}} histogram_quantile(0.99,
  sum(rate(dra_grpc_operations_duration_seconds_bucket{method_name=~".\*NodeUnprepareResources"}[5m]))
  by (le)){{< /highlight >}}.
