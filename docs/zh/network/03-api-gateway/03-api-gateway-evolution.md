# 05-03: 一图看懂 API Gateway 演进

## 核心观点

API Gateway 的演进，本质是入口控制权不断前移。从最早的反向代理和负载均衡，到统一认证、限流、路由、灰度、审计，再到 API 生命周期管理和 AI Gateway，网关已经不只是“把请求转发到后端”的组件，而是业务入口、平台策略和流量治理的交汇点。

现代系统中，网关负责回答三个问题：谁可以访问，流量应该去哪里，访问过程如何被治理。对于 AI 应用，它还要回答模型怎么选、Token 怎么控、成本怎么分摊、上下文怎么审计。

## 图表结构

```text
客户端 / 合作伙伴 / Agent / AI 应用
        |
        v
入口层
  - DNS / CDN / WAF / Load Balancer
        |
        v
API Gateway
  - 路由 / 认证 / 授权 / 限流
  - 灰度 / 熔断 / 重试 / 超时
  - 日志 / 审计 / 指标 / Trace
  - API Key / OAuth2 / OIDC / mTLS
        |
        v
服务层
  - Microservices / Serverless / Model API / Legacy System
```

这张图强调网关的边界：它位于外部流量和内部服务之间，既不是单纯的负载均衡，也不是业务代码的一部分。网关越靠近入口，越适合做横切治理；越深入业务，越容易变成复杂耦合点。

## 演进脉络

第一代是反向代理时代。Nginx、Apache、HAProxy 主要处理静态资源、TLS 终止、七层转发和负载均衡，关注点是连接效率和稳定性。

第二代是 API 网关时代。移动应用、开放平台和微服务兴起后，Kong、Tyk、Traefik、Spring Cloud Gateway 等开始承担认证、限流、路由、插件和开发者门户能力。

第三代是云原生流量治理。Envoy、Istio Ingress、Gateway API 把网关纳入 Kubernetes 和服务网格体系，灰度发布、流量镜像、熔断、超时、重试和可观测性成为默认能力。

第四代是 API 管理平台。Apigee、AWS API Gateway、Azure API Management 等把 API 生命周期、版本、订阅、计费、文档和开发者关系纳入治理。

AI 时代出现 AI Gateway。模型提供商变多，调用成本高，安全风险更复杂，网关开始管理模型路由、Prompt 审计、Token 预算、敏感信息过滤、缓存和多模型降级。

## 关键技术栈

| 阶段 | 代表技术 | 核心能力 |
|------|----------|----------|
| 反向代理 | Nginx, HAProxy, Apache | TLS、转发、负载均衡、静态资源 |
| 云原生网关 | Envoy, Traefik, Kong, Gateway API | 路由、限流、插件、K8s 集成 |
| API 管理 | Apigee, AWS API Gateway, Azure APIM | 生命周期、订阅、计费、开发者门户 |
| 服务流量 | Istio Ingress, Envoy Gateway | 灰度、熔断、重试、mTLS、Trace |
| AI Gateway | LiteLLM, Portkey, OpenAI-compatible gateway | 模型路由、Token 预算、审计、降级 |

网关技术选型应从流量形态出发。公开 API 重视安全和生命周期，内部微服务重视可观测和发布治理，AI 入口重视成本、审计和模型切换。

还有一个常被忽略的维度是组织边界。面向外部开发者的网关需要文档、订阅、配额和版本承诺；面向内部平台的网关需要稳定配置模型和自助接入；面向 AI 的网关则需要把模型调用变成可审计、可限额、可回放的企业资源。不同边界不应强行塞进同一个配置习惯。

## 误区与现实

误区一是把 API Gateway 当成万能中台。现实是网关适合处理横切能力，不适合堆业务规则。把大量业务编排写进网关，会让变更、测试和排障都变困难。

误区二是认为有了 Service Mesh 就不需要 Gateway。现实是网关治理南北向流量，Mesh 更擅长东西向服务通信，两者边界不同。

误区三是忽视出口流量。很多系统只治理入口，却让服务直接访问第三方 API、模型接口和外部 SaaS。AI 时代的出口网关同样重要，因为成本和数据泄露常发生在出口侧。

## 最佳实践

明确网关职责。入口网关处理认证、限流、路由、审计和协议转换；业务聚合放在 BFF 或服务层；复杂编排放到工作流或应用代码。

把策略配置化。限流、超时、重试、熔断、灰度、Header 透传、CORS、鉴权规则应通过声明式配置管理，并进入代码评审和发布流水线。

统一观测字段。请求 ID、用户、租户、API 版本、上游服务、状态码、延迟、限流结果和成本字段要统一，否则网关只能转发，不能治理。

AI Gateway 要单独建账。模型、Token、调用方、缓存命中、失败原因、敏感内容处理和降级路径都应可追踪，不能把 LLM 调用当成普通 HTTP 转发。

最后保留分层边界。网关可以拒绝、路由和记录请求，但业务一致性、复杂事务和领域判断仍应留在服务内部。

## 与长文互链

本篇是第 05 子系列网络入口治理文章，长文稿件入口见[网络与协议长文目录](../longform/README.md)。后续可阅读[05-04 Service Mesh 兴衰](../04-service-mesh/04-service-mesh-rise-fall.md)理解东西向流量治理，再阅读[05-05 RDMA/NVLink/NCCL](../05-rdma-nvlink-nccl/05-rdma-nvlink-nccl.md)进入 AI 集群网络。

## 关键词

API Gateway, Envoy, Kong, Nginx, Gateway API, OIDC, 限流, 灰度发布, AI Gateway, Token 预算
