# 《图解 IT 技术演进史》书籍目录与子目录规划

## 定位

《图解 IT 技术演进史》不是一组工具教程，而是一部围绕「技术 × 商业 × 焦虑 × 系统复杂度」展开的基础设施技术史。

它从已经发布的一图文章出发，把零散选题组织成一条主线：企业为什么会从单机权限、内网信任、资源抽象、云平台、身份体系、算力竞争，一路走到稳定性保卫战和控制权战争。

## 目录总览

| 卷 | 大类 | 子目录 | 核心矛盾 |
|---|---|---|---|
| 00 | 《图解 IT 技术演进史》系列回顾 | `00-series-review/` | 先给读者一张全局地图 |
| 01 | 单机时代 | `01-single-machine-era/` | Root 权力过大，系统需要权限制衡 |
| 02 | 网络时代 | `02-network-era/` | 内网曾经可信，但业务扩张会击穿默认信任 |
| 03 | 云上帝国 | `03-cloud-empire/` | 云给了企业无限扩容的想象，也制造了新的依赖 |
| 04 | 重建信任 | `04-rebuilding-trust/` | 企业需要在跨系统、跨团队、跨网络中重建身份秩序 |
| 05 | 算力之争 | `05-compute-war/` | AI 让基础设施重新回到物理世界和数据中心核心 |
| 06 | 稳定性保卫战 | `06-stability-defense/` | 增长会把所有隐藏复杂度推到高峰流量面前 |
| 07 | 从技术复杂度延伸到业务支撑 | `07-complexity-to-business/` | 复杂度最终不是技术问题，而是控制权和企业能力问题 |

## 00. 《图解 IT 技术演进史》系列回顾

目录：`docs/zh/yitu-it-series/00-series-review/`

这一卷是全书入口，不强调单篇技术细节，而是让读者先看到现代 IT 的全局地图。

| 顺序 | 标题 | 建议文件名 | 章节作用 |
|---|---|---|---|
| 00-01 | 一图概览 IT 系统 | `01-it-system-overview.md` | 建立“复杂度才是现代 IT 主问题”的总判断 |
| 00-02 | 一图读懂 IT 安全体系 | `02-it-security-system.md` | 从安全边界引出身份、权限、治理 |
| 00-03 | 一图读懂 数据库 | `03-database-overview.md` | 说明业务状态如何沉淀为数据系统 |
| 00-04 | 一图读懂 存储服务 | `04-storage-services.md` | 说明数据留存、成本和访问模式如何塑造存储 |
| 00-05 | 一图读懂 网络与协议 | `05-networking-protocols.md` | 说明连接如何升级为数据面和控制系统 |
| 00-06 | 一图读懂 监控的前生今世 | `06-monitoring-evolution.md` | 说明系统不可知如何引出可观测性 |
| 00-07 | 一图看懂 手工运维到现代平台工程的完整演进 | `07-ops-to-platform-engineering.md` | 说明控制权如何从人转向平台 |
| 00-08 | 一图看懂 AI世界 | `08-ai-world.md` | 作为 AI Infra 和算力之争的过渡 |

## 01. 单机时代

目录：`docs/zh/yitu-it-series/01-single-machine-era/`

这一卷从最朴素的系统权力讲起：一台机器、一个 Root、一个操作系统，为什么也会产生安全、权限和治理问题。

| 顺序 | 标题 | 建议文件名 | 章节作用 |
|---|---|---|---|
| 01-01 | 一图看懂 Root 为什么既强大又危险 | `01-root-power-and-risk.md` | 从 Root 引出系统最高权限的两面性 |
| 01-02 | 一图看懂 Linux 从“中央集权”到权限制衡 | `02-linux-permission-balance.md` | 讲用户、组、sudo、capabilities、namespace 的演进 |
| 01-03 | 从 Root 到最小权限：单机时代安全模型的本质 | `03-root-to-least-privilege.md` | 作为本卷长文，收束到最小权限原则 |

## 02. 网络时代

目录：`docs/zh/yitu-it-series/02-network-era/`

这一卷讲企业最早的安全幻觉：只要在内网里，系统就默认可信。但网络一旦连接业务、组织和外部合作方，信任边界就会开始破裂。

| 顺序 | 标题 | 建议文件名 | 章节作用 |
|---|---|---|---|
| 02-01 | 一图看懂：局域网时代的“内网安全可信” | `01-lan-trusted-network.md` | 解释内网可信假设为什么成立，又为什么会失效 |

## 03. 云上帝国

目录：`docs/zh/yitu-it-series/03-cloud-empire/`

这一卷讲云平台的真正变化：它不是让企业少买服务器，而是让企业第一次相信资源可以被抽象、池化、按需调度。

| 顺序 | 标题 | 建议文件名 | 章节作用 |
|---|---|---|---|
| 03-01 | 一图看懂 资源抽象史 | `01-resource-abstraction-history.md` | 建立云时代的核心语言：资源抽象 |
| 03-02 | 一图看懂 计算虚拟化演进 | `02-compute-virtualization.md` | 讲 VM、Hypervisor、容器与计算池化 |
| 03-03 | 一图看懂 存储虚拟化演进 | `03-storage-virtualization.md` | 讲 RAID、SAN、Ceph、CSI 与存储池 |
| 03-04 | 一图看懂 网络虚拟化演进 | `04-network-virtualization.md` | 讲 VLAN、VXLAN、CNI、Service Mesh 与数据面 |
| 03-05 | 一图看懂从单体应用到分布式架构 | `05-monolith-to-distributed.md` | 解释业务复杂度如何推动架构拆分 |

