# 一图读懂监控的前生今世

<!-- yitu-r2-assets:start -->

## 相关文章配图

![一图读懂监控系统](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E4%B8%80%E5%9B%BE%E8%AF%BB%E6%87%82%E7%9B%91%E6%8E%A7%E7%B3%BB%E7%BB%9F.png)

![小红书：监控的前生今世](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E5%B0%8F%E7%BA%A2%E4%B9%A6-%E7%9B%91%E6%8E%A7%E7%9A%84%E5%89%8D%E7%94%9F%E4%BB%8A%E4%B8%96.png)

<!-- yitu-r2-assets:end -->
> **演进主线**：Monitoring -> Observability -> AIOps -> AI Observability -> AI Native Operations

## 核心观点

如果把过去二十年的基础设施演进真正串起来看，“监控”这个词其实已经经历了好几次时代变化。

过去监控是在看机器状态，后来变成理解系统行为。到了 AI Native 时代，它还要开始理解 AI 自身。

## 基础运维时代：机器有没有坏

很多人今天一提监控，脑子里第一反应还是 CPU、内存、磁盘、告警、Dashboard。

那其实是最早期的基础运维时代。那个时代系统还很简单：单体应用、物理机、虚拟机、固定网络架构。监控逻辑也很直接：

```text
采集指标 -> 设置阈值 -> 超过阈值就报警
```

CPU 打满报警，磁盘满了报警，服务 Down 了报警。Nagios、Zabbix、Cacti、Munin 这些工具，本质上都在解决同一个问题：

> 机器有没有坏。

因为系统边界清晰、调用链简单、服务数量有限，所以看指标很多时候真的足够。

## 可观测性时代：为什么坏

云计算与云原生时代到来之后，事情彻底变化。

Kubernetes、微服务、Service Mesh、Serverless、GPU 集群、AI 推理服务，让系统复杂度指数级上升。过去一个请求可能只经过一台 Web Server；现在一个请求可能跨越 API Gateway、二十多个微服务、MQ、Redis、数据库、对象存储、向量数据库、LLM Agent 和外部 API。

传统监控第一次暴露边界。它只能告诉你 Something is wrong，却很难回答 Why。

CPU 高了，但到底是哪个服务导致的？延迟抖动了，问题出现在网络、数据库、缓存还是调用链？Pod 重启了，背后是 OOM、探针失败、依赖超时还是节点抖动？

于是行业从 Monitoring 进入 Observability。真正的变化不是换了工具，而是核心逻辑改变了：

> 从监控已知问题，变成探索未知问题。

Metrics、Logs、Traces 开始融合。Prometheus、VictoriaMetrics 负责指标，Loki、ELK 负责日志，Jaeger、Tempo、SkyWalking 负责链路追踪，OpenTelemetry 统一数据采集标准，eBPF 进一步让系统拥有内核级事实。

现代系统真正重要的，已经不是单点指标，而是上下文。

## AIOps 时代：人类看不过来了

新的问题很快出现：数据爆炸。

现代企业每天可能产生 TB 级日志、亿级 Metrics、百亿级 Span。人类不可能再像过去一样靠盯 Dashboard 排查问题。

于是 AIOps 出现。算法和 AI 开始帮助做异常检测、事件关联、拓扑分析、根因定位、容量预测。

运维体系开始从人盯系统，变成系统辅助人。

很多企业后来发现，真正消耗团队精力的，已经不是故障本身，而是告警风暴、日志洪水、上下文缺失和复杂链路分析。

## AI Native Operations：AI 也需要被观测

行业正在进入下一阶段：LLM + AI Agent 时代。

未来真正需要监控的，已经不只是系统本身，而是 AI。

Prompt 是否异常？Token 消耗是否失控？RAG 检索是否偏移？Memory 是否污染？Agent 是否进入循环调用？Tool Calling 是否失败？推理成本是否飙升？模型是否开始幻觉？

Grafana、Langfuse、Helicone、Arize、Weights & Biases、OpenLIT、Phoenix 等 AI Observability 平台快速崛起，是因为未来系统越来越像：

> AI 在运行 AI。

运维体系也会发生更深变化：AI 先分析，AI 先定位，AI 先修复，人类最后确认。

## 一图结构

| 阶段 | 核心问题 | 代表技术 |
|---|---|---|
| Monitoring | 机器有没有坏 | Nagios、Zabbix、Cacti、Munin |
| Observability | 系统为什么坏 | Prometheus、Loki、Tempo、OpenTelemetry、eBPF |
| AIOps | 人类看不过来了 | 异常检测、事件关联、根因定位、容量预测 |
| AI Observability | AI 行为是否可解释 | Langfuse、Helicone、Arize、OpenLIT、Phoenix |
| AI Native Operations | AI 如何参与修复系统 | LLM Ops、Agent 自愈、Human Confirmation |

## 一句话总结

监控体系真正的演进，是一条清晰路径：

```text
Monitoring -> Observability -> AIOps -> AI Native Operations
```

过去监控是在看机器状态，后来变成理解系统行为，而未来，它会进一步变成理解 AI 自身。

## 封面图提示词

低信息密度封面图，主题为“从监控机器到理解 AI”。画面左侧是传统 Dashboard 和服务器指标，中间是 Observability 三元组 Metrics / Logs / Traces 汇聚成一条链路，右侧是 AI Agent 分析告警并给出根因。只保留三段结构，不放密集图标，整体为蓝白科技书籍封面风格。

## 延伸阅读

- 书籍第 5 章：[可观测性与监控](../../05-observability.md)
