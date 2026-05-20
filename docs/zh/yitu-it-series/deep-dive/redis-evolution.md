# Redis 诞生与演进

> **从内核页缓存到现代 AI 基础设施的数据热层**

## 核心判断

**Redis 不是缓存，它是现代互联网的"热状态层"。**

## 为什么 Redis 会诞生

早期互联网系统架构简单：Nginx + PHP/Java + MySQL。数据库承担了一切：用户信息、Session、排行榜、消息计数。但磁盘 IO 始终是整个系统最慢的一层。

Linux Kernel 早就用 Page Cache 做优化——但 Kernel Page Cache 只能加速文件系统，无法理解业务语义。它不知道什么是排行榜、Session、计数器。

Redis 本质上就是把"内核态缓存思想"，搬到了"用户态业务系统"。

## Redis 代表的关键架构思想

**不是所有数据都值得立即持久化。** 现代系统开始接受"数据冷热分层"：

- 冷数据 → 数据库
- 热数据 → 内存（Redis）

从某种意义上说，Redis 是互联网业务第一次真正开始"状态分层"。

## 技术亮点

| 维度 | 描述 |
|------|------|
| 核心设计 | 单线程事件循环 + 内存数据结构 = 极致吞吐 |
| 数据结构 | Hash、List、Set、Sorted Set，围绕"高频业务模式"设计 |
| 而非 | 传统数据库强调"关系"，Redis 强调"热点状态" |

## 生态演化

从单机 → Twemproxy/Proxy → Codis → Redis Sentinel → Redis Cluster → 云托管（ElastiCache、Memorystore、Redis Cloud）

自建 vs 云服务的权衡：
- 自建更灵活更便宜，但运维复杂（主从复制、脑裂、持久化、热点 Key、缓存雪崩、AOF Rewrite）
- 云服务更稳定，但成本高、厂商绑定

## AI 时代重新定位

- Agent Session 状态、Memory、Prompt Cache、Embedding 热数据
- AI Gateway 高速状态协调
- 从"互联网缓存"→"AI Infra 热状态层"

**Redis 不只是在缓存数据，它正在变成现代系统的 Memory Fabric。**

## 延伸阅读

- 书籍第 3 章：[数据库系统](../../03-database-systems.md)
