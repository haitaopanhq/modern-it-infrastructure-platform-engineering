# 手工运维到现代平台工程的完整演进

> **演进主线**：手工运维 → 脚本化 → 配置管理 → IaC → CI/CD → GitOps → Platform Engineering → AI Native Platform

## 核心观点

**现代基础设施二十年的演进，本质上一直在回答一个问题：如何把越来越复杂的系统，从"依赖人"逐渐变成"依赖平台"。**

很多年轻工程师已经很难想象早期基础设施世界：上线靠 SSH 登录服务器，scp 上传文件，vim 改配置，手动 restart。系统不可审计、不可回滚、不可复现，所有东西依赖"老师傅经验"。

后来开始写脚本，但脚本只自动化"动作"，不理解"状态"。再后来 Puppet/Ansible 出现，机器状态第一次可描述。Terraform 到来，基础设施第一次进入 Git。

然后 CI/CD → GitOps → Platform Engineering，控制权不断从人迁移到平台。

## 演进路径

| 阶段 | 核心变化 | 代表技术 |
|------|----------|----------|
| 手工运维 | 依赖老师傅经验 | SSH、scp、vim |
| 脚本化 | 自动化重复动作 | Shell、Python、cron |
| 配置管理 | 状态可描述 | Puppet、SaltStack、Ansible |
| IaC | 基础设施进 Git | Terraform、Pulumi、OpenTofu |
| CI/CD | Pipeline as Code | Jenkins、GitHub Actions、GitLab CI |
| GitOps | 声明式持续收敛 | ArgoCD、FluxCD |
| Platform Engineering | 复杂度产品化 | IDP、Golden Path、Backstage |
| AI Native Platform | GPU/Agent 编排 | AI Gateway、Agent Runtime、Inference Fabric |

## 信息图 Prompt

```
《手工运维到现代平台工程的完整演进》

风格：蓝白科技时间轴，从左到右的演进路径
左侧：1990s 手工运维（SSH、scp、vim、restart）
中间：2000s DevOps 工具链（Ansible、Terraform、Jenkins）
右侧：2020s 平台工程（GitOps、IDP、Backstage）
未来：AI Native Platform
底部金句：
"系统从依赖人，逐渐变成依赖平台。"
```

## 延伸阅读

- 书籍第 6 章：[从手工管理到现代平台工程](../../06-devops-to-platform-engineering.md)
- 书籍第 7 章：[平台工程核心能力](../../07-platform-engineering-core.md)
- [技术复杂度的背后，其实是一场控制权战争](../essays/control-war.md)
