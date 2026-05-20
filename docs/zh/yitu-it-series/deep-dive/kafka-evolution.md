# Kafka 诞生与内核缓存

> **把 Linux append-only log 思想，扩展到整个互联网世界**

## 核心判断

**Kafka 不是传统消息队列，它是"分布式 Commit Log 系统"。**

## 为什么 Kafka 会诞生

Kafka 最早诞生于 LinkedIn。当时面临的核心问题是：用户行为数据爆炸——页面点击、搜索行为、推荐系统、广告日志，而且这些数据要被多个系统同时消费。

传统做法是应用直接写数据库，但数据库不是为"海量持续 append-only 写入"设计的。

真正需要的是一个**高吞吐日志流系统**。

## Kafka 本质：把操作系统日志思想搬到分布式世界

Kafka 核心思想非常 Linux：

| 技术 | 用途 |
|------|------|
| Append Log | 顺序写入 |
| Page Cache | 磁盘 IO 优化 |
| Sequential IO | 顺序写远比随机写快 |
| sendfile / 零拷贝 | 数据 Page Cache → NIC，减少 CPU Copy |

Kafka 大部分时候**根本不依赖 JVM Heap 做缓存**，而是**极度依赖 Linux Page Cache**。

写入流程：
```
Producer → Socket Buffer → Kernel Page Cache → 后台异步 flush 到磁盘
```

大量写入其实只是内存里的顺序 append。这和数据库随机写完全不同。

## Kafka vs 传统 MQ

| 维度 | 传统 MQ（RabbitMQ 等） | Kafka |
|------|----------------------|-------|
| 本质 | 任务投递系统 | 可回放日志系统 |
| 消息 | 消费后删除 | 保留，Consumer 自己记录 offset |
| 数据 | 瞬时消息 | 长期可消费数据流 |

Kafka 真正改变的是：数据第一次从"瞬时消息"变成"长期可消费数据流"。

## 生态演化

开源自建 → Confluent 商业化 → 云托管（AWS MSK、Confluent Cloud）→ 新一代 Streaming（Pulsar、Redpanda）

## AI 时代重新定位

AI Agent 世界里，Prompt、Tool Call、Session Event、Memory Sync、RAG Pipeline、Observability Event，全部都在 Event 化。

**Kafka/Pulsar 正在重新成为 AI 基础设施里的数据面中枢。**

## 延伸阅读

- 书籍第 3 章：[数据库系统](../../03-database-systems.md)
