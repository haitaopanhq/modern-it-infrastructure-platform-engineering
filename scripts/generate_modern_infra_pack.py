#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "zh"
PLAN_DIR = DOCS / "content-planning" / "modern-infrastructure-evolution"
DIAGRAM_DIR = DOCS / "diagrams" / "modern-infrastructure-evolution"
PROMPT_DIR = DIAGRAM_DIR / "prompts"

FONT_REGULAR = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

SERIES = {
    "01": ("Linux 与硬件重新回归", "foundation"),
    "02": ("虚拟化与资源抽象史", "virtualization"),
    "03": ("云平台与控制权迁移", "cloud-platform"),
    "04": ("容器 Runtime 与隔离边界", "runtime"),
    "05": ("网络与数据面时代", "network"),
    "06": ("数据库、缓存与数据流", "data"),
    "07": ("平台工程与 GitOps", "platform"),
    "08": ("可观测性与治理体系", "observability"),
    "09": ("AI Infra 世界", "ai-infra"),
    "10": ("Agent 与下一代控制面", "agent"),
}

TOPICS = [
    ("01", "01", "Linux 为什么从未离开基础设施核心", "linux-never-left", "foundation/01-linux-kernel/01-linux-never-left.md", "从操作系统到云原生底座，Linux 一直承担真实运行时边界。"),
    ("01", "02", "AI 为什么重新回到裸金属", "ai-back-to-baremetal", "foundation/02-hardware/02-ai-back-to-baremetal.md", "AI 工作负载把 GPU、网络、存储和能耗重新推回架构中心。"),
    ("01", "03", "NUMA 与现代服务器", "numa-modern-server", "foundation/03-numa/03-numa-modern-server.md", "NUMA 不是硬件细节，而是高性能基础设施的延迟边界。"),
    ("01", "04", "CPU → GPU → DPU 演进", "cpu-gpu-dpu-evolution", "foundation/04-cpu-gpu-dpu/04-cpu-gpu-dpu-evolution.md", "算力、并行计算和数据面卸载共同改变服务器分工。"),
    ("01", "05", "从 BIOS 到 Kubernetes", "bios-to-kubernetes", "foundation/05-bios-k8s/05-bios-to-kubernetes.md", "基础设施控制权从硬件初始化一路上移到声明式控制面。"),
    ("02", "01", "计算虚拟化演进", "compute-virtualization-evolution", "virtualization/01-compute-virt/01-compute-virtualization-evolution.md", "虚拟化把服务器从固定机器改造成可分配资源。"),
    ("02", "02", "存储虚拟化演进", "storage-virtualization-evolution", "virtualization/02-storage-virt/02-storage-virtualization-evolution.md", "存储抽象从磁盘保护走向分布式容量和服务化能力。"),
    ("02", "03", "网络虚拟化演进", "network-virtualization-evolution", "virtualization/03-network-virt/03-network-virtualization-evolution.md", "网络虚拟化把连接从物理端口迁移到策略和 Overlay。"),
    ("02", "04", "资源池化历史", "resource-pooling-history", "virtualization/04-resource-pooling/04-resource-pooling.md", "云计算真正出售的是统一资源池，而不是单台服务器。"),
    ("02", "05", "Hypervisor 演进", "hypervisor-evolution", "virtualization/05-hypervisor/05-hypervisor-evolution.md", "Hypervisor 没有消失，而是沉到云、容器和安全隔离之下。"),
    ("03", "01", "OpenStack 为什么衰落", "openstack-decline", "cloud-platform/01-openstack/01-openstack-decline.md", "OpenStack 的问题不是组件不够多，而是控制面产品化不够彻底。"),
    ("03", "02", "Kubernetes 为什么统一云原生", "kubernetes-unified-cloud-native", "cloud-platform/02-k8s-unified/02-kubernetes-unified.md", "Kubernetes 用声明式 API 统一了云原生应用的控制循环。"),
    ("03", "03", "公有云控制面", "cloud-control-plane", "cloud-platform/03-cloud-control-plane/03-cloud-control-plane.md", "公有云的核心是资源、身份、账单和治理的统一控制面。"),
    ("03", "04", "云中立架构", "cloud-agnostic-architecture", "cloud-platform/04-cloud-agnostic/04-cloud-agnostic.md", "云中立不是多买几朵云，而是保留架构控制权。"),
    ("03", "05", "多云真正的问题", "multi-cloud-real-problem", "cloud-platform/05-multi-cloud/05-multi-cloud-challenges.md", "多云真正难在治理、身份、网络、成本和组织协同。"),
    ("04", "01", "OCI Runtime", "oci-runtime", "runtime/01-oci-runtime/01-oci-runtime.md", "OCI 把容器运行边界标准化，让生态不再绑定单一工具。"),
    ("04", "02", "containerd 与 Docker", "containerd-and-docker", "runtime/02-containerd-docker/02-containerd-docker.md", "Docker 变成体验入口，containerd 成为生产运行时核心。"),
    ("04", "03", "gVisor/Kata", "gvisor-kata", "runtime/03-gvisor-kata/03-gvisor-kata.md", "沙箱运行时把容器安全边界重新拉回内核和虚拟化层。"),
    ("04", "04", "沙箱隔离演进", "sandbox-evolution", "runtime/04-sandbox/04-sandbox-evolution.md", "隔离从进程边界走向多层防护，安全重新成为基础设施能力。"),
    ("04", "05", "Runtime 与 Kubernetes 的关系", "runtime-kubernetes-relationship", "runtime/05-runtime-k8s/05-runtime-k8s.md", "Kubernetes 负责编排，Runtime 才真正创建和约束工作负载。"),
    ("05", "01", "C10k 到 AI Fabric", "c10k-to-ai-fabric", "network/01-c10k-ai-fabric/01-c10k-to-ai-fabric.md", "网络从解决连接规模，演进到支撑 GPU 集群的计算协同。"),
    ("05", "02", "eBPF 网络革命", "ebpf-network-revolution", "network/02-ebpf-network/02-ebpf-network-revolution.md", "eBPF 让内核数据面可编程，改变网络、观测和安全。"),
    ("05", "03", "API Gateway 演进", "api-gateway-evolution", "network/03-api-gateway/03-api-gateway-evolution.md", "网关从反向代理升级为流量、身份、策略和观测入口。"),
    ("05", "04", "Service Mesh 兴衰", "service-mesh-rise-fall", "network/04-service-mesh/04-service-mesh-rise-fall.md", "Service Mesh 的兴衰说明复杂度必须被价值证明。"),
    ("05", "05", "RDMA/NVLink/NCCL", "rdma-nvlink-nccl", "network/05-rdma-nvlink-nccl/05-rdma-nvlink-nccl.md", "GPU 集群拼的不只是卡数，而是通信效率和拓扑设计。"),
    ("06", "01", "Redis 演进史", "redis-evolution", "data/01-redis/01-redis-evolution.md", "Redis 从缓存工具演进为实时数据结构基础设施。"),
    ("06", "02", "Kafka 演进史", "kafka-evolution", "data/02-kafka/02-kafka-evolution.md", "Kafka 把消息系统升级成企业数据流的事实日志。"),
    ("06", "03", "数据库分布式演进", "distributed-database-evolution", "data/03-distributed-db/03-distributed-db-evolution.md", "数据库分布式化是在一致性、扩展性和运维复杂度之间取舍。"),
    ("06", "04", "CAP 理论", "cap-theorem", "data/04-cap/04-cap-theorem.md", "CAP 不是背概念，而是理解分布式系统边界的语言。"),
    ("06", "05", "数据湖仓演进", "data-lakehouse-evolution", "data/05-data-lakehouse/05-data-lakehouse.md", "湖仓把数据存储、分析和 AI 训练重新放到同一条管线上。"),
    ("07", "01", "DevOps 演进", "devops-evolution", "platform/01-devops/01-devops-evolution.md", "DevOps 的主线不是工具堆叠，而是交付责任和反馈闭环。"),
    ("07", "02", "GitOps", "gitops", "platform/02-gitops/02-gitops.md", "GitOps 把系统期望状态的入口迁移到版本库。"),
    ("07", "03", "Platform Engineering", "platform-engineering", "platform/03-platform-engineering/03-platform-engineering.md", "平台工程把复杂基础设施产品化为可自助能力。"),
    ("07", "04", "IDP 内部开发平台", "idp-internal-developer-platform", "platform/04-idp/04-idp-internal-developer-platform.md", "IDP 是平台工程能力的用户界面和工作流入口。"),
    ("07", "05", "控制权迁移", "control-plane-migration", "platform/05-control-plane-migration/05-control-plane-migration.md", "现代基础设施演进，本质是一部控制权迁移史。"),
    ("08", "01", "监控演进史", "monitoring-evolution", "observability/01-monitoring-history/01-monitoring-evolution.md", "监控从被动告警走向主动解释系统行为。"),
    ("08", "02", "OpenTelemetry", "opentelemetry", "observability/02-opentelemetry/02-opentelemetry.md", "OpenTelemetry 统一了指标、日志、追踪和事件的采集语言。"),
    ("08", "03", "eBPF 可观测性", "ebpf-observability", "observability/03-ebpf-observability/03-ebpf-observability.md", "eBPF 让系统观测从侵入式埋点走向内核级事实。"),
    ("08", "04", "FinOps", "finops", "observability/04-finops/04-finops.md", "FinOps 把云成本从财务后账变成工程治理能力。"),
    ("08", "05", "IAM 与零信任", "iam-zero-trust", "observability/05-iam-zero-trust/05-iam-zero-trust.md", "身份和零信任让治理从网络边界转向每一次访问。"),
    ("09", "01", "AI Runtime", "ai-runtime", "ai-infra/01-ai-runtime/01-ai-runtime.md", "AI Runtime 把模型执行、显存、并发和延迟变成可管理系统。"),
    ("09", "02", "vLLM", "vllm", "ai-infra/02-vllm/02-vllm.md", "vLLM 让推理服务的瓶颈从模型变成调度和内存管理。"),
    ("09", "03", "Ray", "ray", "ai-infra/03-ray/03-ray.md", "Ray 把分布式 Python 工作负载组织成 AI 应用的计算底座。"),
    ("09", "04", "GPU 调度", "gpu-scheduling", "ai-infra/04-gpu-scheduling/04-gpu-scheduling.md", "GPU 调度决定昂贵算力能否被稳定、可审计、可复用地使用。"),
    ("09", "05", "AI Gateway", "ai-inference-gateway", "ai-infra/05-ai-gateway/05-ai-gateway.md", "这里的 AI Gateway 是模型、推理、Token、成本和路由控制层。"),
    ("10", "01", "MCP/ACP", "mcp-acp", "agent/01-mcp-acp/01-mcp-acp.md", "MCP/ACP 把 Agent 与工具、会话和上下文连接成协议层。"),
    ("10", "02", "Agent Runtime", "agent-runtime", "agent/02-agent-runtime/02-agent-runtime.md", "Agent Runtime 负责会话、记忆、工具调用、权限和执行边界。"),
    ("10", "03", "AI Gateway", "agent-control-ai-gateway", "agent/03-ai-gateway/03-ai-gateway.md", "这里的 AI Gateway 是 Agent 控制面入口，连接会话、工具、技能和审计。"),
    ("10", "04", "Multi-Agent", "multi-agent", "agent/04-multi-agent/04-multi-agent.md", "Multi-Agent 的关键不是角色数量，而是任务分解、协调和责任边界。"),
    ("10", "05", "AI Tool Protocol", "ai-tool-protocol", "agent/05-ai-tool-protocol/05-ai-tool-protocol.md", "AI Tool Protocol 让工具调用从即兴集成走向可治理接口。"),
]

