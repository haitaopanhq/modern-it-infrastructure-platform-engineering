# 从 C10k 到 AI Fabric：高并发战争

> **进程 → 线程 → epoll → 协程 → 用户态网络 → DPU/SmartNIC → AI Fabric**

## 为什么 C10k 重要

1999 年提出的问题："一台服务器如何同时处理 10,000 个连接？"

今天听起来很普通，但在 20 多年前 Apache Prefork 时代，每个连接一个进程。一万连接 = 一万进程 = 系统崩溃。C10k 是互联网第一次撞上"连接数墙"。

## 这场战争背后是完整的技术演进链

| 时代 | 解决方案 | 代表技术 |
|------|----------|----------|
| 进程时代 | 每连接一个进程 | Apache Prefork、CGI |
| 线程时代 | 轻量级并发 | 线程池、Tomcat |
| epoll/kqueue | 事件驱动 | Nginx、Redis、Node.js |
| 协程时代 | 用户态调度 | Go goroutine、Lua coroutine |
| 用户态网络 | 绕过内核 | DPDK、XDP、eBPF |
| DPU/SmartNIC | 硬件卸载 | NVIDIA BlueField、Intel IPU |
| AI Fabric | HPC 级互联 | RDMA、InfiniBand、NVLink、NCCL |

## 从 C10k 到 AI Infra

过去高并发拼的是"连接数"，AI Infra 拼的是"数据流吞吐"。一台 GPU 服务器需要几百 Gbps 的通信带宽，几微秒级的延迟。

C10k 的问题在今天看来已经是基础设施层的默认能力，但它开创的事件驱动、零拷贝、用户态网络思想，继续影响着 AI 时代的网络架构。

## 延伸阅读

- [一图读懂 现代网络与协议](../network/network-protocols.md)
- [Kafka 诞生与内核缓存](./kafka-evolution.md)
