# 现代 IT 复杂度图解

<!-- yitu-r2-assets:start -->

## 相关文章配图

![现代 IT 系统复杂度](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E7%B3%BB%E7%BB%9F%E5%A4%8D%E6%9D%82%E5%BA%A6/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%E7%8E%B0%E4%BB%A3IT%E7%B3%BB%E7%BB%9F%E5%A4%8D%E6%9D%82%E5%BA%A6.png)

![控制权之争](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E7%B3%BB%E7%BB%9F%E5%A4%8D%E6%9D%82%E5%BA%A6/%E6%8E%A7%E5%88%B6%E6%9D%83%E4%B9%8B%E4%BA%89.png)

<!-- yitu-r2-assets:end -->
> **演进主线**：单体 → 微服务、VM → Kubernetes、CPU → GPU、单机 → 分布式、SSH → Control Plane

## 核心判断

**现代 IT 最大的问题已经不是"系统能不能运行"，而是"人类还能不能理解它"。**

## 复杂度爆炸的表现

一个请求在今天的系统中可能经过：
```
API Gateway → 微服务 → MQ → Redis → Kubernetes → Service Mesh
→ 对象存储 → GPU Runtime → AI Gateway → Agent Runtime
```

最后没人敢说"我真正理解整个系统"。

以前一个 Bug 只是一个进程挂了。现在一个 YAML 配错可能触发：CI/CD → GitOps → K8s 调度 → 网络策略 → 自动扩缩容 → 监控告警 → 连锁反应。

## 组织认知错位

| 角色 | 视角 | 关心的问题 |
|------|------|-----------|
| 业务 | 系统能不能用 | 增长、转化、收入 |
| 研发 | 代码够不够好 | 微服务、K8s、API |
| SRE | 系统稳不稳 | 可用性、延迟、容量 |
| Infra | 资源够不够 | 资源池、网络、存储、GPU |
| 管理层 | 成本合不合理 | 为什么 IT 成本越来越高？ |

## 延伸阅读

- [一图概览 IT 系统](../foundation/01-it-system-overview.md)
- [业务部门和 IT 部门，到底在关注什么？](../foundation/02-business-vs-it.md)
- 书籍第 1 章：[现代 IT 系统全景](../../01-modern-it-systems.md)
