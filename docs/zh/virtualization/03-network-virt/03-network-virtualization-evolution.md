# 02-03: 一图看懂网络虚拟化演进

## 核心观点

网络虚拟化的核心，是把物理交换机、网段、路由、安全策略和负载均衡能力，抽象成可以随工作负载移动的逻辑网络。它从 VLAN 的二层隔离开始，发展到虚拟交换机、VXLAN Overlay、SDN 控制器、Kubernetes CNI、eBPF 数据面和服务网格，让网络从“机房布线问题”变成“平台 API 问题”。

这条演进线解决了规模和敏捷性，也引入了新的复杂度。Overlay 可以突破 VLAN 数量限制，但带来封装开销和排障难度；CNI 可以让 Pod 自动入网，但网络策略、DNS、负载均衡和跨集群通信仍然需要清晰设计。网络虚拟化越成熟，越需要统一控制面和可观测性。

很多人以为，网络只是“连接机器”。但如果真正回看过去二十年的基础设施演进，会发现网络其实一直在从“连接系统”逐渐变成“数据面系统”。它不再只是把服务器、用户和应用接起来，而是在不断承担隔离、调度、治理、观测和高性能通信能力。

最早的传统网络时代，核心是 VLAN、Router、Switch、STP。那个时代的网络以硬件设备为中心，主要解决南北向流量、用户访问和基础隔离问题。网络规划几乎是静态的：先设计网段、交换机、路由、ACL 和防火墙，再让业务进入这套拓扑。它稳定、清晰，但扩展能力有限，也很难适应虚拟机和云平台快速变化的生命周期。

后来 Overlay Network 开始出现。VXLAN、GRE、Open vSwitch 让网络第一次真正拥有“虚拟化能力”。网络不再完全依赖物理拓扑，而开始通过隧道、虚拟交换机和逻辑网络实现隔离。应用和租户看到的不再是某个交换机端口，而是可以跨主机、跨机架、跨资源池移动的逻辑网络。网络第一次开始脱离物理交换机，形成“逻辑网络”。

再后来，行业进入 SDN 与 NFV 时代。OpenFlow、NSX、SDN Controller 开始把控制面与数据面分离；防火墙、负载均衡、网关、EPC 等网络设备，也开始从专用硬件转向软件化网络功能。网络第一次真正进入“可编排时代”：策略可以由控制器下发，流表可以被程序修改，网络功能可以像软件一样部署、扩缩和迁移。

随着云计算与高性能网络继续发展，行业又开始重新关注数据面性能。DPDK 出现后，网络大规模进入“用户态高速转发”时代。过去大量网络包需要经过 Linux Kernel 网络栈，而 DPDK 通过用户态 Polling、HugePage、零拷贝与绕过内核协议栈，大幅降低网络转发延迟。于是虚拟交换机、NFV、vRouter、高性能网关开始真正具备接近专用设备的吞吐能力。

Kubernetes 普及后，CNI、Flannel、Calico、Cilium、eBPF 又继续把网络推进到云原生时代。网络开始不只是转发流量，而是承担服务发现、安全、可观测性与策略治理。eBPF 让 Linux Kernel 的网络数据面第一次真正变得“可编程”；XDP 更进一步，把部分过去在用户态或专用设备里的能力，重新带回 Kernel Datapath，并逐渐靠近 NIC 与硬件卸载层。

AI Infra 出现后，网络再次发生巨大变化。传统互联网以南北向流量与 Scale-Out 为主，而 AI Cluster 开始变成典型的东西向通信与 Scale-Up 系统。GPU 与 GPU 之间需要大量同步通信，于是行业重新追求“低延迟、高吞吐、零拷贝”的高速互联能力。

HPC 世界长期使用 InfiniBand，后来 RDMA 成为核心通信模型，RoCE 进一步把 RDMA 带入以太网体系。NVLink 负责 GPU 之间的本地高速互联，NCCL 则在这些高速通信能力之上，实现 GPU 集群间的并行通信与 AllReduce。AI 时代真正开始让网络从“请求转发”变成“算力互联”。

