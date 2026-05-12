# 05-05: 一图看懂 RDMA/NVLink/NCCL

## 核心观点

AI 集群里的网络不是普通基础设施配角，而是训练性能的一部分。大模型训练需要频繁做 AllReduce、AllGather、ReduceScatter 等集合通信，GPU 算得越快，跨卡、跨机同步越容易成为瓶颈。RDMA、NVLink 和 NCCL 的价值，就是尽量减少 CPU、内核和多次拷贝带来的等待，让 GPU 之间更接近“直接对话”。

但 RDMA 不是单独答案。真正的 AI Fabric 还包括拓扑设计、无损以太网、拥塞控制、GPU 亲和、交换机缓冲、NCCL 参数、作业调度和故障定位。只买高速网卡，不会自动得到高效训练集群。

## 图表结构

```text
单机多 GPU
  GPU <-> NVLink / NVSwitch <-> GPU
  目标: 高带宽、低延迟、绕开 PCIe 瓶颈

跨机 GPU
  GPU -> NIC(RDMA/RoCE/IB) -> Switch Fabric -> NIC -> GPU
  目标: 零拷贝、内核旁路、低 CPU 占用

通信库
  NCCL
    - AllReduce
    - AllGather
    - Broadcast
    - ReduceScatter
  目标: 感知拓扑，选择最优通信路径
```

图表分成三层：NVLink 解决单机内 GPU 互联，RDMA/RoCE/InfiniBand 解决跨机低延迟传输，NCCL 则在软件层把训练框架的集合通信映射到实际拓扑。

## 演进脉络

传统数据中心网络以 CPU 和业务服务为中心。应用请求通过 TCP/IP、内核协议栈和多次内存拷贝完成传输，适合 Web、数据库和微服务流量，但不适合大规模 GPU 同步。

GPU 训练集群出现后，单机内先遇到 PCIe 带宽限制。NVLink 和 NVSwitch 让 GPU 之间可以更高带宽通信，提升单机多卡训练效率。

规模继续扩大后，跨机通信成为关键。InfiniBand 长期服务高性能计算，RoCEv2 把 RDMA 能力带到以太网，但要求网络具备低丢包、低抖动和拥塞控制能力。

大模型时代，训练作业对网络拓扑极其敏感。NCCL 需要根据 GPU、NUMA、PCIe、NIC、交换机层级选择 Ring、Tree 或混合算法；调度系统也要理解节点位置和网络健康，否则算力会被通信拖慢。

## 关键技术栈

| 技术 | 位置 | 作用 |
|------|------|------|
| NVLink / NVSwitch | 单机 GPU 互联 | 提供高带宽、低延迟的 GPU-to-GPU 通信 |
| RDMA | 主机间传输机制 | 内核旁路、零拷贝、降低 CPU 参与 |
| InfiniBand | 专用高性能网络 | 低延迟、成熟 HPC 生态 |
| RoCEv2 | Ethernet 上的 RDMA | 利用以太网生态构建 AI Fabric |
| PFC / ECN / DCQCN | 拥塞与无损控制 | 降低丢包和队列拥塞 |
| GPUDirect RDMA | GPU 与网卡直连路径 | 减少 CPU 内存中转 |
| NCCL | 集合通信库 | 为训练框架选择通信算法和路径 |

这些技术必须协同。RoCE 没有正确 PFC/ECN 可能出现丢包和尾延迟；NCCL 拓扑识别错误会让流量走低效路径；节点 NUMA 和 NIC 绑定错误会让 GPU 等待网络。

AI 网络还要求运维指标更贴近训练任务。传统网络只看链路 up/down、端口流量和丢包率往往不够，还需要观察 NCCL 通信耗时、GPU 利用率空洞、队列拥塞、PFC pause、ECN mark、重传和慢节点分布。训练作业的性能问题，经常是计算、网络和调度共同造成的。

## 误区与现实

误区一是认为带宽越大训练越快。现实是延迟、拓扑、拥塞、批大小、并行策略和通信算法都会影响效率。高带宽但拓扑错误，利用率仍然可能很低。

误区二是认为 RDMA 等于零运维。现实是 RoCE 对交换机配置、队列、PFC、ECN、网卡固件和驱动版本敏感，故障排查比普通 TCP 更难。

误区三是只看单节点 GPU 性能。现实的大模型训练瓶颈常常出现在跨节点 AllReduce，单机跑分不能代表集群训练吞吐。

## 最佳实践

从拓扑开始设计。明确每台服务器 GPU、CPU、NUMA、PCIe、NIC 的连接关系，再设计交换机层级和 oversubscription。AI 集群不能只按普通机架网络规划。

建立网络基准。每次上线节点或升级驱动后，运行 ib_write_bw、perftest、nccl-tests、GPU Direct 验证和端到端训练样例，记录基线。

把故障定位前置到作业生命周期。任务启动前检查链路、驱动、NCCL 环境变量和节点健康；运行中持续采集通信指标；失败后保留拓扑、日志和性能数据，避免每次都从“是不是模型代码问题”重新猜。

把拥塞控制标准化。RoCE 网络必须把 PFC、ECN、DCQCN、MTU、队列和交换机缓冲配置纳入版本管理，避免不同机架配置漂移。

让调度理解网络。训练任务应尽量调度到拓扑相近、网络健康的节点组；故障节点、慢链路和异常 NIC 要能被快速隔离。

最后把网络能力写进容量承诺。对训练平台来说，交付的不是“若干 GPU”，而是带宽、延迟、拓扑和稳定性共同构成的有效算力。

## 与长文互链

本篇是第 05 子系列 AI 网络收束文章，长文入口见[网络与协议长文目录](../longform/README.md)。阅读前可先看[05-03 API Gateway 演进](../03-api-gateway/03-api-gateway-evolution.md)和[05-04 Service Mesh 兴衰](../04-service-mesh/04-service-mesh-rise-fall.md)，对比传统应用网络、微服务网络和 AI Fabric 的关注点差异。

## 关键词

RDMA, RoCEv2, InfiniBand, NVLink, NVSwitch, NCCL, GPUDirect RDMA, PFC, ECN, AI Fabric, AllReduce
