# 一图读懂现代网络与协议

<!-- yitu-r2-assets:start -->

## 相关文章配图

![一图读懂网络与协议](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E4%B8%80%E5%9B%BE%E8%AF%BB%E6%87%82%E7%BD%91%E7%BB%9C%E4%B8%8E%E5%8D%8F%E8%AE%AE.png)

![小红书：网络与协议](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E5%B0%8F%E7%BA%A2%E4%B9%A6-%E7%BD%91%E7%BB%9C%E4%B8%8E%E5%8D%8F%E8%AE%AE.png)

<!-- yitu-r2-assets:end -->
> **演进主线**：TCP/IP -> DNS / BGP -> HTTP -> Overlay -> CNI / Service Mesh -> eBPF / XDP -> AI Fabric -> AI Gateway / Agent Protocol

## 核心观点

如果把过去三十年的网络演进真正串起来看，你会发现，现代网络早就不再只是让机器互相连接。

它正在从“连接时代”，进入“数据面时代”，并进一步走向 AI Native 的“语义流量时代”。

过去网络关心的是包从哪里来到哪里去。未来网络还要理解：这个请求属于哪个模型、哪个 Agent、哪个租户、什么优先级、是否可信、是否需要低延迟推理。

## 从连接用户到连接系统

最早的互联网时代，网络目标很单纯：把数据从 A 点传到 B 点。

TCP/IP、DNS、BGP、HTTP 构建起整个互联网世界。DNS 告诉你去哪里，BGP 决定走哪条路，TCP 保证数据可靠到达，HTTP 让应用建立在互联网之上。

那个时代，网络核心是南北流量：用户访问网站，浏览器请求服务器，请求从公网进入数据中心，再返回用户终端。大家真正关心的是带宽够不够、链路稳不稳定、网站能不能被访问。

云计算与 Kubernetes 出现之后，网络世界开始发生变化。越来越多流量不再来自用户访问网站，而来自数据中心内部。Pod 与 Pod、Service 与 Service、Cluster 与 Cluster 开始频繁通信。

东西向流量第一次超过南北流量。网络从连接用户，变成连接系统。

## Overlay 用开销换灵活

VXLAN、Geneve、GRE、IPIP、Open vSwitch 的出现，本质上都在做一件事：用封装换灵活性，让网络脱离物理交换机，变成软件可编排的数据平面。

于是 CNI、SDN、Overlay Network、Service Discovery、Load Balancing 快速崛起。

但 Overlay 从来不是免费的。封装意味着 MTU 损耗、CPU 消耗、PPS 压力和额外延迟。过去 Web 流量还能容忍这些开销，但 AI 时代之后，网络第一次重新回到 HPC 级别的竞争。

## AI 集群让网络重新变贵

AI 集群真正可怕的地方，不是 GPU 算不动，而是 GPU 在等待网络。

大模型训练和推理本质上是在做超高频分布式通信。NCCL、AllReduce、Tensor Parallel、Pipeline Parallel、KV Cache 同步，都会疯狂消耗网络。

模型规模进入 70B、100B+ 之后，真正决定系统上限的，往往不是 GPU FLOPS，而是网络带宽、延迟和拥塞控制能力。

于是 RDMA、RoCEv2、InfiniBand、DPDK、GPUDirect RDMA 又重新变得重要。AI 网络本质上已经不再是传统互联网网络，而是分布式超级计算网络。

很多时候 GPU 没满载，不是因为算力不够，而是在等网络。

## Linux Kernel 成为数据面核心

容器网络底层最终还是 Linux 网络栈。

真正决定性能上限的，不只是网卡驱动和协议栈，而是 netfilter、tc、RSS/RPS、XDP、eBPF、cgroups 与内核数据路径。

Cilium、eBPF、XDP 的崛起，说明网络正在重新进入“内核化时代”。网络不只是转发流量，而是承担服务发现、安全策略、可观测性、流量治理和高性能数据面。

## 从 API Gateway 到 AI Gateway

Kubernetes 又进一步把网络复杂度推向新阶段。

CNI 数据面、Service Mesh、API Gateway、多集群网络、跨云路由、零信任策略、AI 调度网络，全部开始堆积在 Kubernetes 周围。Istio、Linkerd、Envoy、APISIX、Kong、Gateway API、Multi-Cluster Networking 代表了这条路线。

过去 HTTP API 已经不够，gRPC 解决高性能 RPC 通信。传统 Service Mesh 解决服务治理，而 AI Gateway 又开始接管模型路由、多模型调度、Token Streaming 与 Agent 通信。

网络世界正在从传输数据，逐渐变成理解流量。

## 一图结构

| 阶段 | 核心变化 | 代表技术 |
|---|---|---|
| 互联网网络 | 连接用户与网站 | TCP/IP、DNS、BGP、HTTP |
| 数据中心网络 | 南北流量进入数据中心 | VLAN、Router、Switch、STP |
| Overlay / SDN | 网络软件化与可编排 | VXLAN、Geneve、Open vSwitch、OpenFlow |
| Kubernetes 网络 | Pod / Service 数据面 | CNI、Calico、Cilium、Service Mesh |
| 内核数据面 | 可观测和高性能转发进入 Kernel | eBPF、XDP、tc、RSS/RPS |
| AI Fabric | GPU 间高速通信 | RDMA、RoCEv2、InfiniBand、NVLink、NCCL |
| AI Gateway | 模型、Agent 与语义流量治理 | AI Gateway、MCP、Agent Protocol |

## 一句话总结

现代网络已经不再只是路由器与交换机。它正在演变成一套从 Linux Kernel、eBPF / XDP、Overlay Network、Service Mesh、API Gateway、Multi-Cluster，到 AI Gateway 与 Agent Protocol 的超大规模数据面系统。

网络，已经从连接时代进入数据面时代。

## 封面图提示词

低信息密度封面图，主题为“网络从连接进入数据面”。画面左侧是传统互联网路径：User -> Web -> Data Center；中间是 Kubernetes 数据面：Pods / Services / Gateway；右侧是 AI Fabric：GPU Cluster / RDMA / AI Gateway。只保留三段大路径和少量箭头，不展示密集协议清单。视觉风格为深蓝科技线框图，适合书籍章节封面。

## 延伸阅读

- 书籍第 2 章：[网络与协议](../../02-networking-protocols.md)
- [从 C10k 到 AI Fabric：高并发战争](../deep-dive/c10k-to-ai-fabric.md)