## 图表结构

```
传统物理网络
  -> VLAN / ACL / L2-L3 设备配置
虚拟化网络
  -> Linux Bridge / Open vSwitch / vNIC
Overlay 网络
  -> VXLAN / Geneve / GRE
SDN / NFV
  -> OpenFlow / NSX / SDN Controller / vRouter
云原生网络
  -> CNI / NetworkPolicy / Service / Ingress
可编程数据面
  -> DPDK / eBPF / XDP / DPU 卸载
服务通信层
  -> API Gateway / Service Mesh / mTLS
AI 高速互联
  -> InfiniBand / RDMA / RoCE / NVLink / NCCL
```

图表的关键是网络边界从交换机端口移动到了工作负载附近。虚拟机的 vNIC、容器的 veth、Pod 的 IP、服务的 VIP 和网格的 Sidecar 都是网络抽象的一部分。物理 Underlay 仍然重要，但租户和应用看到的是逻辑网络。

这也让排障视角发生变化。过去网络问题常从交换机端口查起，现在同一次失败可能跨越 DNS、Service、CNI、主机路由、Overlay 隧道、负载均衡和服务网格。图中的每一层都可能改写源地址、目标地址、端口、证书或策略，缺少链路视图就很难定位。

## 演进脉络

VLAN 解决了早期多业务隔离，但 4096 个 ID 很快无法支撑大规模云平台。虚拟交换机让同一台宿主机上的虚拟机可以像接入交换机一样通信，Open vSwitch 又把隧道、流表和 SDN 控制能力带入主机。这个阶段的关键变化，是网络开始从硬件端口迁移到宿主机内部，网络边界第一次贴近工作负载。

VXLAN/Geneve 等 Overlay 技术把二层网络封装在三层网络之上，让逻辑网络可以跨机架、跨可用区扩展。SDN 控制器继续把网络意图、策略和流表下发变成可编排能力，NFV 则把过去依赖专用设备的防火墙、负载均衡、网关和电信核心网功能迁移到通用服务器上。

性能压力随后把行业推向数据面加速。DPDK、SR-IOV、SmartNIC、DPU 解决的是同一个问题：当网络功能被软件化之后，数据包仍然必须高速转发。控制面可以越来越抽象，但数据面不能无限变慢。现代网络架构真正困难的地方，也正在于控制面的灵活性和数据面的性能上限必须同时成立。

Kubernetes 进一步要求网络按 Pod 生命周期自动创建，CNI 插件因此成为平台关键组件。近年 eBPF 数据面减少 iptables 规则膨胀，让策略、负载均衡、观测和安全逻辑可以在内核数据面中执行。XDP 把处理位置继续前移到更靠近网卡的位置，DPU 则把部分网络、安全和存储处理卸载到硬件侧。

同时，南北向入口也从单一负载均衡演进为 Ingress、Gateway API、API Gateway 和 Service Mesh 的组合。网络虚拟化不再只处理连通性，还要承载发布策略、证书、安全策略、审计和可观测数据。

AI 集群又把这条线继续推向高速互联。Web 时代最重要的是大量用户请求能否进入系统，云原生时代最重要的是服务之间能否被治理，AI 时代最重要的是 GPU 之间能否以极低延迟同步数据。InfiniBand、RDMA、RoCE、NVLink、NCCL 和 GPU Direct 说明，网络已经从“请求通道”变成“算力系统的一部分”。

因此，网络平台既是连接系统，也是治理系统，更是现代数据面的核心组成。

## 关键技术栈

