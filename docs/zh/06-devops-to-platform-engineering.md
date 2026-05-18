# 第 6 章：从手工管理到现代平台工程

![平台工程图解](../zh/diagrams/06-07-platform-engineering.png)

## 本章概述

本章的现实问题是：为什么技术复杂度背后，其实是一场控制权迁移。

手工运维时代，控制权在人手里；脚本化时代，控制权进入脚本；CI/CD 时代，控制权进入流水线；GitOps 时代，控制权进入 Git；平台工程时代，控制权被产品化，成为开发者可以自助使用、企业可以统一治理的内部能力。

## 6.1 运维演进历程

“一图看懂手工运维到现代平台工程的完整演进”背后，不是工具越来越先进，而是组织越来越无法承受不可重复、不可审计、不可回滚的人肉操作。

### 发展阶段

| 阶段 | 特征 | 工具 | 痛点 |
|------|------|------|------|
| 手工时代 | 人肉运维 | SSH, 脚本 | 不可重复，依赖"老师傅" |
| 脚本时代 | 自动化脚本 | Bash, Python | 难以维护，无标准化 |
| 配置管理 | 声明式配置 | Ansible, Puppet | 学习曲线陡 |
| 容器时代 | 镜像化部署 | Docker, K8s | 复杂度高 |
| 平台工程 | 自助服务平台 | Backstage, Port | 文化建设难 |

### 演进路线图

```
┌─────────────────────────────────────────────────────────────────┐
│                      运维能力演进                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  手工 → 脚本 → 配置管理 → 容器化 → 编排 → 平台工程            │
│   │       │          │         │       │         │             │
│   │       │          │         │       │         ▼             │
│   │       │          │         │       │    ┌─────────────┐    │
│   │       │          │         │       │    │ Golden Path │    │
│   │       │          │         │       │    │  自助服务   │    │
│   │       │          │         │       │    └─────────────┘    │
│   │       │          │         │       │                       │
│   └───────┴──────────┴─────────┴───────┴───────────────────────┘
│                                                                 │
│  效率 ↑                                                      │
│  复杂度 ↑                                                      │
└─────────────────────────────────────────────────────────────────┘
```

## 6.2 IaC (Infrastructure as Code)

### 主流 IaC 工具对比

| 工具 | 类型 | 特点 | 适用场景 |
|------|------|------|----------|
| Terraform | 声明式 | 跨云，HCL 语言 | 多云基础设施 |
| OpenTofu | 声明式 | Terraform 分支 | 开源优先 |
| Pulumi | 声明式 | 代码化，主流语言 | 开发者友好 |
| Ansible | 过程式 | SSH，无状态 | 配置管理 |

### Terraform 工作流程

```
1. Write (编写)
   └─ main.tf → 定义基础设施

2. Init (初始化)
   └─ terraform init → 下载 Provider

3. Plan (计划)
   └─ terraform plan → 预览变更

4. Apply (应用)
   └─ terraform apply → 执行变更

5. Destroy (销毁)
   └─ terraform destroy → 清理资源
```

### 示例：AWS EKS 集群

技术旁注：下面的 IaC 示例用于说明“基础设施被代码化”后的表达方式。主线不是 Terraform 语法，而是资源状态开始脱离个人操作，进入可评审、可回滚、可追踪的工程流程。

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"
  
  cluster_name    = "my-cluster"
  cluster_version = "1.28"
  
  vpc_id                         = module.vpc.vpc_id
  subnet_ids                     = module.vpc.private_subnets
  
  eks_managed_node_group_defaults = {
    ami_type = "AL2_x86_64"
  }
  
  eks_managed_node_groups = {
    primary = {
      name = "primary-node-group"
      
      instance_types = ["m5.large"]
      
      min_size     = 2
      max_size     = 5
      desired_size = 3
    }
  }
}
```

## 6.3 CI/CD

### CI/CD 流程

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Code   │──→ │  Build  │──→ │  Test   │──→ │ Stage   │──→ │  Prod   │
│ Commit  │    │  编译   │    │  测试   │    │ 预发布  │    │ 生产    │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │             │             │              │
     ↓              ↓             ↓             ↓              ↓
  Git Hook    Docker Build   Unit Test    Integration    Canary
               Package       E2E Test     Smoke Test    Blue-Green
```

### 主流 CI/CD 工具

| 工具 | 类型 | 特点 | 适用场景 |
|------|------|------|----------|
| Jenkins | 自托管 | 插件丰富，灵活 | 大型企业 |
| GitLab CI | 自托管/GitLab | 与 Git 深度集成 | GitLab 用户 |
| GitHub Actions | SaaS | 生态丰富，易用 | GitHub 用户 |
| ArgoCD | GitOps | 声明式，K8s 原生 | K8s 部署 |

