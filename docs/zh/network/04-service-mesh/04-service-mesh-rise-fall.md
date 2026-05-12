# 05-04: 一图看懂 Service Mesh 兴衰

## 核心观点

Service Mesh 的兴衰说明了一个工程现实：把流量治理从业务代码中抽出来很有价值，但把每个 Pod 都接入 Sidecar、再引入复杂控制面，并不总是值得。Mesh 解决的是服务间通信的可观测性、安全和治理问题，代价是运行复杂度、资源开销、学习成本和故障面扩大。

所以 Service Mesh 不是失败技术，而是从“默认上 Mesh”的热潮回到“按场景使用”的理性。它适合服务规模大、安全边界强、发布治理复杂、跨语言团队多的组织；不适合用来掩盖服务设计混乱或平台能力不足。

## 图表结构

```text
控制面
  - 服务发现 / 配置下发 / 证书管理 / 策略
        |
        v
数据面
  Service A -- Sidecar Proxy -- Sidecar Proxy -- Service B
        |              |                 |
        |              v                 |
        |        mTLS / Retry / Timeout / Metrics
        v
可观测与安全
  - Trace / Metrics / Logs
  - mTLS / AuthZ / Traffic Policy
```

这张图的核心是“控制面下发意图，数据面执行流量策略”。Sidecar 让业务无须内置 SDK 就能获得统一流量能力，但每个请求多经过代理，也带来性能、排障和升级成本。

## 演进脉络

第一阶段是微服务治理痛点出现。服务数量增加后，重试、超时、熔断、限流、服务发现、调用链和证书管理分散在各语言 SDK 中，治理不一致。

第二阶段是 Sidecar Mesh 兴起。Linkerd、Istio、Consul Connect 等把这些能力下沉到代理层，Envoy 成为事实标准数据面。平台团队可以统一下发流量和安全策略。

第三阶段是复杂性反噬。团队发现 Mesh 控制面、Sidecar 注入、证书轮换、协议识别、资源消耗、升级兼容和排障链路都不简单。很多小团队没有足够收益来覆盖成本。

第四阶段是轻量化和重新分层。Ambient Mesh、eBPF 数据面、Gateway API、服务端 SDK 和平台级网络策略开始分担 Mesh 的能力。行业逐渐从“全量 Sidecar”转向“在需要的边界使用合适治理方式”。

## 关键技术栈

| 组件 | 代表技术 | 作用 |
|------|----------|------|
| 数据面代理 | Envoy, Linkerd-proxy | 拦截流量并执行策略 |
| 控制面 | Istiod, Linkerd control plane, Consul | 服务发现、证书、配置下发 |
| 安全 | mTLS, SPIFFE/SPIRE, AuthorizationPolicy | 服务身份、加密和授权 |
| 流量治理 | VirtualService, DestinationRule, Gateway API | 灰度、路由、重试、熔断 |
| 可观测性 | OpenTelemetry, Prometheus, Jaeger, Kiali | 指标、链路、拓扑和排障 |
| 新路线 | Ambient Mesh, eBPF, Cilium | 降低 Sidecar 成本和侵入性 |

Mesh 的技术栈看起来完整，但每一层都需要运营能力。证书过期、Sidecar 配置错误、代理资源不足、控制面不可用，都可能影响业务调用。

更现实的判断方式，是把 Mesh 看成一套平台能力而非单个组件。它需要平台团队维护证书体系、默认策略、升级节奏、排障手册和容量预算，也需要业务团队理解超时、重试和幂等性。没有这些组织配套，Mesh 只会把原本分散在代码里的问题集中到代理和控制面上。

## 误区与现实

误区一是认为 Service Mesh 能自动提升系统稳定性。现实是 Mesh 只提供工具，错误的重试、过短超时或不合理熔断会放大故障。

误区二是认为业务完全无感。现实中，协议、Header、连接池、长连接、gRPC、WebSocket、数据库连接和大包传输都可能受代理影响。

误区三是认为不用 Mesh 就落后。现实是许多团队用 API Gateway、CNI 网络策略、OpenTelemetry SDK、服务框架和平台规范，也能覆盖主要治理需求。

## 最佳实践

先明确收益场景。跨团队微服务、多语言栈、强 mTLS 要求、复杂灰度、统一链路观测，是 Mesh 值得评估的信号。

从边界开始接入。可以先治理入口、核心服务或高风险调用链，而不是全集群注入 Sidecar。渐进式接入更容易发现兼容性问题。

用数据决定扩展范围。接入后应持续看代理 CPU、内存、P99 延迟、重试放大、证书错误和策略命中率。如果这些数据不能证明收益，继续扩大 Mesh 覆盖面就只是扩大故障面。

设置流量策略基线。超时、重试、熔断、连接池、限流必须有默认值和评审机制，避免每个团队自由配置。

保留逃生路径。控制面故障、代理升级失败、证书轮换异常时，要能快速定位并回滚。Mesh 本身也要有 SLO 和演练。

同时控制策略数量。规则越多，越容易互相覆盖，最终让调用路径难以解释。少量清晰基线通常比复杂规则堆叠更可靠。

## 与长文互链

本篇是第 05 子系列服务间流量治理文章，长文入口见[网络与协议长文目录](../longform/README.md)。可先读[05-03 API Gateway 演进](../03-api-gateway/03-api-gateway-evolution.md)区分南北向入口治理，再读[05-05 RDMA/NVLink/NCCL](../05-rdma-nvlink-nccl/05-rdma-nvlink-nccl.md)理解 AI 时代网络关注点如何从微服务调用转向集群通信。

## 关键词

Service Mesh, Istio, Envoy, Linkerd, Sidecar, mTLS, SPIFFE, Ambient Mesh, eBPF, Gateway API
