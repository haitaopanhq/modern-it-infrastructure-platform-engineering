# 一图看懂 计算虚拟化演进

<!-- yitu-r2-assets:start -->

## 相关文章配图

![计算虚拟化演进](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E8%99%9A%E6%8B%9F%E5%8C%96/%E8%AE%A1%E7%AE%97%E8%99%9A%E6%8B%9F%E5%8C%96.png)

![虚拟化技术的演变](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E7%B3%BB%E7%BB%9F%E5%A4%8D%E6%9D%82%E5%BA%A6/%E8%99%9A%E6%8B%9F%E5%8C%96%E6%8A%80%E6%9C%AF%E7%9A%84%E6%BC%94%E5%8F%98.png)

![虚拟化从未消失](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E8%99%9A%E6%8B%9F%E5%8C%96/%E8%99%9A%E6%8B%9F%E5%8C%96%E4%BB%8E%E6%9C%AA%E6%B6%88%E5%A4%B1.png)

<!-- yitu-r2-assets:end -->
## 核心观点

**计算虚拟化是从"独占硬件"到"共享资源池"的演进历程。**

从最开始的物理机独占，到 Hypervisor 虚拟化、KVM 统一生态、容器轻量化，再到 GPU 虚拟化与 AI 调度。每一代计算虚拟化都在回答同一个问题：如何让计算资源被更灵活地利用。

## 演进路径

| 时代 | 隔离粒度 | 代表技术 |
|------|---------|----------|
| 物理机时代 | 整机独占 | 物理服务器、Bare Metal |
| Hypervisor 时代 | 虚拟机 | VMware ESXi、Xen、KVM |
| 容器时代 | 进程级 | Docker、containerd |
| Serverless | 函数级 | AWS Lambda、Knative |
| GPU 虚拟化 | 算力切片 | MIG、vGPU、GPU Pooling |

## 冲突认知

- 很多人以为容器完全取代了虚拟机
- 现实：K8s 大量跑在 VM 上，虚拟化只是从计算层下沉到了基础设施层

## 延伸阅读

- [一图看懂 资源抽象史](./resource-abstraction.md)
- [虚拟化从未消失：从大型机诞生那一天，它就一直在演变](../essays/virtualization-never-died.md)
