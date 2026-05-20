# 手工运维到现代平台工程的完整演进

<!-- yitu-r2-assets:start -->

## 相关文章配图

![从手工运维到现代平台工程](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E5%B0%8F%E7%BA%A2%E4%B9%A6-%E4%BB%8E%E6%89%8B%E5%B7%A5%E8%BF%90%E7%BB%B4%E5%88%B0%E7%8E%B0%E4%BB%A3%E5%B9%B3%E5%8F%B0%E5%B7%A5%E7%A8%8B.png)

![一图理解平台工程](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E4%B8%80%E5%9B%BE%E7%90%86%E8%A7%A3%E5%B9%B3%E5%8F%B0%E5%B7%A5%E7%A8%8B.png)

<!-- yitu-r2-assets:end -->
> **演进主线**：手工运维 -> 脚本化 -> 配置管理 -> IaC -> CI/CD -> GitOps -> Platform Engineering -> AI Native Platform

## 核心观点

如果把过去二十年的基础设施演进真正串起来看，现代平台工程并不是突然出现的新概念，而是一条非常长的复杂度治理历史。

它真正回答的问题不是“用什么工具部署”，而是：

> 如何把越来越复杂的系统，从依赖人，逐渐变成依赖平台。

## 手工运维时代：系统依赖人

早期基础设施世界几乎没有平台概念。

上线靠 SSH 登录服务器，scp 上传文件，vim 改配置，最后手动 restart 服务。谁知道哪台机器改过配置？谁记得线上跑了哪个版本？谁半夜修过数据库？

所有东西都依赖老师傅经验。系统几乎不可审计、不可回滚、不可复现。

后来大家开始写 Shell、Batch、Python 脚本，希望减少重复劳动。cron、自动发布脚本、批量执行工具开始出现。但很快又进入新的混乱：脚本越来越长，环境越来越漂移，祖传 shell 无人敢删。

那个阶段本质上只是自动化初级阶段。它能提升效率，但系统依然严重依赖人。

## 配置管理时代：机器状态可描述

真正的工程化阶段，是从配置管理时代开始的。

Puppet、Chef、SaltStack、Ansible 第一次尝试把机器状态变成可描述配置。基础设施开始拥有统一节点管理、标准化环境、配置收敛能力。

后来 Apollo、Nacos、Consul、etcd 这些配置中心继续出现，动态配置、服务发现、环境隔离逐渐成为现代系统标配。

但真正的分水岭，是 Terraform、OpenTofu、Pulumi 这类 IaC 工具出现之后。

VPC、DNS、负载均衡、Kubernetes、IAM、安全组这些过去只能手点控制台的资源，开始第一次真正进入 Git。基础设施第一次拥有版本管理、PR Review、Diff、审计、回滚、环境一致性。

IaC 最大的价值，从来不只是自动创建资源，而是让基础设施正式进入软件工程体系。

## CI/CD 与 GitOps：Git 成为事实来源

CI/CD 与 DevOps 改变了软件交付方式。

Jenkins 不是 DevOps 的终点。现代基础设施真正的变化，是 Pipeline as Code、GitOps 与 DevSecOps 的全面出现。

Jenkins Pipeline、GitLab CI、GitHub Actions 把构建、测试、扫描、制品管理、发布流程全部 YAML 化。Trivy、SBOM、Cosign、OIDC、SAST、Policy as Code 这些安全能力，也逐渐进入流水线。

ArgoCD、FluxCD 出现后，行业从“CI 主动 Push 发布”，进入“GitOps 声明式持续收敛”时代。

集群开始主动从 Git 拉取期望状态，自动发现漂移，自动同步，自动回滚。Git 不再只是代码仓库，而逐渐变成整个基础设施的单一事实来源。

## 平台工程：复杂度产品化

Kubernetes、CI/CD、Terraform、RBAC、Service Mesh、Observability、Security Policy 越来越复杂之后，开发者已经无法再理解全部底层。

于是平台团队开始出现。

他们把 Kubernetes、CI/CD、Terraform Module、Golden Path、Service Catalog、RBAC、Observability 封装成开发者自助能力。开发者不再直接面对复杂底层，而是通过标准模板获取环境、权限、流水线、部署能力与监控能力。

现代平台工程真正的目标开始变得清晰：

- 更少人工
- 更低权限
- 更强标准化
- 更高自动化
- 更好的开发者体验
- 更可审计的交付链路

基础设施开始从“运维管理机器”，演变成“向开发者提供产品”。

## AI Native Platform：交付 AI 能力

AI 时代到来之后，这条演进路径继续变化。

未来真正复杂的，已经不只是 Kubernetes 本身，而是 GPU 调度、模型路由、Agent Runtime、AI Gateway、Inference Fabric、Prompt Pipeline、AI Observability。

Platform Engineering 正在进一步向 AI Native Platform 演进。

未来开发者真正申请的，可能不再只是 Kubernetes Namespace，而是 GPU 配额、模型权限、推理网关、Agent Workflow、RAG Pipeline。

过去平台工程解决的是如何更稳定交付应用；未来平台工程会进一步变成：

> 如何更高效、更安全、更低成本地交付 AI 能力。

## 一图结构

| 阶段 | 核心变化 | 代表技术 |
|---|---|---|
| 手工运维 | 系统依赖人 | SSH、scp、vim、restart |
| 脚本化 | 自动化重复动作 | Shell、Python、cron |
| 配置管理 | 机器状态可描述 | Puppet、Chef、SaltStack、Ansible |
| IaC | 基础设施进入 Git | Terraform、OpenTofu、Pulumi |
| CI/CD | 交付流程代码化 | Jenkins、GitHub Actions、GitLab CI |
| GitOps | Git 成为事实来源 | ArgoCD、FluxCD |
| Platform Engineering | 复杂度产品化 | IDP、Golden Path、Backstage、Service Catalog |
| AI Native Platform | AI 能力平台化 | GPU Scheduler、AI Gateway、Agent Runtime、Inference Fabric |

## 一句话总结

这二十年的基础设施演进，本质上一直围绕同一个核心问题：

```text
如何把越来越复杂的系统
从依赖人
逐渐变成依赖平台
```

到了 AI Native 时代，这个平台还要开始管理模型、记忆、工具、推理成本和长期运行的 Agent。

## 封面图提示词

低信息密度封面图，主题为“从人操作系统到平台交付能力”。画面从左到右四段：Manual Ops、IaC / GitOps、Platform Engineering、AI Native Platform。每段只放一个大图标和一句关键词，不放工具清单。右侧用柔和光线表现 AI Gateway 和 Agent Runtime 接入平台。适合书籍章节封面。

## 延伸阅读

- 书籍第 6 章：[从手工管理到现代平台工程](../../06-devops-to-platform-engineering.md)
- 书籍第 7 章：[平台工程核心能力](../../07-platform-engineering-core.md)
- [技术复杂度的背后，其实是一场控制权战争](../essays/control-war.md)