LONGFORM_TITLES = {
    "01": ["AI 时代为什么重新看见 Linux", "云时代隐藏了硬件，AI 时代重新暴露硬件", "GPU 为什么重新改变数据中心架构", "为什么 AI 工作负载重新逼近物理极限"],
    "02": ["虚拟化从未消失，只是沉到了更底层", "容器为什么没有淘汰虚拟机", "Kubernetes 为什么依然离不开虚拟化", "云厂商真正卖的不是 VM，而是资源抽象"],
    "03": ["云计算真正卖的不是服务器", "为什么企业越来越害怕云绑定", "Kubernetes 为什么本质是云控制面", "云中立不是多云，而是控制权问题"],
    "04": ["Kubernetes 之下真正运行的是什么", "为什么 Runtime 会在 AI Agent 时代重新重要", "容器真正依赖的是 Linux Kernel", "安全边界为什么重新变成基础设施核心"],
    "05": ["AI 为什么让网络重新变贵", "Kubernetes 之后，真正变化的是数据面", "网络为什么从“连接服务”变成“控制系统”", "GPU 集群真正拼的是通信"],
    "06": ["Redis 为什么会诞生", "Kafka 为什么会成为数据基础设施", "数据库为什么越来越像分布式系统", "AI 为什么重新改变数据系统"],
    "07": ["平台工程不是工具团队", "GitOps 改变的不是发布，而是控制权", "为什么企业最终都会走向平台化", "运维为什么正在消失成系统能力"],
    "08": ["为什么现代 IT 难点从部署转向治理", "可观测性真正变化的是什么", "OpenTelemetry 为什么会统一生态", "AI 时代为什么治理比部署更重要"],
    "09": ["AI Infra 真正拼的是系统工程", "Kubernetes 正在变成 AI Infra 中间层", "GPU 为什么重新定义资源调度", "AI 时代为什么重新看见基础设施"],
    "10": ["Agent 为什么像下一代基础设施", "MCP/ACP 会不会变成 AI 世界协议层", "OpenClaw 与 Agent Gateway 的意义", "AI Agent 为什么会重新定义平台工程"],
}

