# 第 11 章：故障排查与运行手册

## 本章概述

本章介绍 IT 系统的故障排查方法论和常见场景的运行手册，涵盖网络、数据库、存储、可观测性、CI/CD、以及 Agent 工作流的排查。

## 11.1 故障排查方法论

### 排查流程

```
┌─────────────────────────────────────────────────────────┐
│                  故障排查流程                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   1. 收集信息                                           │
│      ├── 告警内容                                       │
│      ├── 时间范围                                       │
│      ├── 影响的用户/系统                                │
│      └── 最近的变更                                     │
│                                                         │
│   2. 初步诊断                                           │
│      ├── 查看监控指标                                   │
│      ├── 查看日志                                       │
│      └── 检查依赖                                       │
│                                                         │
│   3. 根因分析                                           │
│      ├── 假设-验证                                      │
│      ├── 排除法                                         │
│      └── 溯源分析                                       │
│                                                         │
│   4. 实施修复                                           │
│      ├── 制定方案                                       │
│      ├── 备份/回滚准备                                  │
│      └── 执行修复                                       │
│                                                         │
│   5. 后续处理                                           │
│      ├── 验证修复                                       │
│      ├── 复盘总结                                       │
│      └── 完善文档                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 常用排查工具

| 类别 | 工具 | 用途 |
|------|------|------|
| 网络 | ping, traceroute, netstat, ss | 网络连通性 |
| 抓包 | tcpdump, wireshark | 包分析 |
| DNS | dig, nslookup, curl -v | DNS 解析 |
| K8s | kubectl debug, kubectl describe | 集群状态 |
| 应用 | jstack, py-spy, node --inspect | 进程分析 |
| 日志 | grep, awk, jq | 日志分析 |

## 11.2 网络故障排查

### 网络排查流程

```
问题描述 → 检查物理层 → 检查网络层 → 检查传输层 → 检查应用层
    │           │            │            │            │
    ▼           ▼            ▼            ▼            ▼
 症状收集   网卡状态      IP配置      端口状态     HTTP状态
```

### 常见网络问题

| 症状 | 可能原因 | 排查命令 |
|------|----------|----------|
| 无法访问 | DNS/路由/防火墙 | ping, curl, nslookup |
| 连接超时 | 网络阻塞/服务不可用 | telnet, netstat |
| 延迟高 | 网络拥塞/距离远 | traceroute, mtr |
| 丢包 | 链路问题/QoS | ping -c 100 |

### K8s 网络排查

```bash
# 检查 Pod 网络
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>

# 检查 Service
kubectl get svc -n <namespace>
kubectl endpoint slices -n <namespace>

# 检查网络策略
kubectl get networkpolicy -n <namespace>

# 进入 Pod 调试
kubectl debug -it <pod-name> -n <namespace> -- /bin/sh

# 检查 CNI 状态
kubectl get nodes -o wide
kubectl get pods -n kube-system | grep cni
```

## 11.3 数据库故障排查

### 数据库问题分类

| 类型 | 表现 | 排查方向 |
|------|------|----------|
| 连接 | 连接超时/拒绝 | 连接数、端口、网络 |
| 性能 | 查询慢 | 执行计划、索引 |
| 死锁 | 操作阻塞 | 锁等待、事务 |
| 数据 | 数据丢失/不一致 | 备份、复制状态 |

### MySQL 排查

```sql
-- 查看连接数
SHOW STATUS LIKE 'Threads_connected';

-- 查看慢查询
SHOW VARIABLES LIKE 'slow_query_log';
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;

-- 查看进程
SHOW PROCESSLIST;

-- 查看 InnoDB 状态
SHOW ENGINE INNODB STATUS;

-- 查看执行计划
EXPLAIN SELECT * FROM table WHERE ...
```

### PostgreSQL 排查

```sql
-- 查看连接
SELECT * FROM pg_stat_activity;

-- 查看慢查询
SELECT query, calls, mean_time 
FROM pg_stat_statements 
ORDER BY mean_time DESC LIMIT 10;

-- 查看锁
SELECT * FROM pg_locks;

-- 查看表大小
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_class
ORDER BY pg_total_relation_size(relid) DESC;
```

## 11.4 可观测性排查

### 指标异常排查

```
1. 确定异常指标
   - CPU 高 -> 进程分析
   - 内存高 -> 内存泄漏
   - 磁盘满 -> 清理日志
   - 网络抖 -> 网络分析

