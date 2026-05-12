# 04-03: 一图看懂 gVisor/Kata

## 核心观点

gVisor 和 Kata Containers 都属于“安全容器”路线，但它们解决问题的方式不同。普通容器共享宿主机内核，启动快、性能好，却把隔离边界放在 namespace、cgroups、capabilities、seccomp 和 LSM 上；gVisor 在用户态实现一个内核兼容层，拦截大量系统调用；Kata 则把每个 Pod 放进轻量虚拟机，用独立内核获得更强隔离。

因此安全容器不是“比 Docker 更先进”的替代品，而是在多租户、不可信代码、函数计算、边缘执行和敏感工作负载中，用性能与兼容性换取更明确隔离边界的工程选择。

## 图表结构

```text
普通容器
  App -> libc -> 宿主机 Linux Kernel -> 硬件
  特点: 快、轻、共享内核、隔离较弱

gVisor
  App -> Sentry(用户态内核) -> Gofer(文件代理) -> 宿主机 Kernel
  特点: 系统调用被拦截，减少直接攻击面

Kata Containers
  App -> Guest Kernel -> 轻量 VM -> Hypervisor -> 硬件
  特点: 每个 Pod 独立内核，隔离强，开销更高
```

这张图的核心是隔离边界位置。普通容器的边界在宿主机内核策略上，gVisor 把边界前移到用户态内核模拟层，Kata 把边界下沉到虚拟化层。三者不是线性替代，而是面向不同风险等级的选择。

## 演进脉络

容器普及初期，行业关注点是交付速度和资源密度。Docker、runc、containerd 让应用打包和运行标准化，默认假设是同一集群内的工作负载大体可信。

当容器进入公有云多租户、Serverless、CI 执行器和第三方插件场景，攻击面发生变化。用户上传的代码、镜像和依赖不再可信，单纯依靠共享内核隔离会让平台承担更高风险。

gVisor 代表用户态内核路线。它用 Sentry 模拟 Linux 系统调用，限制应用直接触达宿主机内核的机会，适合需要较强隔离但仍希望保持容器体验的场景。

Kata 代表微虚拟机路线。它继承虚拟机隔离模型，通过 Firecracker、QEMU、Cloud Hypervisor 等 VMM 运行轻量 VM，适合多租户边界更强、合规要求更高的场景。

## 关键技术栈

| 技术 | 位置 | 价值 | 代价 |
|------|------|------|------|
| runc | OCI Runtime | 性能高、兼容好、生态成熟 | 共享宿主机内核 |
| gVisor runsc | 用户态内核 runtime | 缩小内核攻击面 | 系统调用兼容和性能有损耗 |
| Kata Containers | VM-based runtime | 独立内核、强隔离 | 启动和资源开销更高 |
| Firecracker | MicroVM VMM | 快速启动、适合 Serverless | 功能面比完整 VM 更窄 |
| RuntimeClass | Kubernetes 调度接口 | 按工作负载选择 runtime | 需要节点池和策略治理 |

在 Kubernetes 中，安全容器通常通过 RuntimeClass 暴露给业务。平台团队可以把普通服务、CI 任务、不可信插件、外部客户 workload 分配到不同 runtime，而不是让所有工作负载使用同一隔离等级。

## 误区与现实

误区一是认为安全容器等于绝对安全。现实是 gVisor 和 Kata 只是改变攻击面，仍然需要镜像扫描、最小权限、网络策略、密钥隔离、补丁管理和运行时监控。

误区二是认为安全容器可以无感替换普通容器。现实中，某些系统调用、文件系统语义、网络性能、GPU 设备、eBPF、FUSE 和特权容器能力可能受影响，必须按工作负载测试。

误区三是认为隔离越强越好。若全部 workload 都运行在微虚拟机里，资源密度、启动延迟和运维复杂度会明显增加。安全容器应匹配风险，而不是变成默认重锤。

## 最佳实践

先做风险分级。内部可信微服务使用 runc 即可；外部提交代码、CI 执行器、插件市场、Serverless 函数和多租户任务优先评估 gVisor 或 Kata。

再做节点池隔离。不同 runtime 最好对应独立节点池、标签、污点和调度策略，避免普通 workload 与高风险 workload 混跑。

同时把性能预算讲清楚。安全容器上线前，应明确启动延迟、吞吐下降、内存额外占用和镜像预热成本能否被业务接受。对延迟敏感的在线服务、需要高吞吐存储的任务、依赖特殊内核能力的组件，不能只按安全目标决策。

建立兼容性测试清单。系统调用、文件 IO、网络吞吐、DNS、日志、探针、挂载、GPU、启动时间都应纳入测试，尤其是高性能和底层依赖较多的应用。

最后将 runtime 选择产品化。业务不应直接理解复杂 runtime 细节，而应选择“标准隔离”“增强隔离”“强隔离”等平台等级，由平台映射到 gVisor、Kata 或普通 runc。

## 与长文互链

本篇是第 04 子系列安全容器入口，长文稿件集中放在[容器运行时长文目录](../longform/README.md)。建议继续阅读[04-04 沙箱隔离演进](../04-sandbox/04-sandbox-evolution.md)理解隔离技术谱系，再读[04-05 Runtime 与 Kubernetes 的关系](../05-runtime-k8s/05-runtime-k8s.md)理解 RuntimeClass 如何把这些能力接入集群。

## 关键词

gVisor, Kata Containers, 安全容器, RuntimeClass, runsc, Firecracker, MicroVM, 多租户隔离, OCI Runtime, Kubernetes