WEEK_THEME = ["基础设施底层", "数据库 / 数据流", "网络 / 数据面", "平台工程 / GitOps", "AI Infra", "行业观察 / 云厂商 / 开源", "长文总结 / 趋势判断"]


def topic_id(topic: tuple[str, str, str, str, str, str]) -> str:
    return f"{topic[0]}-{topic[1]}"


def han_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def h1(topic: tuple[str, str, str, str, str, str]) -> str:
    return f"# {topic_id(topic)}: 一图看懂 {topic[2]}"


def article_text(topic: tuple[str, str, str, str, str, str]) -> str:
    no, item, title, slug, rel, subtitle = topic
    series_name, _ = SERIES[no]
    lf_slug = f"{no}-lf-01-{slug}.md"
    return f"""{h1(topic)}

## 核心观点

{subtitle}这不是一个孤立技术点，而是《现代基础设施演进史》里的一次抽象上移：底层资源被重新封装，控制权被重新分配，数据面被重新加速，治理能力也从事后检查转向运行时约束。

理解“{title}”，不能只看工具名字。真正要看的是谁拥有系统状态，谁承担故障边界，谁负责成本、性能、安全和审计。当企业把复杂系统变成可复用能力时，这些问题会比单个产品更重要。

## 图表结构

```text
业务目标
  -> 平台入口 / API / 工作流
  -> 控制面: 声明、调度、策略、审计
  -> 数据面: 计算、网络、存储、模型或消息流
  -> 底层约束: 硬件、内核、拓扑、成本、组织边界
```

这张图建议按四层阅读。第一层是业务目标，它决定技术不是为了炫技，而是为了交付稳定性、效率、成本和安全。第二层是控制面，它回答“谁来决定系统应该是什么状态”。第三层是数据面，它回答“请求、数据、模型或任务到底怎样流动”。第四层是底层约束，它提醒我们所有抽象都必须回到物理资源、组织能力和治理边界。

在图片表达上，主视觉应使用蓝白高密度卡片：左侧放演进路线，中间放架构分层，右侧放误区与现实，底部放关键词和一句话总结。读者不需要先懂所有细节，也能顺着箭头看到这项技术如何进入企业能力体系。

## 演进脉络

早期阶段，{title}更多表现为局部工具或局部最佳实践：某个团队解决性能、稳定性、交付或协同问题。随着规模扩大，局部经验开始沉淀为平台能力，配置、接口、身份、网络、存储和观测被统一起来，技术的重点也从“能不能跑”变成“能不能长期治理”。

第二阶段是控制权迁移。人工操作被脚本替代，脚本被声明式接口替代，声明式接口又被平台、网关、调度器和策略系统接管。每一次迁移都会减少直接操作，但也会带来新的治理要求：版本如何追踪，权限如何收敛，成本如何归因，故障如何定位，跨团队如何协同。

到了 AI Infra 和 Agent 控制面阶段，{title}再次被放大。模型、GPU、数据流、工具调用、记忆系统和自动执行让系统复杂度继续上升。企业真正需要的不是更多孤立组件，而是能把这些组件接成稳定闭环的基础设施能力。

## 关键技术栈

| 层次 | 关注对象 | 代表能力 |
| --- | --- | --- |
| 接入层 | API、控制台、CLI、Agent 入口 | 统一入口、权限校验、用户体验 |
| 控制面 | 声明式状态、调度、策略、编排 | 自动校正、审计、回滚、配额 |
| 数据面 | 请求、消息、存储、网络、模型调用 | 吞吐、延迟、隔离、可观测 |
| 治理层 | 身份、成本、安全、合规 | 最小权限、成本归因、风险控制 |
| 底座层 | Linux、硬件、云资源、网络拓扑 | 性能上限、故障域、容量规划 |

## 误区与现实

- 误区：{title}只是一个工具选型。现实：它背后是系统边界和控制权的重新划分。
- 误区：抽象层越高，底层越不重要。现实：高层抽象会隐藏复杂度，但不会消灭延迟、容量、故障域和成本。
- 误区：只要引入平台或云服务就能自动变成熟。现实：成熟来自接口标准、运行规范、观测闭环和组织协同。
- 误区：AI 时代可以绕过传统基础设施。现实：AI 只会更依赖网络、存储、调度、安全和治理。

## 最佳实践

第一，把 {title} 放回系统链路，而不是孤立建设。设计时要明确上游入口、下游资源、失败路径、观测指标和责任归属。每个接口都要回答谁能调用、调用后改变什么状态、失败后如何恢复。

第二，把控制权显式化。凡是涉及资源创建、任务执行、流量转发、数据访问或模型调用的能力，都应有声明式配置、审计记录、回滚路径和最小权限策略。平台不是替人点按钮，而是把正确动作变成默认路径。

第三，把数据面指标纳入日常治理。吞吐、延迟、错误率、排队时间、缓存命中率、GPU 利用率、网络重传和存储 IOPS 都不是排障时才看的指标，而是容量规划和成本控制的输入。

第四，持续沉淀为内容资产。图文负责让读者快速收藏，冲突认知负责传播一个判断，长文负责解释历史脉络。三者互链后，{series_name} 就不再是一组零散选题，而是“复杂系统如何变成企业能力”的一段章节。

## 与长文互链

- 本系列长文：[{no}-LF-01: {LONGFORM_TITLES[no][0]}](../longform/{lf_slug})
- 系列入口：{series_name}
- 总主线：现代基础设施演进，本质是复杂系统如何通过抽象、控制权迁移、数据面强化和治理机制，转化为企业能力。

## 关键词

{title}, {series_name}, 控制权迁移, 数据面, 治理, 平台工程, AI Infra, 企业能力
"""


