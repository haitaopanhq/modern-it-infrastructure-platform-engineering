# 05. 稳定性战争

<!-- yitu-r2-assets:start -->

## 相关文章配图

![一图看懂高可用](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%E9%AB%98%E5%8F%AF%E7%94%A8.png)

![高可用从哪里开始](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%E9%AB%98%E5%8F%AF%E7%94%A8%E4%BB%8E%E5%93%AA%E9%87%8C%E5%BC%80%E5%A7%8B-2026-0515.png)

![可靠性会变成成本问题](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E4%B8%9A%E5%8A%A1%E5%A2%9E%E9%95%BF%E4%B9%8B%E5%90%8E%EF%BC%8C%E5%8F%AF%E9%9D%A0%E6%80%A7%E4%BC%9A%E5%8F%98%E6%88%90%E6%88%90%E6%9C%AC%E9%97%AE%E9%A2%98.png)

![业务峰谷与容量曲线](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%E4%B8%9A%E5%8A%A1%E5%B3%B0%E8%B0%B7%E4%B8%8E%E5%AE%B9%E9%87%8F%E6%9B%B2%E7%BA%BF-2026-0513.png)

![性能瓶颈为什么总在高峰出现](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%E6%80%A7%E8%83%BD%E7%93%B6%E9%A2%88%E4%B8%BA%E4%BB%80%E4%B9%88%E6%80%BB%E5%9C%A8%E9%AB%98%E5%B3%B0%E5%87%BA%E7%8E%B0.png)

![故障恢复与业务损失](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%E6%95%85%E9%9A%9C%E6%81%A2%E5%A4%8D%E4%B8%8E%E4%B8%9A%E5%8A%A1%E6%8D%9F%E5%A4%B1-2026-0515.png)

![用户请求如何变成计算压力](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E6%8A%80%E6%9C%AF%E8%A7%82%E5%AF%9F/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%E7%94%A8%E6%88%B7%E8%AF%B7%E6%B1%82%E5%A6%82%E4%BD%95%E5%8F%98%E6%88%90%E8%AE%A1%E7%AE%97%E5%8E%8B%E5%8A%9B-2026-0514.png)

<!-- yitu-r2-assets:end -->
命题：用成本购买确定性。

本卷讲业务增长如何把隐藏的技术复杂度推到台前：容量、峰谷、瓶颈、冗余和稳定性成本，最终都会变成业务问题。

| 顺序 | 标题 |
|---|---|
| 05-01 | 一图看懂业务增长如何放大 IT 压力 |
| 05-02 | 一图读懂容量冗余的本质：用成本换稳定 |
| 05-03 | 一图看懂用户请求如何变成计算压力 |
| 05-04 | 一图看懂业务峰谷与容量曲线 |
| 05-05 | 一图看懂性能瓶颈为什么总在高峰出现 |
