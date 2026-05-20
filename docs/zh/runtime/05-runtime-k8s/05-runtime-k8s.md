# 04-05: 一图看懂 Runtime 与 Kubernetes 的关系

## 核心观点

Kubernetes 自己并不直接运行容器，它通过 kubelet 调用 CRI，把创建 Pod 沙箱、拉取镜像、启动容器、收集状态等动作交给容器运行时。containerd、CRI-O、Kata、gVisor 等 runtime 承担的是“把 Kubernetes 的 Pod 意图变成节点上真实进程或虚拟机”的工作。

理解这层关系很重要，因为 Kubernetes 统一的是编排接口，不是所有运行细节。镜像格式、网络命名空间、存储挂载、日志路径、cgroup、GPU 设备、安全沙箱和 RuntimeClass，都会影响一个 Pod 在节点上的真实行为。

## 图表结构

```text
API Server
   |
   v
Scheduler 选择节点
   |
   v
kubelet
   |
   v
CRI gRPC
  - RunPodSandbox
  - PullImage
  - CreateContainer
  - StartContainer
  - StopContainer
   |
   v
Container Runtime
  - containerd / CRI-O
  - gVisor runsc / Kata
   |
   v
OCI Runtime / VM / Host Kernel
  - runc / crun / MicroVM
```

图表中的分界线说明：Kubernetes 负责声明和调度，kubelet 负责节点执行，CRI 是标准接口，runtime 负责真正启动 workload。Docker 不再作为 Kubernetes 默认运行时入口，并不代表 Docker 镜像消失；OCI 镜像仍然是事实标准。

## 演进脉络

早期 Kubernetes 通过 dockershim 连接 Docker Engine。那时 Docker 同时承担开发工具、镜像构建、镜像仓库交互和容器运行入口，使用体验统一，但组件边界不清晰。

随着 Kubernetes 成熟，社区把运行时接口抽象成 CRI。containerd 和 CRI-O 逐渐成为更轻、更清晰的节点 runtime，dockershim 被移除，Kubernetes 不再依赖 Docker Engine。

之后 runtime 开始分层。containerd 管理镜像、快照、任务和插件，底层调用 runc 或 crun；安全场景可以接入 gVisor、Kata；特殊场景可以接入 WASM runtime、GPU runtime 或虚拟机 runtime。

现在的趋势是多 runtime 并存。普通服务追求密度和性能，不可信任务追求隔离，AI 任务需要 GPU 和高速网络，边缘任务需要轻量和可更新。Kubernetes 通过 RuntimeClass、节点标签和调度策略把这些差异暴露为平台能力。

## 关键技术栈

| 组件 | 作用 | 说明 |
|------|------|------|
| kubelet | 节点代理 | 接收 PodSpec，调用 CRI，汇报状态 |
| CRI | Kubernetes 与 runtime 的接口 | 统一镜像和容器生命周期操作 |
| containerd | 通用容器运行时 | Kubernetes 默认常见选择，插件生态成熟 |
| CRI-O | 面向 Kubernetes 的 runtime | 设计目标更聚焦 CRI 和 OCI |
| runc / crun | OCI Runtime | 真正创建 Linux 容器进程 |
| RuntimeClass | runtime 选择策略 | 让不同 Pod 使用不同 runtime |
| CNI / CSI | 网络与存储接口 | runtime 执行时必须与网络、存储插件配合 |

这些组件共同决定 Pod 是否能稳定启动。很多“应用启动失败”表面上是镜像或 YAML 问题，实际可能来自 runtime socket、cgroup driver、镜像快照、CNI 初始化或节点内核能力。

对平台团队来说，runtime 也是节点产品的一部分。一个节点池到底支持普通容器、安全容器、GPU、WASM 还是高性能网络，不应只靠节点标签描述，还要有配套镜像预热、驱动版本、日志路径、监控采集和升级策略。否则 Kubernetes 控制面看起来统一，节点执行层却会形成多个不可见孤岛。

## 误区与现实

误区一是认为 Docker 被 Kubernetes 移除后镜像格式变了。现实是 OCI 镜像仍然通用，开发者可以继续用 Docker、BuildKit、Podman 构建镜像，节点侧只是少了一层 Docker Engine。

误区二是认为 runtime 对业务无感。现实是日志路径、文件系统、特权能力、GPU 设备、启动速度、沙箱隔离和系统调用兼容都会影响业务。

误区三是认为一个集群只能有一个 runtime。现实是 Kubernetes 可以通过 RuntimeClass 支持多 runtime，但需要节点池、调度、监控和安全策略配套。

## 最佳实践

保持节点运行时简单。生产默认优先选择 containerd 或 CRI-O，减少不必要组件，保证 cgroup、日志、镜像仓库和 CNI 配置一致。

把 runtime 差异平台化。不要让业务直接猜测节点能力，应提供标准等级：普通容器、增强隔离、强隔离、GPU 任务、WASM 任务等。

为节点池建立准入规则。需要 GPU、特权能力、hostNetwork、特殊挂载或强隔离的 workload，应通过 admission policy 和 RuntimeClass 绑定到明确节点池，避免调度结果依赖约定俗成的标签。

为 RuntimeClass 建立测试。每个 runtime 都要覆盖镜像拉取、探针、日志、网络、存储挂载、资源限制、安全策略和升级回滚。

升级前验证节点事实。Kubernetes 版本、containerd 版本、Linux 内核、cgroup v2、CNI 插件和 GPU driver 必须一起看，不能只看控制面版本。

运行中也要持续校验漂移。节点重启、系统包升级、镜像垃圾回收、runtime 配置修改和驱动替换，都可能改变 Pod 的真实执行环境。平台应定期比对节点基线，并把异常节点自动摘除或降级使用。

这样做的目的，是让控制面声明、节点能力和业务预期始终对齐，避免问题暴露时才发现运行时早已偏离基线。

## 与长文互链

本篇是第 04 子系列 runtime 与 Kubernetes 的收束文章，长文入口见[容器运行时长文目录](../longform/README.md)。前置阅读包括[04-03 gVisor/Kata](../03-gvisor-kata/03-gvisor-kata.md)和[04-04 沙箱隔离演进](../04-sandbox/04-sandbox-evolution.md)，它们解释为什么 Kubernetes 需要支持多种 runtime。

## 关键词

Kubernetes, CRI, kubelet, containerd, CRI-O, runc, RuntimeClass, OCI Image, CNI, CSI, cgroup