def longform_text(no: str, index: int, title: str) -> str:
    series_name, _ = SERIES[no]
    related = [t for t in TOPICS if t[0] == no]
    rel_lines = "\n".join(f"- {topic_id(t)} 一图看懂 {t[2]}" for t in related)
    return f"""# {no}-LF-{index:02d}: {title}

## 冲突开场

很多人讨论“{title}”时，容易把问题压缩成一个产品、一个开源项目或一组配置命令。但在《现代基础设施演进史》这条主线里，它真正指向的是一个更大的变化：复杂系统不再依赖少数专家手工维持，而是通过抽象、控制面、数据面和治理机制，被转化为企业可以长期复用的能力。

表层看，技术越来越多：Kubernetes、GitOps、云平台、Runtime、AI Gateway、Agent、可观测性和安全策略不断叠加。底层看，问题始终只有一个：谁来决定系统的状态，谁来执行状态迁移，谁来承担失败后的恢复，谁来证明这一切是可审计、可复现、可治理的。

## 历史脉络

在早期基础设施里，系统靠人和经验运行。工程师登录机器、调整配置、观察日志、重启服务，知识沉淀在个人脑子、脚本目录和故障复盘里。这个阶段的好处是直接，坏处是不可复制：规模一上来，系统稳定性就被人员经验、沟通成本和操作纪律限制。

第二个阶段是自动化和资源抽象。虚拟化让服务器变成资源池，云平台让资源通过 API 被申请，容器和 Kubernetes 让应用状态进入声明式控制循环，GitOps 又把期望状态迁移到版本库。技术栈变复杂了，但复杂的原因不是工具失控，而是企业希望把更多不确定操作变成确定流程。

第三个阶段是 AI Infra 与 Agent 控制面。GPU、模型、向量数据、工具调用、长期记忆和自动执行，把基础设施重新推向更高复杂度。它们要求系统同时处理物理瓶颈、成本瓶颈、安全边界和自动化决策。{series_name} 的价值，就在于把这条演进脉络从单点技术重新还原为系统能力。

## 系统边界

讨论这件事，必须先画清边界。接入层面对的是用户、开发者、业务系统或 Agent；控制面负责声明、调度、策略、身份、审计和回滚；数据面负责真实流量、存储、模型调用、网络转发和任务执行；底座层则承载 Linux、硬件、云资源、网络拓扑和成本结构。

边界不清时，系统会出现三个问题。第一，责任不清：业务以为平台会兜底，平台以为底层服务会兜底，底层团队又看不到业务意图。第二，观测不清：看到错误率上升，却不知道是配置、容量、网络、权限还是模型调用导致。第三，治理不清：权限、成本、数据访问和审计分散在多个系统里，出了问题只能人工拼图。

成熟的基础设施不是把所有东西塞进一个平台，而是让每一层都有清晰接口。平台要屏蔽不必要的复杂度，但不能隐藏关键事实；自动化要减少手工操作，但不能删除审计和回滚；AI Agent 可以参与执行，但必须被身份、权限、策略和观测系统约束。

## 方法论落地

第一步是把能力拆成可治理对象。不要先问“应该选哪个产品”，而要先问“这个能力改变了哪些对象的状态”。资源、应用、数据、模型、身份、任务和工单，都应该有明确的生命周期。生命周期一旦清楚，平台就能定义创建、变更、回滚、删除、审计和告警这些通用动作。

第二步是把默认路径产品化。成熟的平台不会要求每个团队重新理解底层拓扑，也不会把所有权限直接交给个人。它会提供少数经过验证的入口：标准模板、服务目录、环境申请、发布流水线、观测看板、成本归因和安全策略。开发者看到的是自助能力，平台团队管理的是背后的控制面。

第三步是把例外路径显式化。所有企业都会遇到特殊需求：高性能网络、独占 GPU、跨区域容灾、特殊数据合规、临时扩容、模型灰度或紧急修复。例外不是不能存在，但必须有申请、审批、过期、审计和复盘机制。否则例外会逐渐变成新的默认路径，平台能力也会重新退化成人肉运维。

第四步是把观测指标和业务语言接起来。基础设施团队不能只说 CPU、内存、QPS 和错误率，业务团队也不能只说增长、转化和体验。中间需要一层共同语言：SLO、成本单元、容量水位、交付周期、故障恢复时间、变更失败率和安全暴露面。只有这样，技术能力才会变成可讨论、可权衡、可投入的企业能力。

## 控制权、数据面与治理变化

控制权的变化，是这篇长文的主线。过去控制权在人手里，后来进入脚本，再进入云控制面、Kubernetes 控制循环、GitOps 状态入口、平台工程产品界面，最后开始进入 Agent Runtime 和 AI Gateway。每一次迁移都会让人离机器更远，但也要求系统更可解释。

数据面的变化，同样关键。现代基础设施的瓶颈越来越少出现在“有没有功能”，越来越多出现在吞吐、延迟、隔离、拓扑和成本。AI 训练需要高带宽网络和高性能存储，实时数据需要稳定的消息流和缓存策略，Agent 执行需要可靠的工具调用和上下文传递。控制面决定状态，数据面决定状态能否高效发生。

治理的变化，则决定企业能否放心规模化。身份从用户扩展到工作负载和 Agent，审计从变更记录扩展到运行时行为，成本从月末账单扩展到工程决策，安全从边界防护扩展到每次调用。没有治理，抽象越高风险越大；有了治理，抽象才能真正成为企业能力。

## 产业判断

未来几年，基础设施不会因为 AI 变简单。相反，AI 会把过去被云平台隐藏的硬件、网络、存储和调度问题重新暴露出来，也会把过去靠人工判断的运维和平台流程推向自动化执行。真正有壁垒的团队，不是掌握最多工具的团队，而是能把工具组织成稳定控制体系的团队。

企业会继续购买云服务、托管平台和 AI 能力，但它们更关心的是控制权是否可保留，成本是否可解释，状态是否可审计，失败是否可恢复。云中立、平台工程、可观测性、FinOps、IAM、Agent Gateway 这些词最终都会汇到同一件事上：复杂系统必须被产品化、度量化、自动化和治理化。

这也是本系列的长期价值。每一篇图文不是为了追热点，而是把一个技术点放回演进链路：它从哪里来，解决什么边界问题，把控制权交给谁，又如何帮助企业把复杂系统变成可靠能力。

## 对团队能力的影响

对基础设施团队来说，能力边界会从“维护系统”扩展到“设计系统的可操作性”。团队不再只是修机器、写脚本或维护集群，而是要定义接口、约束、指标和默认路径。一个平台是否成功，不看功能清单有多长，而看业务团队是否能在不破坏安全和稳定性的前提下，自助完成高频工作。

对 SRE 和运维团队来说，工作重心会从命令执行转向风险管理。告警不是终点，告警之后要能定位影响面、判断优先级、触发自动化、记录证据并推动复盘。随着 Agent 进入执行链路，人类更需要设计护栏：哪些动作可以自动执行，哪些动作必须人工确认，哪些动作只能给出建议。

对架构师和技术管理者来说，这条主线会改变投资判断。很多工具看起来都能提高效率，但真正值得投入的是那些能降低长期协作成本、提升系统可解释性、减少不可控风险的能力。换句话说，基础设施预算不只是购买资源，也是在购买组织的确定性。

## 内容资产沉淀

这篇长文对应的图文、冲突认知和复盘稿要互相引用。图文负责把结构讲清楚，让读者收藏；冲突认知负责打破误区，让读者转发；长文负责建立完整解释，让读者形成判断。三者合起来，才是《现代基础设施演进史》的内容资产，而不是一次性文章。

后续复用时，每个主题都可以抽成四类材料：一张结构图、一条冲突判断、一篇长文、一个实践清单。结构图解决“看见”，冲突判断解决“记住”，长文解决“理解”，实践清单解决“行动”。如果一个主题不能被拆成这四类材料，就说明它还没有真正沉淀为体系化内容。

## 本文对应图文

{rel_lines}

## 金句收束

技术演进的表层是工具更新，底层是控制权迁移。真正的现代基础设施，不是让系统看起来更复杂，而是让复杂系统可以被声明、被观测、被审计、被恢复，并最终变成企业能力。
"""


