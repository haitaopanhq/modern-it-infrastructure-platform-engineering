# IT 基础设施演进之路

> **演进主线**：Hardware -> Virtualization -> Cloud Control Plane -> Runtime -> Network -> Orchestration -> AI Infra

## 核心观点

过去十几年基础设施演进如果真正串起来看，Kubernetes 更像一个时代性的“中间层”，而不是最终答案。

现代基础设施的演进路径，越来越像这样：

```text
Hardware
  -> Virtualization
  -> Cloud Control Plane
  -> Runtime
  -> Network
  -> Orchestration
  -> AI Infra
```

这条路径背后真正不变的问题是：如何让不断增长的业务，突破单机、单机房、单团队、单云厂商、甚至单时代技术栈的限制继续扩张。

## 硬件从未退场

很多人以前总觉得，软件会越来越抽象，硬件的重要性会越来越低。

但 AI 时代恰恰反了。

GPU、NVMe、RDMA、高速网络、Linux Kernel、eBPF、cgroups，这些过去被很多业务团队忽视的底层能力，重新变成决定系统上限的核心。因为大模型训练和推理最终拼的，不只是“算力”，而是显存容量、带宽、通信延迟、IO 吞吐和 GPU Feeding 能力。

AI Infra 的残酷现实是：当模型规模进入 30B、70B、100B+ 之后，真正先被打爆的，往往不是 CPU，而是显存、网络和调度系统。

这让基础设施重新回到最原始的问题：

> 如何让昂贵硬件被更高效、更稳定、更可治理地使用。

## 虚拟化不是虚拟机，而是资源池化

最早的基础设施核心，是虚拟化。

但今天的虚拟化，早就不只是 KVM、QEMU、VMware 这类“虚拟机技术”。它更像一种资源池化世界观：把计算、存储、网络和 IO 从离散硬件中抽离出来，变成可以统一调度、隔离、迁移和回收的资源。

Ceph 把存储池化，Open vSwitch 把网络虚拟化，SR-IOV 和 DPDK 重新定义高性能网络路径，CSI、CNI、CRI 把存储、网络和运行时抽象成标准接口。它们表面上属于不同技术领域，本质上都在做同一件事：

> 把离散硬件抽象成可统一调度的资源池。

硬件不再只属于某一台机器，而开始属于整个数据中心。

## Cloud Control Plane 接管资源

资源池化之后，一个更大的问题出现了：谁来管理这些资源？

于是 Cloud Control Plane 到来。AWS、OpenStack、Harvester 这些平台真正重要的地方，并不是底层虚拟化技术本身，而是它们第一次把基础设施变成统一控制平面。

企业终于可以像管理一个操作系统一样管理整个数据中心。创建虚拟机、分配网络、挂载存储、调度资源，不再完全依赖人工操作，而开始进入 API 驱动时代。

后来很多人把这种变化称作“云”，但云真正改变的，从来不只是机器部署方式，而是基础设施第一次拥有了统一控制能力。企业开始相信：资源可以按需申请，流量可以弹性吸收，系统可以通过控制面持续收敛。

## Kubernetes 是中间层时代

接下来，Kubernetes 出现了。

如果放在更长历史周期里看，它更像一种分布式容器操作系统，统一了 Runtime 与 Orchestration 之间的关系。Mesos、Docker Swarm 也曾试图成为这个时代的答案，但它们没有形成完整生态，也没有形成行业事实标准。真正活下来的，只剩 Kubernetes。

于是 Kubernetes 开始快速吞噬整个行业：数据库跑 K8s，存储跑 K8s，边缘计算跑 K8s，虚拟机跑 K8s，CI/CD 跑 K8s，监控跑 K8s，AI 也开始跑 K8s。

整个行业逐渐进入“Kubernetes Everything”的状态。

但任何一个成功到极致的中间层，最后都会开始暴露自己的边界。很多企业后来发现，自己管理的已经不是业务，而是 Kubernetes 本身。

YAML、Operator、CRD、Service Mesh、Overlay Network、CSI、CNI、GPU Plugin、Ingress、Gateway API……复杂度开始不断向平台层堆积。Cloud Native 原本是为了解决复杂系统治理，但随着规模继续增长，它自己也逐渐变成新的复杂度中心。

## AI Infra 打破云原生结构

AI Infra 正在重新打破传统 Cloud Native 的结构。

传统 Web Infra 关注的是 HTTP 请求、副本数、弹性扩容、服务治理、微服务链路。AI Infra 更关注 GPU 调度、KV Cache、显存拓扑、分布式推理、Tensor Parallel、Pipeline Parallel、Token 延迟、多模型路由和 Inference Gateway。

这两者已经不是同一种问题。

于是 vLLM、Ray、TensorRT-LLM、SGLang、Triton 开始快速崛起。它们解决的，已经不是 Kubernetes 最擅长的问题，而是 AI 时代的硬件效率、推理吞吐、显存管理、任务编排和模型服务问题。

AI Infra 的核心矛盾，正在从“服务调度”重新回到“硬件调度”。过去软件抽象让硬件看起来被隐藏了；AI 时代则重新让 GPU、NVLink、HBM、RDMA、高速网络、Linux Kernel、eBPF、cgroups 成为系统性能真正的决定因素。

## Kubernetes 会下沉

未来 Kubernetes 大概率不会消失。

它已经像 Linux 一样，变成一种基础设施默认存在的底座。但它很可能会逐渐下沉，成为 Cloud Control Plane 与 Runtime 之间的标准层。真正继续向上生长的，将是 AI Gateway、GPU Scheduler、Inference Fabric、Semantic Cache、Agent Runtime 这些全新的 AI Native 基础设施。

Cloud Native 没有结束。

它只是正在进入下一阶段：

> AI Native。

## 读者问题

你觉得未来 AI Infra 最终会继续建立在 Kubernetes 之上，还是会出现一套新的 AI 原生控制平面，重新定义下一代基础设施？

## 延伸阅读

- 书籍序章：[IT 基础设施演进之路](../../00-it-infrastructure-evolution-road.md)
- [AI 会重新定义下一代基础设施吗？](./ai-redefine-infra.md)