## 6.4 GitOps

### GitOps 核心概念

```
┌─────────────────────────────────────────────────────────┐
│                      GitOps 流程                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐       ┌─────────────┐                │
│   │   Git Repo  │       │  Git Repo   │                │
│   │ (Desired    │       │ (Actual     │                │
│   │   State)    │       │   State)    │                │
│   └──────┬──────┘       └──────┬──────┘                │
│          │                     │                        │
│          │  Pull               │  Observe               │
│          ↓                     ↓                        │
│   ┌──────────────────────────────────────────────┐     │
│   │              GitOps Controller                │     │
│   │  (ArgoCD / Flux)                              │     │
│   │                                               │     │
│   │  Compare: Desired vs Actual                  │     │
│   │  Diff: kubectl apply -f manifest             │     │
│   └──────────────────────┬───────────────────────┘     │
│                          │                              │
│                          ↓                              │
│                  ┌──────────────┐                       │
│                  │ Kubernetes   │                       │
│                  │   Cluster    │                       │
│                  └──────────────┘                       │
└─────────────────────────────────────────────────────────┘
```

### ArgoCD 示例

技术旁注：GitOps 示例用于说明“期望状态”如何成为控制权入口。真正改变的不是发布按钮，而是谁定义状态、谁校正状态、谁审计状态。

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/my-app
    targetRevision: HEAD
    path: deploy/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## 6.5 平台工程

### 平台工程定义

> 平台工程是构建和运营内部开发者平台的学科，目标是优化开发者体验，加快业务价值交付。

### 核心组件

```
┌─────────────────────────────────────────────────────────┐
│                  平台工程架构                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────────────────────────────────────────┐  │
│   │              Developer Portal                    │  │
│   │  (Backstage / Port / Gatsby)                    │  │
│   └──────────────────────┬──────────────────────────┘  │
│                          │                               │
│   ┌──────────────────────┼──────────────────────────┐  │
│   │                      │                          │  │
│   ↓                      ↓                          ↓  │
│┌──────────┐      ┌──────────────┐       ┌──────────┐ │
││ 应用模板  │      │  服务目录    │       │ 资源目录 │ │
││ (Cookiecutter│     │ (Service    │       │(Infra    │ │
││ / Templater)│     │  Catalog)   │       │ Catalog) │ │
│└──────────┘      └──────────────┘       └──────────┘ │
│      │                  │                    │        │
│      └──────────────────┼────────────────────┘        │
│                         ↓                              │
│              ┌─────────────────────┐                  │
│              │   Platform Core     │                  │
│              │   (Backstage API)   │                  │
│              └──────────┬──────────┘                  │
│                         │                              │
│    ┌────────────────────┼────────────────────┐        │
│    ↓                    ↓                    ↓        │
│┌─────────┐        ┌─────────┐         ┌─────────┐    │
││ GitOps  │        │  IaC    │         │ Service │    │
││ (ArgoCD)│        │(Terraform)        │ Mesh    │    │
│└─────────┘        └─────────┘         └─────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 平台工程成熟度模型

| 级别 | 特征 | 描述 |
|------|------|------|
| L0 | 手工 | 无标准，纯手工操作 |
| L1 | 标准化 | 有限模板，文档驱动 |
| L2 | 自动化 | CI/CD 自动化，自助服务 |
| L3 | 平台化 | 统一门户，多能力集成 |
| L4 | 智能化 | 智能推荐，预测性运维 |

## 6.6 控制权迁移

### 平台工程改变的是控制权

```
传统模式：
  业务 → 提需求 → 运维/平台 → 交付
  (被动响应，依赖人工)

平台工程模式：
  业务 → 自助平台 → 自动化交付
  (主动自助，标准化+自动化)

关键变化：
- 从"人治"到"法治"
- 从"审批"到"自助"
- 从"定制"到"标准"
- 从"运维驱动"到"开发者驱动"
```

## 本章收束

DevOps 到平台工程的演进说明，自动化不是终点，控制权产品化才是关键。企业最终需要的不是更多脚本，而是一套能稳定交付、持续校正、降低认知负担的平台能力。

下一章进入平台工程核心能力。因为当控制权进入平台后，真正的问题变成：平台如何设计边界、身份、模板、目录、审计和开发者体验，让复杂度被组织长期承接。

- [Platform Engineering Guide](https://platformengineering.org/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Backstage Documentation](https://backstage.io/docs/)