## 04. 重建信任

目录：`docs/zh/yitu-it-series/04-rebuilding-trust/`

这一卷讲企业身份体系的出现。系统越来越多之后，信任不可能继续绑定在一台机器、一个内网或一个管理员身上。

| 顺序 | 标题 | 建议文件名 | 章节作用 |
|---|---|---|---|
| 04-01 | 一图看懂：AD / LDAP / Kerberos 的出现 | `01-ad-ldap-kerberos.md` | 解释目录、认证、票据和企业身份秩序 |

## 05. 算力之争

目录：`docs/zh/yitu-it-series/05-compute-war/`

这一卷讲 AI 为什么让基础设施重新变成战略资产。算力不再只是 CPU 使用率，而是 GPU、网络、数据、推理成本和现实世界控制权的竞争。

| 顺序 | 标题 | 建议文件名 | 章节作用 |
|---|---|---|---|
| 05-01 | 一图看懂 H200 真正冲击了什么 | `01-h200-impact.md` | 从单张 GPU 扩展到数据中心供给与成本结构 |
| 05-02 | 一图概览 FSD 背后的 AI基座 | `02-fsd-ai-foundation.md` | 用自动驾驶说明数据、训练、推理和闭环系统 |
| 05-03 | 一图看懂 基础设施正在重回核心 | `03-infra-return-to-core.md` | 解释 AI 为什么把硬件、网络、存储重新推上前台 |
| 05-04 | 一图概览 AI 巨头与”现实世界“之争 | `04-ai-giants-real-world.md` | 从模型竞争延伸到终端、机器人、汽车和物理世界入口 |

## 06. 稳定性保卫战

目录：`docs/zh/yitu-it-series/06-stability-defense/`

这一卷讲业务增长之后的基础设施压力。系统平时可用不代表高峰可用，低成本可用不代表长期可靠。

| 顺序 | 标题 | 建议文件名 | 章节作用 |
|---|---|---|---|
| 06-01 | 一图看懂业务增长如何放大 IT 压力 | `01-growth-amplifies-it-pressure.md` | 说明增长如何把局部问题放大成系统问题 |
| 06-02 | 一图读懂容量冗余的本质：用成本换稳定 | `02-capacity-redundancy.md` | 解释冗余、预留和稳定性成本 |
| 06-03 | 一图看懂用户请求如何变成计算压力 | `03-request-to-compute-pressure.md` | 把一次请求拆成链路、依赖和资源消耗 |
| 06-04 | 一图看懂业务峰谷与容量曲线 | `04-traffic-peak-capacity-curve.md` | 解释峰谷、弹性、预留和浪费 |
| 06-05 | 一图看懂性能瓶颈为什么总在高峰出现 | `05-peak-performance-bottleneck.md` | 说明瓶颈为什么总在系统最贵的时候暴露 |

## 07. 从技术复杂度延伸到业务支撑

目录：`docs/zh/yitu-it-series/07-complexity-to-business/`

这一卷是全书的判断层：技术复杂度不会停留在技术部门内部，它最终会变成业务节奏、成本结构、组织协作和控制权问题。

| 顺序 | 标题 | 建议文件名 | 章节作用 |
|---|---|---|---|
| 07-01 | 技术复杂度的背后，其实是一场控制权战争 | `01-control-war.md` | 全书核心长文，解释控制权迁移 |
| 07-02 | 虚拟化从未消失：从大型机诞生那一天，它就一直在演变 | `02-virtualization-never-died.md` | 把虚拟化从技术分类提升为资源抽象史 |
| 07-03 | 流量暴涨的那一刻，Infra 团队到底在害怕什么？ | `03-what-infra-fears-during-traffic-spike.md` | 把稳定性焦虑写成真实组织问题 |
| 07-04 | 云平台真正改变的，不是上云，而是业务第一次拥有“无限扩容”的错觉 | `04-cloud-infinite-scale-illusion.md` | 收束云时代的商业想象与物理边界 |

## 与现有草稿的迁移关系

| 现有素材 | 目标卷册 |
|---|---|
| `foundation/01-it-system-overview.md` | `00-series-review/01-it-system-overview.md` |
| `foundation/02-business-vs-it.md` | `07-complexity-to-business/` 的组织视角素材 |
| `security/security-overview.md` | `00-series-review/02-it-security-system.md` 与 `04-rebuilding-trust/` |
| `data/storage-overview.md` | `00-series-review/04-storage-services.md` |
| `network/network-protocols.md` | `00-series-review/05-networking-protocols.md` 与 `02-network-era/` |
| `observability/monitoring-evolution.md` | `00-series-review/06-monitoring-evolution.md` |
| `platform/devops-to-platform-engineering.md` | `00-series-review/07-ops-to-platform-engineering.md` |
| `virtualization/*.md` | `03-cloud-empire/` |
| `complexity/*.md` | `06-stability-defense/` |
| `essays/control-war.md` | `07-complexity-to-business/01-control-war.md` |
| `essays/ai-redefine-infra.md` | `05-compute-war/` 与后续 AI Infra 过渡 |

## 章节写法

每个子目录中的正式文章按同一模型扩写：

1. 用一个现实问题开场，而不是用“什么是”开场。
2. 用技术史解释这个问题为什么出现。
3. 用结构图说明系统边界、控制权或数据面如何变化。
4. 用商业和组织语言解释成本、稳定性、效率和焦虑。
5. 结尾回到同一句主线：基础设施演进不是工具越来越多，而是抽象、控制权、数据面和治理机制不断重组。