def conflict_text(topic: tuple[str, str, str, str, str, str], date: dt.date) -> str:
    no, item, title, slug, rel, subtitle = topic
    series_name, _ = SERIES[no]
    return f"""# {date.isoformat()} 14:00 冲突型认知：{title}

很多人把“{title}”当成一个技术名词来学，所以越学越碎。真正的冲突点是：{subtitle}如果只看工具，你会问它怎么配置；如果看基础设施演进，你会问它把控制权交给了谁、把数据面压力放到了哪里、把治理责任留给了哪个团队。

现代基础设施最容易被误解的地方，是把复杂度当成坏事。复杂度本身不是问题，不可见、不可控、不可审计的复杂度才是问题。{series_name} 这一段要表达的是：企业不是为了追新技术，而是为了把不稳定的人肉经验变成可复用、可度量、可回滚的系统能力。

一句话：{title} 的价值，不在于多一个组件，而在于它重新定义了抽象、控制权、数据面或治理边界。
"""


def prompt_text(topic: tuple[str, str, str, str, str, str]) -> str:
    no, item, title, slug, rel, subtitle = topic
    series_name, _ = SERIES[no]
    return f"""# image2 Prompt: {topic_id(topic)} {title}

Create a vertical Chinese “一图读懂” infrastructure infographic poster.

Canvas:
- 1024x1536, vertical 2:3 ratio
- clean white / very light blue technical background
- high-density but readable layout, no empty marketing hero page

Topic:
- Title: 《一图看懂 {title}》
- Subtitle: {subtitle}
- Series: {series_name}

Visual style:
- modern IT infrastructure education poster
- navy and royal-blue engineering diagram style
- thin rounded rectangular cards, light blue borders, subtle shadows
- blue line icons plus polished 3D infrastructure assets such as servers, cloud, GPU, network fabric, database cylinders
- professional Chinese tech-media style, dense information architecture

Required modules:
1. Top title band with small infrastructure illustrations.
2. Core architecture or evolution diagram for {title}.
3. “传统方式 vs 现代方式” or “误区 vs 现实” comparison.
4. Decision tree or checklist.
5. Bottom modules: “关键词”, “核心价值”, and “一句话总结”.

Color system:
- dark navy #061B55
- primary blue #0B4EDB
- bright blue #2F7BFF
- pale blue #AFCBFF
- background #F7FAFF
- accent green/yellow/red only for status badges

Avoid:
- no dark full-page background
- no decorative blobs
- no stock-photo people
- no unreadable tiny text
- no overlapping cards or labels
- no fake UI screenshots
- no inconsistent icon styles
- no English-only poster
"""


