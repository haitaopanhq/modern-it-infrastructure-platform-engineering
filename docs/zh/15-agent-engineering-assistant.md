# 第 15 章：构建 Agent 驱动的工程助手

## 本章概述

本章介绍如何构建一个 Agent 驱动的工程助手，涵盖 Agent Runtime、工具调用、技能管理、任务执行、审批与回滚等能力。

## 15.1 Agent 运行时架构

### 核心组件

```
┌─────────────────────────────────────────────────────────┐
│              Agent 驱动工程助手架构                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │                  对话界面                          │  │
│  │   Web │ Slack │ Discord │ CLI                    │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Gateway (网关层)                     │  │
│  │   认证 │ 会话 │ 限流 │ 审计                        │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Agent Runtime                        │  │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐        │  │
│  │   │  规划   │  │  记忆   │  │  工具   │        │  │
│  │   │ Engine  │  │  Memory │  │  Hub    │        │  │
│  │   └─────────┘  └─────────┘  └─────────┘        │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │              工具层 (Tools)                        │  │
│  │   K8s │ GitHub │ Terraform │ DB │ Browser        │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 15.2 工具调用框架

### 工具定义

```yaml
tools:
  - name: kubectl_exec
    description: "Execute kubectl commands"
    type: exec
    allowed_commands:
      - kubectl get
      - kubectl describe
      - kubectl logs
    parameters:
      command:
        type: string
        required: true
      namespace:
        type: string
        default: default
    security:
      timeout: 60s
      require_approval: true
      
  - name: github_pr
    description: "Create GitHub Pull Request"
    type: http
    endpoint: "https://api.github.com/repos/{owner}/{repo}/pulls"
    method: POST
    auth: bearer_token
```

## 15.3 技能管理系统

### Skill 定义

```yaml
skill:
  name: kubernetes运维
  version: 1.0.0
  description: "Kubernetes 集群运维技能"
  
  triggers:
    - pattern: ".*(部署|扩缩容|查看).*Pod.*"
    - pattern: ".*(创建|删除).*Deployment.*"
    
  capabilities:
    - list_pods
    - scale_deployment
    - view_logs
    - restart_pod
    
  tools:
    - kubectl_exec
    - kubernetes_api
    
  permissions:
    - k8s:read
    - k8s:write:development
```

### 技能编排

```python
class SkillOrchestrator:
    def match_skill(self, user_input: str) -> List[Skill]:
        # 意图识别匹配技能
        matched = []
        for skill in self.skills:
            if self.matcher.match(user_input, skill.triggers):
                matched.append(skill)
        return matched
    
    def execute_skill(self, skill: Skill, context: Context) -> Result:
        # 执行技能
        pass
```

## 15.4 任务执行

### 执行流程

```
用户请求 → 意图解析 → 技能匹配 → 参数提取 → 工具调用 → 结果处理 → 响应

示例：
用户: "帮我重启 user-service 的 Pod"

意图: restart_pod
参数: service=user-service
执行: kubectl rollout restart deployment/user-service -n default
响应: 已触发重启，请稍候查看状态
```

### 任务状态管理

```python
class TaskManager:
    def create_task(self, user_id: str, intent: str, params: dict) -> Task:
        task = Task(
            id=uuid.uuid4(),
            user_id=user_id,
            intent=intent,
            params=params,
            status="pending"
        )
        self.db.save(task)
        return task
    
    def execute_task(self, task_id: str) -> TaskResult:
        task = self.db.get(task_id)
        task.status = "running"
        
        # 执行工具调用
        result = self.tool_executor.execute(task.intent, task.params)
        
        task.status = "completed"
        task.result = result
        return result
```

## 15.5 审批与回滚

### 审批工作流

```yaml
approval_workflow:
  rules:
    - name: production_deploy
      condition: 
        action: deploy
        environment: production
      require_approval: true
      approvers:
        - role: tech-lead
        
    - name: resource_create
      condition:
        action: create
        resource_type: pvc
      require_approval: false
      quota_check: true
      
  rollback:
    enabled: true
    auto_rollback_on_failure: true
    max_retry: 2
    snapshot_before_change: true
```

### 回滚机制

```python
class RollbackManager:
    def create_snapshot(self, resource: str) -> Snapshot:
        # 创建资源快照
        original = self.k8s.get(resource)
        snapshot = self.db.save_snapshot(original)
        return snapshot
    
    def rollback(self, snapshot_id: str) -> bool:
        snapshot = self.db.get_snapshot(snapshot_id)
        self.k8s.apply(snapshot.resource)
        return True
```

## 15.6 日志、指标、追踪

### 可观测性集成

```yaml
observability:
  metrics:
    - agent_requests_total
    - agent_request_duration_seconds
    - tool_execution_total
    - tool_execution_duration_seconds
    
  logs:
    level: info
    include_context: true
    sensitive_data_mask: true
    
  traces:
    enabled: true
    sample_rate: 0.1
    propagation: w3c
```

### 监控面板

```
Agent 监控指标:
- 请求成功率
- 平均响应时间
- 工具调用分布
- 技能使用频率
- 用户满意度
```

## 15.7 安全边界与权限控制

### 权限模型

```
┌─────────────────────────────────────────────────────────┐
│              Agent 权限控制                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  用户权限 → Agent 权限 → 工具权限                        │
│                                                         │
│  示例:                                                  │
│  用户Alice (developer) → Agent(limited) → kubectl(get) │
│  用户Bob (admin)       → Agent(full)    → kubectl(*)   │
│                                                         │
│  权限限制:                                              │
│  • 命令白名单                                           │
│  • 资源范围限制                                         │
│  • 环境隔离                                             │
│  • 敏感操作需要二次确认                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 安全配置

```yaml
security:
  # 命令限制
  allowed_commands:
    - kubectl get
    - kubectl describe
    - kubectl logs
    - kubectl apply
    
  denied_commands:
    - kubectl delete
    - kubectl exec
    - kubectl run
    
  # 资源限制
  resource_limits:
    cpu: "2"
    memory: "4Gi"
    
  # 审计
  audit:
    log_all: true
    log_failed: true
    retention_days: 90
```

## 15.8 最佳实践

### 开发规范

1. **技能设计**
   - 单一职责
   - 清晰触发条件
   - 完善的错误处理

2. **工具封装**
   - 幂等性
   - 超时控制
   - 清晰的日志

3. **安全**
   - 最小权限
   - 操作审计
   - 敏感数据保护

### 部署架构

```
生产环境高可用:
┌─────────────────────────────────────────┐
│           Load Balancer                 │
└──────────────────┬──────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌────────┐    ┌────────┐    ┌────────┐
│ Agent 1 │    │ Agent 2 │    │ Agent 3 │
│ Active │    │ Active │    │ Active │
└────────┘    └────────┘    └────────┘
    │              │              │
    └──────────────┼──────────────┘
                   │
         ┌────────┴────────┐
         │   Redis (Session)│
         └────────┬────────┘
                   │
         ┌────────┴────────┐
         │  PostgreSQL     │
         │  (持久化)       │
         └─────────────────┘
```

## 学习目标

- [ ] 理解 Agent 运行时架构
- [ ] 掌握工具调用框架
- [ ] 能设计技能管理系统
- [ ] 能实现审批与回滚
- [ ] 能构建安全的 Agent 系统

## 延伸阅读

- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [AutoGen Framework](https://microsoft.github.io/autogen/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
