# 一图看懂 资源抽象史

> **演进主线**：Linux 资源抽象 → VPS/Hypervisor → KVM 统一 → 云原生 → AI Infra

## 核心观点

**现代基础设施的本质是资源抽象能力的演进。**

Linux Kernel 本身就是最早的资源抽象系统：进程调度、虚拟内存、page cache、swap、cgroups、namespaces。后来 Hypervisor 把服务器变成资源池，KVM 赢的不是性能而是生态收敛，Docker/K8s 继续向上抽象，AI 时代反而重新看见硬件。

很多人认知中 Docker 淘汰了 VM、Kubernetes 消灭了 Hypervisor、云已屏蔽硬件。但现实世界：K8s 大量跑在 VM 上、公有云底层仍是 KVM、AI Infra 更依赖 PCIe/NUMA/RDMA。

**虚拟化从未消失，只是沉到了更底层。**

## 演进路径

| 时代 | 核心能力 | 一句话 |
|------|----------|--------|
| Linux 资源抽象 | 分时、虚拟内存、进程调度 | "Linux 本身就是最早的资源抽象系统" |
| Hypervisor 时代 | OpenVZ、Xen、VMware | "服务器第一次变成资源池" |
| KVM 统一时代 | KVM、QEMU、libvirt、OpenStack | "KVM 赢的不是性能，而是生态收敛" |
| 云原生时代 | Docker、K8s、CSI、CNI、Ceph | "容器没有替代 VM，而是继续向上抽象" |
| AI Infra 时代 | GPU Passthrough、RDMA、DPU | "AI 又把行业重新拉回硬件现实" |

## 信息图 Prompt

```
《一图看懂资源抽象史》

风格：蓝白科技风，NVIDIA/RedHat/VMware 官方技术海报风格
中央：Linux Kernel 剖面结构
向外扩散：KVM、QEMU、Ceph、OVS、DPU、GPU Passthrough
左侧演进轴：Linux → VPS → KVM → 云原生 → AI Infra
右侧对比：
- 很多人认知：Docker 淘汰 VM
- 现实世界：K8s 跑在 VM 上、公有云底层是 KVM
底部金句：
"现代基础设施，本质不是技术堆叠，而是资源抽象能力的不断演进。"
```

## 延伸阅读

- [计算虚拟化演进](./compute-virtualization.md)
- [存储虚拟化演进](../virtualization/storage-virtualization.md)
- [网络虚拟化演进](../virtualization/network-virtualization.md)
- [虚拟化从未消失：深度长文](../essays/virtualization-never-died.md)
