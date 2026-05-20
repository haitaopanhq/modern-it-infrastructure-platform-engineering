# SLA 为什么不是运维口号

<!-- yitu-r2-assets:start -->

## 相关文章配图

![SLA 为什么不是运维口号](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82SLA%E4%B8%BA%E4%BB%80%E4%B9%88%E4%B8%8D%E6%98%AF%E8%BF%90%E7%BB%B4%E5%8F%A3%E5%8F%B7-2026-0515.png)

![SLA 为什么不是运维口号](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%20SLA%20%E4%B8%BA%E4%BB%80%E4%B9%88%E4%B8%8D%E6%98%AF%E8%BF%90%E7%BB%B4%E5%8F%A3%E5%8F%B7.png)

![容量预留为什么越来越贵](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%E5%AE%B9%E9%87%8F%E9%A2%84%E7%95%99%E4%B8%BA%E4%BB%80%E4%B9%88%E8%B6%8A%E6%9D%A5%E8%B6%8A%E8%B4%B5.png)

![容量预留背后的问题](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%E5%AE%B9%E9%87%8F%E9%A2%84%E7%95%99%E8%83%8C%E5%90%8E%E7%9A%84%E9%97%AE%E9%A2%98.png)

![闲置资源如何吞掉预算](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%E9%97%B2%E7%BD%AE%E8%B5%84%E6%BA%90%E5%A6%82%E4%BD%95%E5%90%9E%E6%8E%89%E9%A2%84%E7%AE%97.png)

![成本、性能与体验的三角关系](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%E6%88%90%E6%9C%AC%E3%80%81%E6%80%A7%E8%83%BD%E4%B8%8E%E4%BD%93%E9%AA%8C%E7%9A%84%E4%B8%89%E8%A7%92%E5%85%B3%E7%B3%BB.png)

![容量与成本](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E5%AE%B9%E9%87%8F%E4%B8%8E%E6%88%90%E6%9C%AC.png)

<!-- yitu-r2-assets:end -->
> **SLA 不是运维部门的 KPI，而是业务与技术之间的契约。**

## 核心观点

很多企业把 SLA 当作运维部门自己的考核指标，但在成熟组织里，SLA = SLO + Error Budget，是整个业务系统的真实边界。

99.9%（三个九）和 99.99%（四个九）之间，不是一个等级的技术难度，而是一个数量级的成本差距。企业需要回答的不是"能不能做到四个九"，而是"业务愿意为那 0.09% 付多少钱"。

## 冲突认知

- 很多人以为 SLA 越高越好
- 现实：每增加一个九，基础设施成本可能翻倍。关键是**知道什么时候叫停**

## 延伸阅读

- 书籍第 1 章：[现代 IT 系统全景](../../01-modern-it-systems.md)
- [成本、性能与体验的三角关系](./cost-performance-experience.md)
- [业务增长之后，可靠性会变成成本问题](./reliability-cost.md)
