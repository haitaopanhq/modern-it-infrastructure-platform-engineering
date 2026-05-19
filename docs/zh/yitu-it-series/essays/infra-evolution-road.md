# IT 基础设施演进之路

> **演进主线**：Hardware → Virtualization → Cloud Control Plane → Runtime → Network → Orchestration → AI Infra

## 核心观点

**过去十几年基础设施演进串起来看，Kubernetes 更像一个时代的"中间层"，而不是最终答案。**

## 全文

如果把过去二十多年的基础设施演进真正串起来看，你会发现，整个 IT 世界其实一直在围绕同一个问题反复演化：如何让不断增长的业务，能够突破单机、单机房、单团队、甚至单时代技术栈的限制继续扩张。

很多人后来把这些变化拆分成不同的技术名词，但如果站在更长时间尺度回头看，它们其实是一条连续演进的基础设施历史。现代基础设施越来越像一条不断上升的路径：

```
Hardware → Virtualization → Cloud Control Plane → Runtime → Network → Orchestration → AI Infra
```

### 硬件时代

最早的时代，基础设施的核心从来不是软件，而是硬件。CPU 主频、内存容量、磁盘 IO、网络带宽，直接决定系统上限。

### 虚拟化时代

互联网爆发之后，企业第一次发现：真正限制业务增长的，并不只是代码，而是资源无法被灵活利用。于是虚拟化时代开始。
虚拟化真正改变世界的地方，并不是"虚拟机"本身，而是它第一次让计算资源脱离物理机器，被抽象成可动态调度的资源池。

后来这种抽象开始继续扩张：
- Ceph 把存储池化
- Open vSwitch 把网络虚拟化
- CSI、CNI、CRI 逐渐形成标准接口

**硬件不再属于某一台机器，而属于整个数据中心。**

### Cloud Control Plane 时代

资源池化之后，一个更大的问题出现：谁来管理这些资源？

于是 Cloud Control Plane 时代开始到来。AWS、OpenStack、Harvester 这些平台真正重要的地方，并不是底层虚拟化技术本身，而是它们第一次把基础设施变成了"统一控制平面"。

企业终于可以像管理一个操作系统一样管理整个数据中心。创建机器、分配网络、挂载存储、调度资源，进入 API 驱动时代。

### Kubernetes 时代

接下来，Kubernetes 出现了。它更像一种"分布式容器操作系统"，统一了 Runtime 与 Orchestration 之间的关系。

于是 Kubernetes 开始快速吞噬整个行业：数据库跑 K8s，存储跑 K8s，AI 跑 K8s，虚拟机跑 K8s。整个行业逐渐进入"Kubernetes Everything"的状态。

但任何一个成功到极致的中间层，最后都会开始暴露自己的边界。很多企业后来发现，自己管理的已经不是业务，而是 Kubernetes 本身。

### AI Infra 时代

AI Infra 正在重新打破这个结构。传统 Web Infra 关注 HTTP 请求、副本数、弹性扩缩容和服务治理；AI Infra 更关注 GPU 调度、KV Cache、显存拓扑、RDMA、Tensor Parallel、Pipeline Parallel、Token 延迟。

它们已经不是同一种问题。

所以 vLLM、Ray、TensorRT-LLM、SGLang、Triton 开始快速崛起。AI 时代并没有让硬件变得不重要，反而让 GPU、NVLink、HBM、RDMA、高速网络、Linux Kernel、eBPF、cgroups 重新成为系统上限。

**基础设施又回到那个最原始的问题：如何让硬件资源被更高效地利用。**

## 未来趋势

未来 Kubernetes 不会消失。但它很可能会逐渐"下沉"，像 Linux 一样，成为基础设施默认存在的底座。真正继续向上生长的，将是 AI Gateway、GPU Scheduler、Inference Fabric、Semantic Cache、Agent Runtime。

Cloud Native 并没有结束，它只是正在进入下一阶段：**AI Native**。

## 延伸阅读

- 书籍序章：[IT 基础设施演进之路](../../00-it-infrastructure-evolution-road.md)
- [虚拟化从未消失：从大型机诞生那一天，它就一直在演变](./virtualization-never-died.md)
- [AI 会重新定义下一代基础设施吗？](./ai-redefine-infra.md)
