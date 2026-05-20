# 第 9 章：AI Agent 与平台工程融合

## 本章概述

本章介绍 AI Agent 如何与平台工程融合，包括 Agent 调用平台能力、人机协同、安全隔离、以及从 ChatOps 到 AgentOps 的演进。

## 9.1 AI Agent 如何接入平台能力

### Agent 与平台的交互模式

```
┌─────────────────────────────────────────────────────────┐
│              AI Agent 平台交互架构                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │                  AI Agent                        │   │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐        │   │
│   │  │  LLM    │  │  Plan   │  │  Tool   │        │   │
│   │  │  Core   │  │  Executor│ │  Caller │        │   │
│   │  └─────────┘  └─────────┘  └─────────┘        │   │
│   └──────────────────────┬──────────────────────────┘   │
│                          │                               │
│                          ↓                               │
│   ┌─────────────────────────────────────────────────┐   │
│   │            Platform Integration Layer           │   │
│   │   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │   │
│   │   │K8s API │ │ GitHub │ │Terraform│ │Pager   │  │   │
│   │   │        │ │  API   │ │  API   │ │Duty    │  │   │
│   │   └────────┘ └────────┘ └────────┘ └────────┘  │   │
│   └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 工具封装

Agent 通过调用封装好的工具来使用平台能力：

```yaml
# k8s-tool.yaml
name: kubectl_tool
description: "Kubernetes 集群管理工具"

capabilities:
  - list_pods
  - get_logs
  - scale_deployment
  - restart_pod

parameters:
  cluster:
    type: string
    required: true
  namespace:
    type: string
    default: default
    
execution:
  type: http
  endpoint: "{{ .Values.k8s_api }}/apis/batch/v1/namespaces/{namespace}/jobs"
  auth: 
    type: bearer_token
```

## 9.2 Agent 执行任务流程

### 任务执行流程

```
1. 用户输入
   ↓
2. 意图识别 (Intent Recognition)
   - 解析用户请求
   - 提取关键信息
   ↓
3. 任务规划 (Task Planning)
   - 分解为子任务
   - 确定执行顺序
   ↓
4. 工具选择 (Tool Selection)
   - 匹配可用工具
   - 检查权限
   ↓
5. 执行 (Execution)
   - 调用工具
   - 处理结果
   ↓
6. 反馈 (Feedback)
   - 返回结果
   - 确认状态
```

### 示例：部署新服务

```
用户: "帮我部署一个新的 API 服务，名称是 user-api"

Agent 思考:
1. 理解意图：需要部署新服务
2. 检查权限：用户有部署权限
3. 规划步骤：
   a. 创建 Kubernetes Deployment
   b. 创建 Service
   c. 配置 Ingress
   d. 检查部署状态
4. 执行：
   a. 调用 k8s-tool.create-deployment
   b. 调用 k8s-tool.create-service
   c. 调用 k8s-tool.create-ingress
   d. 调用 k8s-tool.wait-for-deployment
5. 返回结果
```

## 9.3 人机协同与审批机制

### 审批工作流

```
┌─────────────────────────────────────────────────────────┐
│                  Agent 审批工作流                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Agent Action → 风险评估 → 审批决策 → 执行 → 通知       │
│       │              │            │         │    │      │
│       ▼              ▼            ▼         ▼    ▼      │
│   操作生成      规则引擎      人工审批    API    消息   │
│                  (AI判断)    (可选)      调用   推送   │
│                                                         │
│  风险等级:                                               │
│  • 低风险 → 直接执行                                     │
│  • 中风险 → 审批后执行                                   │
│  • 高风险 → 人工确认 + 审批                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 审批规则示例

```yaml
# approval-rules.yaml
rules:
  - name: production-deploy
    condition: 
      environment: production
      action: deploy
    require_approval: true
    approvers:
      - role: sre-lead
      - role: tech-lead
      
  - name: resource-create
    condition:
      action: create
      resource_type: persistentvolume
    require_approval: true
    thresholds:
      storage: 100Gi
      cpu: "4"
      memory: 8Gi
      
  - name: read-only
    condition:
      action: read
    require_approval: false
```

### 人机协同模式

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| Agent 主导 | Agent 执行，人工监督 | 常规操作 |
| 人工主导 | 人工执行，Agent 辅助 | 复杂问题 |
| 并行协作 | 同时参与，职责分离 | 重要变更 |
| 审批模式 | Agent 提议，人工审批 | 生产变更 |

## 9.4 Agent 运行时安全隔离

### 安全边界设计

