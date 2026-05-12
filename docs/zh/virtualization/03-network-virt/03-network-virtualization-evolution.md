# 02-03: 一图看懂网络虚拟化演进

## 核心观点

网络虚拟化的核心，是把物理交换机、网段、路由、安全策略和负载均衡能力，抽象成可以随工作负载移动的逻辑网络。它从 VLAN 的二层隔离开始，发展到虚拟交换机、VXLAN Overlay、SDN 控制器、Kubernetes CNI、eBPF 数据面和服务网格，让网络从“机房布线问题”变成“平台 API 问题”。

这条演进线解决了规模和敏捷性，也引入了新的复杂度。Overlay 可以突破 VLAN 数量限制，但带来封装开销和排障难度；CNI 可以让 Pod 自动入网，但网络策略、DNS、负载均衡和跨集群通信仍然需要清晰设计。网络虚拟化越成熟，越需要统一控制面和可观测性。

## 图表结构

```
传统物理网络
  -> VLAN / ACL / L2-L3 设备配置
虚拟化网络
  -> Linux Bridge / Open vSwitch / vNIC
Overlay 网络
  -> VXLAN / Geneve / GRE
云原生网络
  -> CNI / NetworkPolicy / Service / Ingress
可编程数据面
  -> eBPF / XDP / DPU 卸载
服务通信层
  -> API Gateway / Service Mesh / mTLS
```

图表的关键是网络边界从交换机端口移动到了工作负载附近。虚拟机的 vNIC、容器的 veth、Pod 的 IP、服务的 VIP 和网格的 Sidecar 都是网络抽象的一部分。物理 Underlay 仍然重要，但租户和应用看到的是逻辑网络。

这也让排障视角发生变化。过去网络问题常从交换机端口查起，现在同一次失败可能跨越 DNS、Service、CNI、主机路由、Overlay 隧道、负载均衡和服务网格。图中的每一层都可能改写源地址、目标地址、端口、证书或策略，缺少链路视图就很难定位。

## 演进脉络

VLAN 解决了早期多业务隔离，但 4096 个 ID 很快无法支撑大规模云平台。虚拟交换机让同一台宿主机上的虚拟机可以像接入交换机一样通信，Open vSwitch 又把隧道、流表和 SDN 控制能力带入主机。

VXLAN/Geneve 等 Overlay 技术把二层网络封装在三层网络之上，让逻辑网络可以跨机架、跨可用区扩展。Kubernetes 进一步要求网络按 Pod 生命周期自动创建，CNI 插件因此成为平台关键组件。近年 eBPF 数据面减少 iptables 规则膨胀，DPU 则把部分网络处理卸载到硬件侧。

同时，南北向入口也从单一负载均衡演进为 Ingress、Gateway API、API Gateway 和 Service Mesh 的组合。网络虚拟化不再只处理连通性，还要承载发布策略、证书、安全策略、审计和可观测数据。

因此，网络平台既是连接系统，也是治理系统。

## 关键技术栈

| 技术 | 作用 | 平台工程关注点 |
| --- | --- | --- |
| VLAN/VRF | 基础隔离与路由域 | 物理网络规划与边界 |
| Linux Bridge/OVS | 主机虚拟交换 | VM/容器接入与隧道 |
| VXLAN/Geneve | Overlay 封装 | MTU、Underlay、VTEP |
| CNI | Kubernetes 网络插件接口 | IPAM、策略、性能 |
| Calico/Cilium | 云原生网络实现 | BGP、eBPF、NetworkPolicy |
| Ingress/Gateway API | 南北向流量入口 | TLS、路由、发布治理 |
| Service Mesh | 服务间通信治理 | mTLS、流量策略、观测成本 |

## 误区与现实

- 误区：Overlay 让物理网络不重要。现实：Underlay 的丢包、MTU、拥塞和路由收敛会直接影响 Overlay。
- 误区：CNI 只是安装插件。现实：CNI 决定 IP 地址、策略、性能、排障方式和跨集群演进路径。
- 误区：Service Mesh 能解决所有网络问题。现实：网格主要解决服务通信治理，不替代基础网络、DNS 和负载均衡设计。

## 最佳实践

网络设计要先区分 Underlay、Overlay、服务入口和东西向治理。Underlay 追求稳定、简单和可观测；Overlay 负责租户与工作负载隔离；Ingress/Gateway 负责发布入口；服务网格只在需要细粒度策略、mTLS 和可观测时引入。

平台团队应建立端到端排障路径：从 Pod DNS、Service、CNI、主机路由、隧道封装、物理交换机到对端应用都要有指标和抓包方法。AI 集群还要单独关注 RDMA、RoCE、ECN、PFC 和多网卡拓扑，不能把训练网络当普通业务网。

网络变更管理也要适应虚拟化后的速度。过去改一个 VLAN 可能走机房流程，现在一个应用发布就可能创建 Service、Ingress、证书、策略和 DNS 记录。平台需要用策略即代码、准入校验和自动回滚控制风险，否则逻辑网络的敏捷性会变成不可见的复杂度。

对开发者而言，理想体验是“声明服务意图”，而不是学习所有网络设备命令。对平台团队而言，理想状态是每一次逻辑网络变更都能追溯到提交、审批、策略和运行指标。二者结合，网络虚拟化才真正服务平台工程。

## 与长文互链

- 长文计划：[02-LF-01: 从虚拟机到云原生沙箱：虚拟化为什么仍是平台底座](../longform/02-virtualization-platform-foundation.md)
- 相关短文：[02-01: 计算虚拟化演进](../01-compute-virt/01-compute-virtualization-evolution.md)
- 相关短文：[02-04: 资源池化历史](../04-resource-pooling/04-resource-pooling.md)

## 关键词

网络虚拟化, VLAN, Open vSwitch, VXLAN, Geneve, CNI, Calico, Cilium, eBPF, Service Mesh, Gateway API