def ensure_dirs() -> None:
    for path in [PLAN_DIR, PLAN_DIR / "conflicts", PLAN_DIR / "recaps", DIAGRAM_DIR, PROMPT_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def cleanup_stale_paths() -> None:
    stale = [
        DOCS / "foundation/longform/01-foundation-control-power.md",
        DOCS / "virtualization/longform/02-virtualization-platform-foundation.md",
    ]
    for path in stale:
        if path.exists():
            path.unlink()


def needs_article_write(path: Path) -> bool:
    if not path.exists():
        return True
    text = path.read_text(encoding="utf-8")
    required = ["## 核心观点", "## 图表结构", "## 演进脉络", "## 关键技术栈", "## 误区与现实", "## 最佳实践", "## 与长文互链", "## 关键词"]
    return any(r not in text for r in required) or len(text.splitlines()) < 55 or han_count(text) < 1200


def write_articles() -> None:
    for topic in TOPICS:
        path = DOCS / topic[4]
        path.parent.mkdir(parents=True, exist_ok=True)
        if needs_article_write(path):
            path.write_text(article_text(topic), encoding="utf-8")


def write_longforms() -> None:
    for no, titles in LONGFORM_TITLES.items():
        _, dirname = SERIES[no]
        target = DOCS / dirname / "longform"
        target.mkdir(parents=True, exist_ok=True)
        for idx, title in enumerate(titles, start=1):
            slug = slugify(title)
            (target / f"{no}-lf-{idx:02d}-{slug}.md").write_text(longform_text(no, idx, title), encoding="utf-8")


def write_schedule_and_conflicts() -> None:
    start = dt.date(2026, 5, 18)
    rows = []
    conflict_index = ["# 50 条冲突型认知索引", ""]
    for idx, topic in enumerate(TOPICS):
        day = start + dt.timedelta(days=idx)
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][day.weekday()]
        week_theme = WEEK_THEME[day.weekday()]
        no, item, title, slug, rel, subtitle = topic
        series_name, _ = SERIES[no]
        if idx < 40:
            lf_idx = idx % 4
            longform = LONGFORM_TITLES[no][lf_idx]
            longform_type = "正式长文"
        else:
            longform = "长文复盘 / 选题储备"
            longform_type = "复盘稿"
        png = f"../../diagrams/modern-infrastructure-evolution/{topic_id(topic)}-{slug}.png"
        prompt = f"../../diagrams/modern-infrastructure-evolution/prompts/{topic_id(topic)}-{slug}.md"
        conflict_path = PLAN_DIR / "conflicts" / f"{day.isoformat()}-{topic_id(topic)}-{slug}.md"
        conflict_path.write_text(conflict_text(topic, day), encoding="utf-8")
        conflict_index.append(f"- [{day.isoformat()} {topic_id(topic)} {title}](conflicts/{conflict_path.name})")
        rows.append((day.isoformat(), weekday, week_theme, topic_id(topic), series_name, title, conflict_path.name, longform_type, longform, png, prompt))

    matrix = [
        "# 现代基础设施演进史 50 天发布矩阵",
        "",
        "起始日期：2026-05-18。每日 08:00 图文、14:00 冲突型认知、18:00 长文或复盘。",
        "",
        "| 日期 | 星期 | 周主题 | 编号 | 子系列 | 08:00 图文 | 14:00 冲突稿 | 18:00 类型 | 18:00 主题 | PNG | Prompt |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        date, weekday, theme, tid, series, title, conflict, lf_type, lf_title, png, prompt = row
        matrix.append(f"| {date} | {weekday} | {theme} | {tid} | {series} | 一图看懂 {title} | [冲突稿](conflicts/{conflict}) | {lf_type} | {lf_title} | [{tid}.png]({png}) | [prompt]({prompt}) |")
    (PLAN_DIR / "publishing-matrix.md").write_text("\n".join(matrix) + "\n", encoding="utf-8")
    (PLAN_DIR / "conflicts.md").write_text("\n".join(conflict_index) + "\n", encoding="utf-8")


def write_recaps() -> None:
    start = dt.date(2026, 6, 27)
    recap_topics = TOPICS[40:]
    for idx, topic in enumerate(recap_topics):
        day = start + dt.timedelta(days=idx)
        no, item, title, slug, rel, subtitle = topic
        text = f"""# {day.isoformat()} 长文复盘 / 选题储备：{title}

## 本日定位

这篇复盘承接 2026-05-18 至 2026-06-26 已发布的正式长文，把《现代基础设施演进史》的主线重新收束到 AI Infra 与 Agent 控制面。当天 08:00 的图文是“一图看懂 {title}”，14:00 的冲突认知只打一个判断，18:00 不再扩展新长文，而是沉淀可复用选题池。

## 本周主线

到这一阶段，读者已经经历了 Linux 与硬件、虚拟化、云平台、Runtime、网络、数据、平台工程、可观测性和 AI Infra 的完整链路。复盘要强调：这些内容不是技术清单，而是一条控制权迁移曲线。复杂系统先被抽象，再被平台化，再被治理，最后才有可能被 Agent 接管一部分任务执行。

## 已发布互链

- 图文：一图看懂 {title}
- 冲突认知：{title} 的价值，不在于多一个组件，而在于重新定义抽象、控制权、数据面或治理边界。
- 总主线：复杂系统如何通过抽象、控制权迁移、数据面强化和治理机制，转化为企业能力。

## 下一批选题池

- {title} 在企业平台中的落地边界
- {title} 与成本治理、身份治理、审计治理的关系
- {title} 在 AI Infra 与 Agent 工作流中的新角色
- 从 {title} 看下一代控制面的产品化机会

## 一句话总结

复盘不是回顾目录，而是把技术点重新接回主线：谁控制系统状态，谁执行状态迁移，谁证明复杂系统仍然可治理。
"""
        (PLAN_DIR / "recaps" / f"{day.isoformat()}-{topic_id(topic)}-{slug}.md").write_text(text, encoding="utf-8")


def write_style_and_index() -> None:
    readme = """# 现代基础设施演进史内容包

本目录保存 2026-05-18 至 2026-07-06 的 50 天发布矩阵、冲突型认知、复盘稿、图片生成清单和视觉规范。仓库是主产物库，Google Drive 只作为历史参考风格来源。
"""
    style = """# GPT image2 视觉规范

- 画布：1024x1536，竖版 2:3。
- 背景：白色或极浅蓝，不使用黑底。
- 色彩：深蓝标题、皇家蓝结构线、浅蓝卡片边框；绿色只用于推荐，黄色用于过渡，红色用于过时或风险。
- 布局：顶部标题带，主体为 3-4 列卡片网格，必须包含结构图或演进图、对比模块、决策树或清单、关键词、核心价值和一句话总结。
- 风格：高密度中文技术信息图，面向基础设施工程师、平台工程团队、SRE 和 AI Infra 团队。
- 禁止：纯观点海报、暗色全页背景、装饰光斑、随机人物、伪造 UI、文字重叠、不可读小字、无意义渐变。
"""
    image_index = ["# 图片生成清单", "", "| 编号 | 主题 | PNG | Prompt |", "| --- | --- | --- | --- |"]
    for topic in TOPICS:
        tid = topic_id(topic)
        slug = topic[3]
        image_index.append(f"| {tid} | {topic[2]} | [{tid}-{slug}.png](../../diagrams/modern-infrastructure-evolution/{tid}-{slug}.png) | [prompt](../../diagrams/modern-infrastructure-evolution/prompts/{tid}-{slug}.md) |")
    (PLAN_DIR / "README.md").write_text(readme, encoding="utf-8")
    (PLAN_DIR / "visual-style.md").write_text(style, encoding="utf-8")
    (PLAN_DIR / "image-generation-index.md").write_text("\n".join(image_index) + "\n", encoding="utf-8")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size=size)


