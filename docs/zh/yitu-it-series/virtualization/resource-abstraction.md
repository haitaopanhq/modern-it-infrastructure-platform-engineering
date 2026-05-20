# 一图看懂 资源抽象史

<!-- yitu-r2-assets:start -->

## 相关文章配图

![资源抽象史](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E8%99%9A%E6%8B%9F%E5%8C%96/%E8%B5%84%E6%BA%90%E6%8A%BD%E8%B1%A1%E5%8F%B2.png)

<!-- yitu-r2-assets:end -->
> **演进主线**：Linux 资源抽象 → VPS/Hypervisor → KVM 统一 → 云原生 → AI Infra

## 核心观点

**现代基础设施的本质是资源抽象能力的演进。**

很多人以为，现代基础设施的核心是 Kubernetes、Docker，甚至 AI。但如果把过去二十多年 IT 演进真正串起来看，会发现整个行业持续演进的主线，一直都是“资源抽象”。

最早解决资源共享问题的，并不是云，而是 Kernel。大型机和 UNIX 时代已经开始解决：如何让一台机器同时服务多个任务。后来 DOS、macOS、Windows、Linux 继续演进这套资源管理逻辑。进程调度、虚拟内存、page cache、fork、swap，本质上都是 Kernel 在把 CPU、内存、IO 从物理硬件抽象成可共享资源。

后来互联网规模扩大，行业进入 Hypervisor 时代。KVM、VMware、Xen、OpenVZ 让服务器第一次从“机器”变成“资源池”。CPU、内存、网络、存储开始可以动态切分、隔离、迁移和回收。虚拟化真正改变的，不只是性能，而是资源管理方式。

再后来，Docker、Kubernetes、CNI、CSI、Ceph 把抽象继续向上推进。Docker 抽象运行环境，CNI 抽象网络，CSI 抽象存储，Ceph 抽象分布式存储池，Kubernetes 抽象整个集群控制面。现代基础设施越来越像一个巨大的资源翻译系统：底层是硬件，上层是 API，中间全部是抽象层。

AI 时代之后，行业又重新开始看见硬件。GPU、NUMA、RDMA、NVLink、PCIe、DPU 开始重新决定系统上限。因为抽象从来不是为了消灭硬件，而是为了更高效地使用硬件。

很多人认知中 Docker 淘汰了 VM、Kubernetes 消灭了 Hypervisor、云已屏蔽硬件。但现实世界：K8s 大量跑在 VM 上、公有云底层仍是 KVM、AI Infra 更依赖 PCIe/NUMA/RDMA。

**虚拟化从未消失，只是沉到了更底层。**

## 演进路径

| 时代 | 核心能力 | 一句话 |
|------|----------|--------|
| Kernel 时代 | 进程调度、虚拟内存、page cache、fork、swap | Kernel 是现代资源抽象体系真正的起点 |
| Hypervisor 时代 | KVM、VMware、Xen、OpenVZ | 服务器第一次从机器变成资源池 |
| 云平台时代 | OpenStack、公有云、资源 API、控制面 | 资源供给从人工分配变成 API 能力 |
| 云原生时代 | Docker、Kubernetes、CNI、CSI、Ceph | 容器没有替代 VM，而是继续向上抽象 |
| AI Infra 时代 | GPU、NUMA、RDMA、NVLink、PCIe、DPU | AI 又把行业重新拉回硬件效率 |

## 书稿收束

过去二十年，整个 IT 行业其实一直在做同一件事：把离散硬件逐渐抽象成统一资源池，再把复杂系统逐渐抽象成可编排能力。

现代基础设施，本质不是技术堆叠，而是一场持续二十多年的资源抽象运动。

## 信息图 Prompt

```
《一图看懂资源抽象史》

风格：蓝白科技风，NVIDIA/RedHat/VMware 官方技术海报风格
中央：Linux Kernel 剖面结构
向外扩散：KVM、QEMU、Ceph、OVS、DPU、GPU Passthrough
左侧演进轴：Kernel → Hypervisor → Cloud Control Plane → Kubernetes → AI Infra
右侧对比：
- 很多人认知：Docker 淘汰 VM
- 现实世界：K8s 跑在 VM 上、公有云底层是 KVM，AI Infra 重新受 GPU/NUMA/RDMA 约束
底部金句：
"现代基础设施，本质不是技术堆叠，而是一场持续二十多年的资源抽象运动。"
```

## 延伸阅读

- [计算虚拟化演进](./compute-virtualization.md)
- [存储虚拟化演进](../virtualization/storage-virtualization.md)
- [网络虚拟化演进](../virtualization/network-virtualization.md)
- [虚拟化从未消失：深度长文](../essays/virtualization-never-died.md)
