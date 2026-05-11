# 第 7 章：平台工程核心能力

![平台工程图解](../zh/diagrams/06-07-platform-engineering.png)

## 本章概述

本章深入介绍平台工程的核心能力，包括自助服务平台、标准化模板、服务目录、环境交付、权限安全等内容。

## 7.1 自助服务平台

### 什么是自助服务

自助服务平台让开发者无需依赖运维团队即可完成：
- 资源申请（计算、存储、网络）
- 环境创建（开发、测试、预发布、生产）
- 应用部署（CI/CD、配置管理）
- 监控查看（指标、日志、告警）

### 平台架构

```
┌─────────────────────────────────────────────────────────┐
│                自助服务平台架构                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Developer Portal                     │  │
│  │   ┌──────────┐ ┌──────────┐ ┌──────────┐        │  │
│  │   │  服务目录 │ │  资源申请 │ │  部署中心 │        │  │
│  │   │          │ │          │ │          │        │  │
│  │   └──────────┘ └──────────┘ └──────────┘        │  │
│  └──────────────────────┬──────────────────────────┘  │
│                          │                               │
│  ┌──────────────────────┼──────────────────────────┐  │
│  │              Platform API                         │  │
│  │   ┌──────────┐ ┌──────────┐ ┌──────────┐        │  │
│  │   │  审批    │ │  配额    │ │  审计    │        │  │
│  │   │  工作流  │ │  管理    │ │  日志    │        │  │
│  │   └──────────┘ └──────────┘ └──────────┘        │  │
│  └──────────────────────┬──────────────────────────┘  │
│                          │                               │
│  ┌──────────────────────┼──────────────────────────┐  │
│  │              Backplane (底层平台)                 │  │
│  │   ┌──────────┐ ┌──────────┐ ┌──────────┐        │  │
│  │   │ Kubernetes│ │ Terraform │ │ GitLab   │        │  │
│  │   │          │ │          │ │          │        │  │
│  │   └──────────┘ └──────────┘ └──────────┘        │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Backstage 核心概念

| 概念 | 说明 |
|------|------|
| Catalog | 服务目录，注册所有组件 |
| Template | 应用模板，快速创建项目 |
| Plugins | 插件，扩展平台能力 |
| TechDocs | 技术文档，统一文档平台 |

## 7.2 标准化模板 (Golden Path)

### Golden Path 定义

> Golden Path 是经过验证的、最佳实践的应用开发和部署路径。

### 模板要素

```yaml
# app-template.yaml
apiVersion: backstage.io/v1alpha1
kind: Template
metadata:
  name: go-service
  title: Go Service Template
spec:
  owner: platform-team
  parameters:
    - name: serviceName
      title: Service Name
      type: string
    - name: description
      title: Description
      type: string
      
  steps:
    - id: fetch-template
      action: fetch:template
      name: Fetch Template
      input:
        url: https://github.com/org/go-service-scaffold
        values:
          serviceName: ${{ parameters.serviceName }}
          
    - id: publish
      action: catalog:register
      name: Register Service
      input:
        catalogInfoUrl: ${{ steps.fetch-template.output.catalogInfoUrl }}
```

### 模板类型

| 类型 | 用途 | 示例 |
|------|------|------|
| 应用模板 | 创建新服务 | Go/Java/Node.js 微服务 |
| 基础设施模板 | 创建基础设施 | K8s Namespace, Database |
| 流水线模板 | CI/CD 配置 | GitHub Actions, GitLab CI |

## 7.3 服务目录

### 服务目录内容

```
┌─────────────────────────────────────────────────────────┐
│                   服务目录内容                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 组件 (Components)                                   │
│     • 微服务                                            │
│     • 网站                                              │
│     • 库                                                │
│     • 函数                                              │
│                                                         │
│  2. 系统 (Systems)                                      │
│     • 组件集合                                          │
│     • 依赖关系                                          │
│     • API 定义                                          │
│                                                         │
│  3. 资源 (Resources)                                   │
│     • 数据库                                            │
│     • 消息队列                                          │
│     • 缓存                                              │
│     • 存储                                              │
│                                                         │
│  4. API                                                │
│     • REST API                                          │
│     • GraphQL                                           │
│     • gRPC                                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 服务注册

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  description: Payment processing service
  tags:
    - go
    - microservice
    - payments