2. 关联分析
   - 与告警关联
   - 与变更关联
   - 与业务关联

3. 定位根因
   - 应用层面
   - 系统层面
   - 基础设施层面
```

### 日志排查

```bash
# Loki 查询示例
{app="api-gateway"} |= "error" | json | level="error"

# Elasticsearch 查询
GET /logs/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"service": "payment"}},
        {"range": {"@timestamp": {"gte": "now-1h"}}}
      ]
    }
  }
}
```

### 链路追踪排查

```
Span 关系:
HTTP GET /api/users
  ├─ SQL: SELECT * FROM users (50ms)
  ├─ HTTP GET /auth service (20ms)
  └─ Redis GET user:123 (5ms)

定位问题:
1. 找到慢 Span
2. 分析依赖调用
3. 确认瓶颈位置
```

## 11.5 CI/CD 与 GitOps 排查

### CI/CD 问题

| 问题类型 | 表现 | 排查点 |
|----------|------|--------|
| 构建失败 | 编译错误 | 代码、依赖、配置 |
| 测试失败 | 测试用例不过 | 测试代码、环境 |
| 部署失败 | 发布报错 | 镜像、权限、资源 |
| 镜像问题 | 拉取失败 | 仓库、网络、凭证 |

### ArgoCD 排查

```bash
# 查看应用状态
argocd app get my-app

# 查看应用事件
argocd app events my-app

# 查看资源状态
argocd app resources my-app

# 手动同步
argocd app sync my-app

# 查看 ArgoCD 日志
kubectl logs -n argocd deployment/argocd-server
```

## 11.6 Agent 工作流排查

### Agent 问题类型

| 类型 | 表现 | 排查方法 |
|------|------|----------|
| 理解错误 | 答非所问 | 检查 Prompt |
| 工具调用失败 | 操作未执行 | 检查工具配置 |
| 循环执行 | 无法终止 | 检查退出条件 |
| 响应慢 | 超时 | 检查 LLM 延迟 |

### 排查方法

```yaml
# 启用调试模式
agent:
  debug: true
  log_level: debug
  trace: true

# 检查工具调用日志
logs:
  level: debug
  include_tool_calls: true
  include_thoughts: true
  
# 验证工具配置
tools:
  - name: http_tool
    validate: true
    test_on_load: true
```

## 11.7 从 Checklist 到自动化 Runbook

### Runbook 模板

```yaml
# runbook-example.yaml
name: "Pod 重启处理"
severity: medium
frequency: high

triggers:
  - alert: "PodRestartHigh"
  - manual: true

steps:
  - id: collect_info
    title: 收集信息
    command: |
      kubectl get pods -n {{.namespace}}
      kubectl describe pod {{.pod_name}} -n {{.namespace}}
      kubectl logs {{.pod_name}} -n {{.namespace}} --previous
      
  - id: check_events
    title: 检查事件
    command: |
      kubectl get events -n {{.namespace}} --field-selector involvedObject.name={{.pod_name}}
      
  - id: analyze
    title: 分析原因
    options:
      - reason: "OOMKilled"
        next_step: check_memory_limits
      - reason: "Error"
        next_step: check_app_logs
      - reason: "Scheduled"
        next_step: check_node_resources
        
  - id: fix
    title: 修复
    command: |
      kubectl delete pod {{.pod_name}} -n {{.namespace}}
```

### 自动化 Runbook

```
┌─────────────────────────────────────────────────────────┐
│               自动化 Runbook 执行                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   告警触发 → 自动收集 → 根因判断 → 自动修复 → 通知     │
│     │          │           │           │          │     │
│     ▼          ▼           ▼           ▼          ▼     │
│   监控系统   脚本执行    规则匹配    API调用    消息   │
│                                                         │
│   自动化场景:                                           │
│   • Pod 自动重启                                        │
│   • 磁盘自动清理                                        │
│   • 自动扩容                                            │
│   • 流量切换                                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 学习目标

- [ ] 掌握故障排查方法论
- [ ] 能进行网络、数据库、存储排查
- [ ] 理解可观测性排查方法
- [ ] 能编写和使用 Runbook

## 延伸阅读

- [SRE Book](https://sre.google/sre-book/table-of-contents/)
- [Kubernetes Troubleshooting](https://kubernetes.io/docs/tasks/debug/)
- [Runbook Automation](https://runbook自动化.io/)
