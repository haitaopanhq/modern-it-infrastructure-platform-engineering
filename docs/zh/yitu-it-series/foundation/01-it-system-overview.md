# 一图概览 IT 系统

> **演进主线**：单体 → 微服务 → VM → Kubernetes → CPU → GPU → 单机 → 分布式 → SSH → Control Plane

## 核心观点

**现代 IT 最大的问题已经不是功能，而是复杂度。**

过去一个网站，Nginx + Java + MySQL + Linux 就够了。运维 SSH 登录，看看日志，大概就知道问题在哪。那时候系统原始，但至少"人还能理解系统"。

现在一个请求，可能经过 API Gateway → 微服务 → MQ → Redis → Kubernetes → Service Mesh → 对象存储 → GPU 推理 → AI Gateway。最后没人敢说"我真正理解整个系统"。

## 信息图 Prompt

```
《一图看懂现代 IT 系统全景》

风格：蓝白科技风，企业级架构海报
中央：从"单体 → 分布式"的演进时间轴
左侧：技术栈演进（VM→K8s, CPU→GPU, SSH→CP）
右侧：复杂度爆炸维度
底部金句：
"现代 IT 最大的问题已经不是功能，而是复杂度。"
```

## 冲突观点

- 很多人以为现代 IT 的问题是"技术不够先进"
- 现实：大多数系统已经"功能过剩"，真正的问题是复杂度失控

## 延伸阅读

- 书籍第 1 章：[现代 IT 系统全景](../../01-modern-it-systems.md)
- [业务部门和 IT 部门，到底在关注什么？](./02-business-vs-it.md)
- [现代 IT 复杂度图解](../complexity/modern-it-complexity.md)
