# 第 14 章：构建平台工程最小闭环

## 本章概述

本章介绍如何构建一个平台工程的最小可行产品(MVP)，涵盖服务目录、应用模板、CI/CD、GitOps、权限审计等核心能力。

## 14.1 最小闭环架构

### 核心组件

```
┌─────────────────────────────────────────────────────────┐
│              平台工程最小闭环架构                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Developer Portal (Backstage)        │  │
│  │   服务目录 │ 模板中心 │ 文档                      │  │
│  └──────────────────────┬───────────────────────────┘  │
│                         │                                │
│  ┌──────────────────────┼───────────────────────────┐  │
│  │              API Gateway                          │  │
│  │   审批 │ 权限 │ 配额 │ 审计                        │  │
│  └──────────────────────┬───────────────────────────┘  │
│                         │                                │
│  ┌──────────────────────┼───────────────────────────┐  │
│  │              执行层 (GitOps)                       │  │
│  │   ArgoCD │ Terraform │ GitHub Actions            │  │
│  └──────────────────────┬───────────────────────────┘  │
│                         │                                │
│  ┌──────────────────────┴───────────────────────────┐  │
│  │              Kubernetes Cluster                   │  │
│  │   Dev │ Test │ Staging │ Prod                     │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 14.2 服务目录设计

### Backstage 部署

```bash
# 安装 Backstage
npx @backstage/create-app@latest

# 添加插件
yarn add @backstage/plugin-catalog
yarn add @backstage/plugin-github-actions
yarn add @backstage/plugin-logs
```

### 组件注册

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-service
  annotations:
    github.com/project-slug: myorg/my-service
spec:
  type: service
  lifecycle: production
  owner: platform-team
  system: payment-system
```

## 14.3 应用模板

### 创建模板

```yaml
apiVersion: backstage.io/v1alpha1
kind: Template
metadata:
  name: spring-boot-service
  title: Spring Boot Service
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
    - id: fetch-skeleton
      action: fetch:template
      name: Fetch Skeleton
      input:
        url: https://github.com/owner/skeleton-spring-boot
        values:
          serviceName: ${{ parameters.serviceName }}
    - id: publish
      action: catalog:register
      name: Register
```

## 14.4 CI/CD 流水线

### GitHub Actions 示例

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          
      - name: Build
        run: mvn clean package
        
      - name: Test
        run: mvn test
        
      - name: Build Docker Image
        run: |
          docker build -t my-service:${{ github.sha }} .
          
      - name: Deploy to Dev
        run: |
          kubectl apply -f k8s/development/
```

## 14.5 GitOps 配置

### ArgoCD 应用

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-service
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/manifests.git
    targetRevision: main
    path: my-service/overlays/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: development
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## 14.6 权限与审计

### RBAC 配置

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: development
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps"]
  verbs: ["get", "list", "watch", "create", "update", "patch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch"]
```

### 审计日志收集

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: RequestResponse
  resources:
  - group: ""
    resources: ["pods", "services"]
  - group: "apps"
    resources: ["deployments"]
```

## 学习目标

- [ ] 能部署 Backstage 门户
- [ ] 创建应用模板
- [ ] 配置 CI/CD 流水线
- [ ] 实现 GitOps 部署
- [ ] 配置权限和审计

## 延伸阅读

- [Backstage Documentation](https://backstage.io/docs/)
- [ArgoCD Getting Started](https://argo-cd.readthedocs.io/)