```
┌─────────────────────────────────────────────────────────┐
│                 Agent 安全边界                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │               外部边界 (Network)                  │   │
│  │   • 网络策略隔离                                   │   │
│  │   • API 认证授权                                   │   │
│  │   • 入口过滤                                       │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │               运行时边界 (Runtime)                │   │
│  │   • 工具白名单                                     │   │
│  │   • 命令限制                                       │   │
│  │   • 资源配额                                       │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │               数据边界 (Data)                     │   │
│  │   • 敏感数据脱敏                                   │   │
│  │   • 审计日志                                       │   │
│  │   • 访问控制                                       │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 工具执行限制

```yaml
# tool-security.yaml
security:
  allowed_commands:
    # Kubernetes 操作
    - kubectl get
    - kubectl describe
    - kubectl logs
    - kubectl apply (限制)
    
  denied_commands:
    - kubectl delete
    - kubectl exec
    - kubectl run
    
  execution:
    timeout: 300s
    max_retries: 2
    require_confirmation: true
    
  sensitive_data:
    mask_patterns:
      - password
      - token
      - secret
      - key
```

### 审计日志

```json
{
  "timestamp": "2026-05-11T10:00:00Z",
  "agent_id": "agent-001",
  "user_id": "alice@company.com",
  "action": "execute_tool",
  "tool": "kubectl_tool",
  "parameters": {
    "command": "kubectl get pods -n default",
    "cluster": "prod-cluster"
  },
  "result": "success",
  "duration_ms": 150,
  "risk_level": "low"
}
```

## 9.5 从 ChatOps 到 AgentOps

### ChatOps

- **特点**：通过聊天界面触发操作
- **交互**：人工输入命令，Agent 执行
- **局限**：需要人工持续参与

### AgentOps

- **特点**：Agent 自主决策和执行
- **交互**：人工设定目标，Agent 自动完成
- **优势**：7x24 小时无人值守

### 演进对比

| 维度 | ChatOps | AgentOps |
|------|---------|----------|
| 触发方式 | 手动 | 自动/手动 |
| 执行模式 | 同步 | 异步 |
| 决策 | 人工 | AI + 人工 |
| 监控 | 实时 | 异步 |
| 响应时间 | 秒级 | 分钟级 |

### AgentOps 架构

```
┌─────────────────────────────────────────────────────────┐
│                   AgentOps 架构                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   目标设定 ──→ Agent 规划 ──→ 自动执行 ──→ 结果验证   │
│       │            │            │            │         │
│       ▼            ▼            ▼            ▼         │
│   人工定义      AI 分解      API 调用      自动检查    │
│   SLO/SLA     执行计划      工具执行      异常告警    │
│                                                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │              持续反馈循环                         │   │
│   │   执行结果 → 效果评估 → 策略调整 → 优化执行     │   │
│   └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 9.6 智能化运维闭环

### 运维闭环

```
┌─────────────────────────────────────────────────────────┐
│                  智能运维闭环                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐           │
│   │  监控   │───→│  分析   │───→│  决策   │           │
│   │  采集   │    │  AI诊断 │    │  Agent  │           │
│   └─────────┘    └─────────┘    └────┬────┘           │
│                                       │                │
│                                       ▼                │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐           │
│   │  验证   │←───│  执行   │←───│  审批   │           │
│   │  确认   │    │  自动   │    │  人工   │           │
│   └─────────┘    └─────────┘    └─────────┘           │
│       │                                       │        │
│       └───────────────────────────────────────┘        │
│                       ↓                                 │
│              持续优化 / 学习                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 智能运维场景

| 场景 | 传统方式 | AgentOps 方式 |
|------|----------|---------------|
| 异常检测 | 阈值告警 | AI 预测 + 根因分析 |
| 故障响应 | 人工排查 | Agent 自动定位 |
| 变更管理 | 审批流程 | 智能审批 + 自动执行 |
| 容量规划 | 人工评估 | AI 预测 + 自动扩容 |
| 性能优化 | 专家调优 | Agent 自动调优 |

## 学习目标

- [ ] 理解 Agent 与平台能力的集成方式
- [ ] 掌握人机协同和审批机制设计
- [ ] 理解 Agent 运行时安全隔离
- [ ] 能构建基础的 AgentOps 能力

## 延伸阅读

- [LLM Agent Survey](https://arxiv.org/abs/2309.07864)
- [AgentOps Best Practices](https://www.anyscale.com/blog)
- [Platform Engineering + AI](https://platformengineering.org/ai)
