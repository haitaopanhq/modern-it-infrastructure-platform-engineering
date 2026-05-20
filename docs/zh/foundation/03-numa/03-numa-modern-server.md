# 01-03: 一图看懂 NUMA 与现代服务器

## 核心观点

NUMA 是现代服务器性能问题的底层语法。多路 CPU、海量内存、高速网卡、本地 NVMe、GPU 和 DPU 同时出现后，“服务器”不再是一个均匀资源池，而是由多个局部性很强的计算与内存岛组成。进程访问本地内存很快，跨 Socket 或跨 NUMA Node 访问就会增加延迟、降低带宽，并放大尾延迟。

平台工程如果只把节点看成 CPU 核数和内存容量，就会忽略资源之间的距离。数据库、缓存、消息队列、AI 推理、RDMA 网络和高性能存储都会受到 NUMA 影响。理解 NUMA，不是为了手工调参，而是为了让调度、容量和故障诊断具备物理常识。

## 图表结构

```
NUMA Node 0
  CPU Core 0-31
  Local Memory
  NIC / NVMe / GPU A

NUMA Node 1
  CPU Core 32-63
  Local Memory
  GPU B / DPU

跨 Node 访问
  -> 经过互联总线
  -> 延迟上升，带宽下降，抖动增加
```

图表强调三类关系：CPU 到内存的距离、CPU 到设备的距离、进程与数据所在 Node 的关系。一个 Pod 申请了 16 个 CPU 和 128GB 内存，不代表它们一定来自同一个 NUMA Node；一个 GPU 任务拿到卡，也不代表 CPU 线程和网卡就在同侧。

读图时可以把 NUMA 想成服务器内部的“城市距离”。同城访问快，跨城访问慢；道路没有断，但绕路会增加时间。很多平台指标只显示总量，不显示距离，这正是 NUMA 问题隐蔽的原因。调度器如果只看剩余 CPU 和内存，就可能把计算线程、内存页和设备放到不同的“城市”。

## 演进脉络

单路服务器时代，内存访问近似均匀，应用通常不需要关心物理布局。多路服务器把 CPU 和内存控制器拆成多个局部域，NUMA 成为性能事实。虚拟化时代，Hypervisor 需要把 vCPU 和 Guest Memory 尽量放在同一 NUMA 拓扑内，否则虚拟机内部看不见的问题会变成性能抖动。

容器时代，问题并没有消失，只是被 Kubernetes 节点抽象盖住。AI 和高性能网络再次把 NUMA 推到前台：GPU 挂在哪个 PCIe Root Complex 下，网卡是否靠近训练进程，本地 NVMe 是否跨 Socket，都会影响吞吐与稳定性。

更重要的是，NUMA 问题往往不会表现成明确报错，而是表现为“偶尔慢”“扩容无效”“同配置节点性能不同”。这类问题最容易被误判为应用代码、数据库参数或网络抖动，直到把拓扑拉出来才发现资源距离才是真正原因。

这也是现代服务器容量评估必须包含拓扑视角的原因。

## 关键技术栈

| 技术 | 作用 | 平台工程关注点 |
| --- | --- | --- |
| `numactl` / `numastat` | 查看与绑定 NUMA 策略 | 排障和基线验证 |
| CPU Manager | Kubernetes CPU 亲和 | 独占核与静态策略 |
| Topology Manager | 协调 CPU、内存、设备拓扑 | GPU/NIC/内存同侧放置 |
| HugePages | 减少页表开销 | 数据库、DPDK、AI 推理 |
| IRQ/RPS/XPS | 网络中断与队列亲和 | 避免跨 Node 网络处理 |
| PCIe/NVLink 拓扑 | 设备距离 | GPU、DPU、NVMe 亲和 |

## 误区与现实

- 误区：NUMA 只影响传统数据库。现实：只要任务对内存、网络或设备延迟敏感，NUMA 都可能成为瓶颈。
- 误区：容器天然屏蔽 NUMA。现实：容器共享宿主机内核，调度器不感知拓扑时更容易制造跨 Node 访问。
- 误区：绑核一定提升性能。现实：错误绑核会把进程固定在远离内存或设备的位置，效果反而更差。

## 最佳实践

高性能节点应在交付前输出 NUMA 拓扑报告，包含 CPU、内存、网卡、GPU、NVMe 与 DPU 的对应关系。对于数据库、缓存、网关、推理服务和训练任务，应优先使用独占 CPU、HugePages、设备亲和和拓扑感知调度。

排障时不要只看平均 CPU 利用率。应同时观察 remote memory access、LLC miss、网络队列、IRQ 分布、GPU 利用率和应用尾延迟。平台层要把“同节点”进一步细化成“同 NUMA 域”，否则资源看似充足，实际路径已经绕远。

在 Kubernetes 中，可以把 CPU Manager 的 static 策略、Topology Manager 的 restricted 或 single-numa-node 策略、HugePages 和设备插件组合使用，让关键 Pod 尽量获得一致的拓扑放置。对于虚拟机平台，也要让 vNUMA 与宿主机 NUMA 尽量匹配，避免 Guest 内部调度器基于错误拓扑做决策。

NUMA 优化不应只在极端性能项目中出现。只要一个服务承担核心交易、网关、缓存、数据库、推理或高吞吐数据面，就值得至少做一次拓扑审计。很多“偶发慢请求”并不是代码突然变差，而是线程、内存和设备被放到了错误距离上。

## 与长文互链

- 长文计划：[01-LF-01: 从 Linux 内核到平台工程：基础设施控制权为什么总会回到底层](../longform/01-foundation-control-power.md)
- 相关短文：[01-02: AI 为什么重新回到裸金属](../02-hardware/02-ai-back-to-baremetal.md)
- 相关短文：[01-04: CPU → GPU → DPU 演进](../04-cpu-gpu-dpu/04-cpu-gpu-dpu-evolution.md)

## 关键词

NUMA, Socket, CPU 亲和, Topology Manager, HugePages, PCIe 拓扑, GPU 亲和, RDMA, 低延迟, 平台工程
