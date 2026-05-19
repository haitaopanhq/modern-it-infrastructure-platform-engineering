# 一图读懂 监控的前生今世

> **演进主线**：Nagios/Zabbix → Prometheus/Grafana → OpenTelemetry → AIOps → AI Native Operations

## 核心观点

**监控正在从"看机器状态"，走向"理解系统行为"，再走向"AI Native Operations"。**

传统监控逻辑：采集指标 → 设置阈值 → 告警。CPU 高了报警，磁盘满了报警，服务 Down 了报警。那个时代系统很简单：单体应用、物理机、VM。

但云原生之后，Kubernetes、微服务、Service Mesh、GPU 集群让系统复杂度指数级上升。一个请求可能跨越 20+ 微服务。传统监控只能告诉你"Something is wrong"，却无法回答"Why"。

于是行业进入 Observability（可观测性）时代：Metrics + Logs + Traces + eBPF 开始统一关联。

## 演进路径

| 时代 | 特点 | 代表技术 |
|------|------|----------|
| 基础运维 | 单点阈值 | Nagios、Zabbix、Cacti |
| 可观测性 | 上下文关联 | Prometheus、OpenTelemetry、Loki、Tempo |
| AIOps | 智能分析 | 异常检测、根因定位、拓扑分析 |
| AI Native Ops | AI 自主运维 | LLM 辅助、AI Agent 自愈 |

## 冲突认知

- 很多人以为监控 = 指标 + 告警
- 现实：现代系统需要的是关联上下文，而不是单点指标

- 很多人以为数据多是好事
- 现实：TB/day 的日志 + 亿级 Metrics 已经让人类无法分析，才需要 AIOps

## 信息图 Prompt

```
《一图读懂监控的前生今世》

风格：蓝白科技时间轴
左侧：过去——Nagios、Zabbix、阈值告警、"看机器状态"
右侧：现在——Prometheus、OpenTelemetry、eBPF、"理解系统行为"
未来：AIOps → LLM + AI Agent → "AI Native Operations"
底部金句：
"从监控已知问题，变成探索未知问题。"
```

## 延伸阅读

- 书籍第 5 章：[可观测性与监控](../../05-observability.md)
