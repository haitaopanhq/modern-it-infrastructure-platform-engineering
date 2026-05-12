# 01-01: 一图看懂 Linux 为什么从未离开基础设施核心

## 核心观点

Linux 从未离开基础设施核心，它只是从机房里显眼的服务器操作系统，变成了云平台、容器平台和 AI 集群背后的共同运行时。今天开发者看到的是 Kubernetes API、云控制台、Serverless 平台或模型服务端点，但真正负责进程调度、内存回收、文件系统、网络协议栈、设备驱动和安全边界的，仍然是 Linux Kernel。

这篇图的重点不是怀旧，而是提醒平台工程团队：抽象层越高，越不能忘记底层约束。容器的隔离来自 namespace，资源限制来自 cgroups，网络可观测和数据面加速越来越依赖 eBPF，GPU、DPU、NVMe 与 RDMA 又把驱动、内核模块和 I/O 路径重新推到前台。Linux 没有退场，只是换了位置。

## 图表结构

```
应用与平台体验
  -> Kubernetes / Serverless / AI Gateway
  -> OCI Runtime / containerd / CRI
  -> syscall / cgroups / namespace / seccomp / eBPF
  -> Linux Kernel
  -> CPU / Memory / Disk / NIC / GPU / DPU
```

这张图用自上而下的方式表达一件事：用户入口可以不断变化，但每一次资源申请、网络收发、文件读写、容器启动和设备调用，最终都会落到内核对象上。Kubernetes 管 Pod，不直接调度 CPU 指令；云厂商卖实例，也必须通过内核和 Hypervisor 管理真实硬件；AI 平台提供模型 API，但显存、PCIe、NVLink 和驱动版本决定了服务上限。

读这张图时要特别注意“抽象”和“责任”的区别。抽象可以让用户少接触底层命令，但责任不会凭空消失。平台把 Linux 包装成更易用的接口，也必须继续承担补丁、参数、权限、驱动和观测责任。

## 演进脉络

早期基础设施以物理机为中心，Linux 是管理员直接登录、调优和排障的对象。虚拟化普及后，Linux 一部分变成 Guest OS，一部分作为 KVM、存储节点、网络节点和宿主机继续存在。云计算时代，Linux 被云控制面隐藏起来，用户更关心规格、镜像和弹性伸缩。

容器时代再次改变了可见层：Docker、containerd 和 Kubernetes 把 Linux 的 namespace、cgroups、capabilities、iptables/nftables 包装成声明式接口。到了 AI 基础设施阶段，Linux 又因为 GPU 驱动、RDMA、DPU、NUMA、HugePages 和内核旁路能力重新暴露。越是高性能场景，越不能只看 YAML 和控制台。

## 关键技术栈

| 技术 | 作用 | 平台工程关注点 |
| --- | --- | --- |
| cgroups v2 | CPU、内存、I/O 限制与统计 | 配额、隔离、压测基线 |
| namespace | 进程、网络、挂载等隔离 | 容器边界与逃逸风险 |
| seccomp/capabilities | 收敛系统调用与权限 | 最小权限运行时 |
| eBPF | 内核可编程观测与数据面 | 网络、安全、性能诊断 |
| io_uring/NVMe/RDMA | 高性能 I/O 路径 | 数据密集与 AI 训练吞吐 |
| GPU/DPU 驱动 | 异构设备接入 | 版本、拓扑、故障域管理 |

## 误区与现实

- 误区：有了 Kubernetes，就不需要理解 Linux。现实：Kubernetes 只是把 Linux 能力产品化，故障仍会以内核、网络、存储和驱动问题的形式出现。
- 误区：容器是完整虚拟机。现实：容器共享宿主机内核，隔离强度、补丁节奏和系统调用策略都依赖宿主机。
- 误区：云厂商会屏蔽所有底层差异。现实：实例规格、内核版本、网卡能力、NUMA 拓扑和加速卡型号都会影响性能与稳定性。

## 最佳实践

平台团队应把 Linux 作为运行时事实源之一纳入设计，而不是只在事故时才打开 `dmesg`。容量规划要同时看 CPU、内存、I/O、网络和设备拓扑；容器基线要统一 cgroups v2、seccomp、内核参数和镜像运行权限；可观测性要覆盖系统调用延迟、网络丢包、磁盘队列、内核错误和 GPU 驱动状态。

对于 AI 与高性能场景，建议在上线前建立节点画像：内核版本、驱动版本、GPU/NIC 亲和关系、NUMA 拓扑、RDMA 配置和 HugePages 策略都要进入交付清单。平台抽象可以简化体验，但不能删除物理现实。

更进一步，平台团队应把 Linux 基线当作产品版本管理。哪些内核参数允许业务覆盖，哪些驱动必须随节点池一起升级，哪些 eBPF 程序可以进入生产，哪些系统调用需要默认禁用，都应有明确策略。这样做不是增加运维负担，而是避免每个业务在事故中重新学习同一套底层知识。

在内容表达上，这篇图也可以作为排障入口：当一个 Pod 慢、一个模型服务抖动、一次网络请求丢包时，读者应能沿着“应用 -> Runtime -> 内核 -> 设备”的路径往下追。只要这条路径仍然成立，Linux 就仍然是现代基础设施的核心语言。

## 与长文互链

- 长文计划：[01-LF-01: 从 Linux 内核到平台工程：基础设施控制权为什么总会回到底层](../longform/01-foundation-control-power.md)
- 相关短文：[01-02: AI 为什么重新回到裸金属](../02-hardware/02-ai-back-to-baremetal.md)
- 相关短文：[01-05: 从 BIOS 到 Kubernetes](../05-bios-k8s/05-bios-to-kubernetes.md)

## 关键词

Linux Kernel, cgroups, namespace, eBPF, containerd, Kubernetes, GPU 驱动, DPU, 平台工程, AI 基础设施