spec:
  type: service
  lifecycle: production
  owner: payments-team
  providesApis:
    - payment-api
  dependsOn:
    - resource:postgres-payment
    - resource:redis-payment
```

## 7.4 环境交付

### 环境类型

| 环境 | 用途 | 特点 |
|------|------|------|
| Dev | 开发调试 | 频繁变更、快速反馈 |
| Test | 集成测试 | 自动化、可重复 |
| Staging | 预发布 | 与生产一致 |
| Prod | 生产 | 高可用、安全 |

### 环境创建流程

```
用户请求 ──→ 审批 ──→ 资源创建 ──→ 配置 ──→ 验证 ──→ 交付
   │           │           │         │        │        │
   ▼           ▼           ▼         ▼        ▼        ▼
 门户       工作流      Terraform   K8s/VM   测试    通知
```

### 多环境管理

```yaml
# values-dev.yaml
replicas: 1
resources:
  limits:
    cpu: 500m
    memory: 512Mi

# values-prod.yaml
replicas: 3
resources:
  limits:
    cpu: 2000m
    memory: 4Gi
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
```

## 7.5 权限、安全与审计

### 权限模型

```
┌─────────────────────────────────────────────────────────┐
│                  平台权限模型                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  角色 (Role)                                            │
│  ├── 平台管理员 (Platform Admin)                        │
│  │   └── 完全控制                                      │
│  ├── 开发者 (Developer)                                 │
│  │   ├── 读取服务目录                                   │
│  │   ├── 创建/更新应用                                  │
│  │   └── 部署到 Dev/Test                                │
│  ├── 运维 (SRE)                                         │
│  │   ├── 所有开发者权限                                 │
│  │   └── 部署到 Prod                                    │
│  └── 只读 (Viewer)                                      │
│       └── 只读权限                                      │
│                                                         │
│  权限粒度：                                              │
│  • 组件级 (Component)                                   │
│  • 环境级 (Environment)                                 │
│  • 资源级 (Resource)                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 安全实践

1. **网络安全**
   - NetworkPolicy 隔离
   - Service Mesh mTLS
   - 零信任网络

2. **密钥管理**
   - Vault 集中管理
   - 敏感信息加密
   - 密钥轮换

3. **审计日志**
   - 所有操作记录
   - 敏感操作告警
   - 合规报告

### 审计示例

```json
{
  "timestamp": "2026-05-11T10:00:00Z",
  "actor": "alice@company.com",
  "action": "deploy",
  "resource": "payment-service",
  "environment": "production",
  "result": "success",
  "changes": [
    {"kind": "deployment", "name": "payment-service", "replicas": "2 -> 3"}
  ]
}
```

## 7.6 开发者体验优化

### 开发者体验指标

| 指标 | 描述 | 目标 |
|------|------|------|
| MTTR | 平均恢复时间 | < 1小时 |
| 部署频率 | 部署次数/天 | > 10次 |
| 变更前置时间 | 代码到生产 | < 1天 |
| 首次修复率 | 首次修复比例 | > 70% |

### 改善措施

```
┌─────────────────────────────────────────────────────────┐
│                开发者体验改善措施                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 文档                                                │
│     • 快速入门指南                                       │
│     • API 文档                                          │
│     • 示例代码                                          │
│                                                         │
│  2. 工具                                                │
│     • 一键环境搭建                                       │
│     • 本地开发环境                                       │
│     • CLI 工具                                          │
│                                                         │
│  3. 支持                                                │
│     • Slack/钉钉支持频道                                │
│     • 每周办公时间                                       │
│     • 知识库                                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 学习目标

- [ ] 理解自助服务平台架构
- [ ] 掌握 Golden Path 模板设计
- [ ] 理解服务目录和资源管理
- [ ] 能构建基础的平台工程能力

## 延伸阅读

- [Backstage Documentation](https://backstage.io/docs/)
- [Platform Engineering Book](https://platformengineering.org/platform-engineering-book)
- [Internal Developer Platform](https://internaldeveloperplatform.org/)
