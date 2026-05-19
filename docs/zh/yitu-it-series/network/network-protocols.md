# 一图读懂 现代网络与协议

> **演进主线**：TCP/IP → DNS → BGP → HTTP → gRPC → Service Mesh → API Gateway → AI Gateway → Agent 协议

## 核心观点

**网络已经从"连接时代"进入"数据面时代"。**

很多人以为：网络 = 路由器 + 交换机；云原生网络 = Kubernetes + CNI；AI 集群 = 多买几张 GPU。

但真正吃资源的已经不是南北流量（用户访问网站），而是东西向流量：Pod 与 Pod、Service 与 Service、GPU 与 GPU、Cluster 与 Cluster。尤其在 AI 集群里，NCCL、AllReduce、KV Cache、Tensor Parallel 本质都在疯狂消耗网络。很多时候 GPU 没满载，不是算不动，而是**在等网络**。

## 演进路径

| 时代 | 核心 | 代表技术 |
|------|------|----------|
| 传统网络 | 连接设备 | VLAN、Router、Switch、STP |
| Overlay 网络 | 软件定义 | VXLAN、GRE、Open vSwitch |
| SDN 时代 | 控制与转发分离 | OpenFlow、NSX、SDN Controller |
| K8s 网络 | 容器通信 | CNI、Calico、Cilium、eBPF |
| AI Fabric | HPC 级通信 | RDMA、RoCEv2、InfiniBand、NVLink、NCCL |

## 冲突认知

- 很多人以为 Overlay 网络是"免费"的
- 现实：VXLAN/Geneve 需要用 MTU 损耗、PPS 压力、CPU 消耗和延迟增加来换取灵活性

- 很多人以为 Linux 网络只是"网卡驱动 + 协议栈"
- 现实：eBPF、XDP、tc、RSS/RPS 才是真正的数据面核心

## 信息图 Prompt

```
《一图读懂现代网络与协议》

风格：Cisco / NVIDIA Networking 风格，高速网络 Fabric，蓝色科技工业感
时间轴：传统网络 → Overlay → SDN → K8s 网络 → AI Fabric
右侧对比：
- 传统互联网：南北流量、用户请求
- AI Infra：东西向流量、GPU 同步通信
底部金句：
"AI 时代，网络再一次变成算力不可或缺的部分。"
```

## 延伸阅读

- 书籍第 2 章：[网络与协议](../../02-networking-protocols.md)
- [从 C10k 到 AI Fabric：高并发战争](../deep-dive/c10k-to-ai-fabric.md)