def wrap_text(text: str, max_chars: int) -> list[str]:
    chunks: list[str] = []
    for part in re.split(r"(\s+)", text):
        if not part.strip():
            continue
        while len(part) > max_chars:
            chunks.append(part[:max_chars])
            part = part[max_chars:]
        if not chunks or len(chunks[-1]) + len(part) > max_chars:
            chunks.append(part)
        else:
            chunks[-1] += part
    return chunks


def draw_card(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], title: str, lines: list[str], accent: str = "#0B4EDB") -> None:
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=18, fill="#FFFFFF", outline="#BBD1FF", width=2)
    draw.rounded_rectangle((x1 + 16, y1 + 14, x1 + 190, y1 + 48), radius=12, fill=accent)
    draw.text((x1 + 28, y1 + 20), title, fill="white", font=font(21, True))
    y = y1 + 66
    for line in lines:
        for wrapped in wrap_text(line, 22):
            if y > y2 - 34:
                return
            draw.text((x1 + 24, y), "• " + wrapped, fill="#061B55", font=font(19))
            y += 30


def draw_png(topic: tuple[str, str, str, str, str, str]) -> None:
    no, item, title, slug, rel, subtitle = topic
    tid = topic_id(topic)
    series_name, _ = SERIES[no]
    img = Image.new("RGB", (1024, 1536), "#F7FAFF")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1024, 154), fill="#FFFFFF")
    draw.text((42, 28), f"一图看懂 {title}", fill="#061B55", font=font(48, True))
    draw.text((48, 96), subtitle, fill="#0B4EDB", font=font(24, True))
    draw.rounded_rectangle((730, 28, 968, 112), radius=24, fill="#EAF1FF", outline="#AFCBFF", width=2)
    draw.text((760, 50), f"{no}｜{series_name}", fill="#061B55", font=font(24, True))

    cards = [
        ("核心结构", ["业务目标 -> 平台入口 -> 控制面 -> 数据面 -> 底层约束", "重点看抽象如何上移，控制权如何重新分配。"], "#0B4EDB"),
        ("演进路线", ["人工经验阶段", "脚本和自动化阶段", "平台与声明式控制阶段", "AI Infra / Agent 控制面阶段"], "#2F7BFF"),
        ("误区 vs 现实", [f"误区：{title}只是工具。", "现实：它改变系统边界、责任归属和治理方式。"], "#0B4EDB"),
        ("关键技术栈", ["接入层：API / 控制台 / Agent", "控制面：调度 / 策略 / 审计", "数据面：计算 / 网络 / 存储 / 模型", "治理层：身份 / 成本 / 安全"], "#2F7BFF"),
        ("最佳实践", ["先画清系统边界，再选择工具。", "把权限、审计、回滚、成本纳入默认路径。", "用可观测指标证明抽象是否有效。"], "#0B4EDB"),
        ("关键词", [f"{title}", "控制权迁移", "数据面", "治理", "平台工程", "企业能力"], "#18A058"),
    ]
    positions = [
        (32, 184, 492, 432),
        (532, 184, 992, 432),
        (32, 462, 492, 710),
        (532, 462, 992, 710),
        (32, 740, 992, 1000),
        (32, 1030, 992, 1238),
    ]
    for pos, card in zip(positions, cards):
        draw_card(draw, pos, card[0], card[1], card[2])

    draw.rounded_rectangle((32, 1272, 992, 1436), radius=20, fill="#0B4EDB")
    summary = f"一句话总结：{title} 的价值，不在于多一个组件，而在于把复杂系统变成可声明、可观测、可审计、可恢复的企业能力。"
    y = 1302
    for line in wrap_text(summary, 34):
        draw.text((62, y), line, fill="white", font=font(26, True))
        y += 40
    draw.text((62, 1468), "核心价值：抽象 | 控制权 | 数据面 | 治理 | 企业能力", fill="#061B55", font=font(23, True))
    path = DIAGRAM_DIR / f"{tid}-{slug}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def write_prompts_and_pngs() -> None:
    for topic in TOPICS:
        tid = topic_id(topic)
        slug = topic[3]
        (PROMPT_DIR / f"{tid}-{slug}.md").write_text(prompt_text(topic), encoding="utf-8")
        draw_png(topic)


def slugify(text: str) -> str:
    mapping = {
        "Linux": "linux",
        "AI": "ai",
        "GPU": "gpu",
        "Kubernetes": "kubernetes",
        "Runtime": "runtime",
        "Agent": "agent",
        "Gateway": "gateway",
        "OpenClaw": "openclaw",
        "MCP": "mcp",
        "ACP": "acp",
        "GitOps": "gitops",
        "OpenTelemetry": "opentelemetry",
        "Redis": "redis",
        "Kafka": "kafka",
    }
    slug = text
    for k, v in mapping.items():
        slug = slug.replace(k, v)
    slug = re.sub(r"[“”/、，：？\s]+", "-", slug)
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff-]+", "", slug)
    return slug.strip("-").lower()


def main() -> None:
    ensure_dirs()
    cleanup_stale_paths()
    write_articles()
    write_longforms()
    write_schedule_and_conflicts()
    write_recaps()
    write_style_and_index()
    write_prompts_and_pngs()


if __name__ == "__main__":
    main()