| 技术 | 作用 | 平台工程关注点 |
| --- | --- | --- |
| VLAN/VRF | 基础隔离与路由域 | 物理网络规划与边界 |
| Linux Bridge/OVS | 主机虚拟交换 | VM/容器接入与隧道 |
| VXLAN/Geneve | Overlay 封装 | MTU、Underlay、VTEP |
| SDN Controller | 控制面与数据面分离 | 策略下发、流表、故障域 |
| DPDK | 用户态高速转发 | HugePage、CPU 绑核、延迟 |
| CNI | Kubernetes 网络插件接口 | IPAM、策略、性能 |
| Calico/Cilium | 云原生网络实现 | BGP、eBPF、NetworkPolicy |
| eBPF/XDP | 内核可编程数据面 | 负载均衡、观测、安全、加速 |
| RDMA/RoCE/NVLink/NCCL | AI 与 HPC 高速互联 | 拓扑、拥塞控制、GPU 通信效率 |
| Ingress/Gateway API | 南北向流量入口 | TLS、路由、发布治理 |
| Service Mesh | 服务间通信治理 | mTLS、流量策略、观测成本 |

## 误区与现实

- 误区：Overlay 让物理网络不重要。现实：Underlay 的丢包、MTU、拥塞和路由收敛会直接影响 Overlay。
- 误区：CNI 只是安装插件。现实：CNI 决定 IP 地址、策略、性能、排障方式和跨集群演进路径。
- 误区：Service Mesh 能解决所有网络问题。现实：网格主要解决服务通信治理，不替代基础网络、DNS 和负载均衡设计。
- 误区：AI 网络只是带宽更大的普通网络。现实：GPU 集群关注拓扑、延迟、拥塞、零拷贝和集体通信效率，问题模型已经不同。

## 最佳实践

网络设计要先区分 Underlay、Overlay、服务入口和东西向治理。Underlay 追求稳定、简单和可观测；Overlay 负责租户与工作负载隔离；Ingress/Gateway 负责发布入口；服务网格只在需要细粒度策略、mTLS 和可观测时引入。

平台团队应建立端到端排障路径：从 Pod DNS、Service、CNI、主机路由、隧道封装、物理交换机到对端应用都要有指标和抓包方法。AI 集群还要单独关注 RDMA、RoCE、ECN、PFC 和多网卡拓扑，不能把训练网络当普通业务网。

网络变更管理也要适应虚拟化后的速度。过去改一个 VLAN 可能走机房流程，现在一个应用发布就可能创建 Service、Ingress、证书、策略和 DNS 记录。平台需要用策略即代码、准入校验和自动回滚控制风险，否则逻辑网络的敏捷性会变成不可见的复杂度。

对开发者而言，理想体验是“声明服务意图”，而不是学习所有网络设备命令。对平台团队而言，理想状态是每一次逻辑网络变更都能追溯到提交、审批、策略和运行指标。二者结合，网络虚拟化才真正服务平台工程。

面向 AI Infra，网络还要从业务网络中单独建模。训练网络、存储网络、管理网络和用户访问网络不应混成一套模糊拓扑。GPU 集群需要把 NUMA、PCIe、NVLink、RDMA 网卡、交换机层级、拥塞控制和作业调度放在同一张图里看。否则平台看到的是“网络可达”，训练作业感受到的却是吞吐下降、同步变慢和 GPU 空转。

## 与长文互链

- 长文计划：[02-LF-01: 从虚拟机到云原生沙箱：虚拟化为什么仍是平台底座](../longform/02-virtualization-platform-foundation.md)
- 相关短文：[02-01: 计算虚拟化演进](../01-compute-virt/01-compute-virtualization-evolution.md)
- 相关短文：[02-04: 资源池化历史](../04-resource-pooling/04-resource-pooling.md)

## 关键词

网络虚拟化, VLAN, Open vSwitch, VXLAN, Geneve, SDN, NFV, DPDK, CNI, Calico, Cilium, eBPF, XDP, RDMA, RoCE, NVLink, NCCL, Service Mesh, Gateway API
