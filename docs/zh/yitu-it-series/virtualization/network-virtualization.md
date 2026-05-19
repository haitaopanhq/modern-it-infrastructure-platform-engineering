# 一图看懂 网络虚拟化演进

> **演进主线**：VLAN → Overlay Network → SDN → CNI → AI Fabric

## 核心观点

**网络开始软件定义，最终走向 HPC 级数据面。**

传统网络是物理设备控制一切。Overlay 网络让网络第一次软件定义，SDN 分离控制面与转发面，CNI 统一容器网络，AI Fabric 让网络重回 HPC 级竞争。

## 演进路径

| 时代 | 特点 | 代表技术 |
|------|------|----------|
| 传统网络 | 物理隔离 | VLAN、Router、STP |
| Overlay | 软件定义网络 | VXLAN、GRE、Open vSwitch |
| SDN | 控制与转发分离 | OpenFlow、NSX |
| K8s 网络 | 容器通信标准 | CNI、Calico、Cilium、eBPF |
| AI Fabric | HPC 级互联 | RDMA、InfiniBand、NVLink、NCCL |

## 冲突认知

传统互联网拼南北流量（用户请求），AI Infra 拼东西流量（GPU 同步通信）。网络正在从"连接服务"变成"控制系统"。

## 延伸阅读

- [一图读懂 现代网络与协议](../network/network-protocols.md)
- 书籍第 2 章：[网络与协议](../../02-networking-protocols.md)
