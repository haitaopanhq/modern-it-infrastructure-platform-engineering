# 第 1 章：现代 IT 系统全景

![现代IT系统全景图](../zh/diagrams/01-it-systems.png)

## 本章概述

本章介绍现代 IT 基础架构的演进历程和整体架构，帮助读者建立对现代 IT 系统的全局认知。

## 1.1 什么是现代 IT 基础架构

现代 IT 基础架构是指从传统物理服务器、虚拟机到云原生系统的整体技术栈。它包括：

- **计算资源**：物理服务器、虚拟机、容器、函数计算
- **存储资源**：块存储、文件存储、对象存储、分布式存储
- **网络资源**：传统网络、软件定义网络（SDN）、CNI、Service Mesh
- **数据服务**：数据库、缓存、消息队列、数据湖、向量数据库
- **可观测性**：监控、日志、追踪、事件
- **安全体系**：IAM、RBAC、网络策略、零信任

## 1.2 从单机到云原生的演进

### 时代划分

| 时代 | 特征 | 代表技术 |
|------|------|----------|
| 物理机时代 | 独占硬件，手工管理 | 物理服务器、RAID、SAN |
| 虚拟化时代 | 资源池化，虚拟化管理 | VMware、KVM、Xen |
| 容器时代 | 轻量级隔离，快速部署 | Docker、Kubernetes |
| 云原生时代 | 声明式、自动化、弹性 | K8s、Service Mesh、GitOps |

### 关键演进节点

1. **虚拟化技术** - 从硬件虚拟化到操作系统虚拟化
2. **容器编排** - 从 Docker Swarm 到 Kubernetes 一统天下
3. **服务网格** - 从微服务到 Service Mesh
4. **GitOps** - 从 CI/CD 到声明式运维

## 1.3 系统分层架构

```
┌─────────────────────────────────────────────┐
│              应用层 (Application)            │
│  业务应用 │ Web 服务 │ API │ AI Agents       │
├─────────────────────────────────────────────┤
│              平台层 (Platform)               │
│  K8s │ Service Mesh │ API Gateway │ IDP     │
├─────────────────────────────────────────────┤
│              基础设施层 (Infrastructure)     │
│  计算 │ 存储 │ 网络 │ 数据库 │ 缓存          │
├─────────────────────────────────────────────┤
│              硬件层 (Hardware)               │
│  服务器 │ GPU │ 存储设备 │ 网络设备         │
└─────────────────────────────────────────────┘
```

## 1.4 核心能力体系

### 基础设施能力

- 计算资源管理
- 存储资源管理
- 网络资源管理
- 基础安全能力

### 平台能力

- 应用交付
- 运行时管理
- 可观测性
- 自动化运维

### 应用能力

- 业务逻辑
- 数据处理
- 用户交互
- 外部集成

## 1.5 从"组件堆叠"到"能力体系"

传统 IT 建设关注的是"买什么组件"，现代 IT 关注的是"需要什么能力"。

### 对比

| 维度 | 传统思维 | 现代思维 |
|------|----------|----------|
| 关注点 | 组件功能 | 业务能力 |
| 交付方式 | 手工部署 | 自动化交付 |
| 运维模式 | 被动响应 | 主动运营 |
| 扩展方式 | 垂直扩展 | 水平扩展 |
| 治理方式 | 分散管理 | 统一平台 |

## 1.6 基础设施演进： 从 Cloud Native 到 AI Native

### 演进路径

```
硬件层 → 虚拟化层 → 云控制平面 → 运行时 → 网络 → 编排层 → AI 基础设施
   │           │             │          │       │        │         │
   ▼           ▼             ▼          ▼       ▼        ▼         ▼
 GPU/NVMe   Ceph/CSI      AWS/K8s    Docker   CNI     K8s     vLLM/Ray
 RDMA       Open vSwitch  OpenStack  OCI      eBPF   Kubelet  Triton
```

### 层次解析

| 层次 | 核心组件 | 关注点 |
|------|----------|--------|
| 硬件层 | GPU、NVMe、RDMA、Linux Kernel、eBPF、cgroups | 资源边界与性能上限 |
| 虚拟化层 | Ceph、Open vSwitch、SR-IOV、DPDK、CSI | 计算/存储/网络统一资源池化 |
| 云控制平面 | AWS、OpenStack、Harvester | 资源统一管理、调度、编排 |
| 容器编排 | Kubernetes | 分布式容器操作系统 |
| AI 基础设施 | vLLM、Ray、TensorRT-LLM、SGLang、Triton | GPU调度、分布式推理、模型路由 |

### Kubernetes 的定位

Kubernetes 更像是时代的"中间层"，而非最终答案：

- **成功原因**：形成完整生态和事实标准，Mesos、Docker Swarm 逐渐退场
- **应用误区**：Kubernetes Everything——数据库跑 K8s、AI 跑 K8s、边缘跑 K8s、存储也跑 K8s
- **最终状态**：像 Linux 一样逐渐"下沉"，成为基础设施底座

### AI 时代的基础设施重构

| 传统 Web 基础设施 | AI 基础设施 |
|-------------------|-------------|
| HTTP 请求 | Token 延迟 |
| 副本数 | GPU 调度 |
| 弹性伸缩 | KV Cache |
| 服务治理 | 显存拓扑 |
| API Gateway | 多模型网关 |

### 未来趋势

**向上生长的新层**：
- AI Gateway - AI 请求路由与负载均衡
- GPU Scheduler - 异构资源调度
- Inference Fabric - 推理服务网格
- Semantic Cache - 语义缓存
- Agent Runtime - Agent 执行时

> Cloud Native 没有结束，它正在进入下一阶段：**AI Native**

## 学习目标

- [ ] 能画出现代 IT 系统的整体结构
- [ ] 能区分基础设施能力、平台能力、应用能力
- [ ] 理解从物理机到云原生的演进历程
- [ ] 理解"能力体系" vs "组件堆叠"的区别

## 延伸阅读

- [Cloud Native Architecture](https://github.com/cncf/tag-cloud-architecture)
- [Kubernetes Documentation](https://kubernetes.io/docs/concepts/overview/)
- [Platform Engineering Guide](https://platformengineering.org/)
