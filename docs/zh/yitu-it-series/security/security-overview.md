# 一图读懂 IT 安全体系

> **演进主线**：网络边界 → 入侵检测 → IAM/SSO → 零信任 → 工作负载身份 → 软件供应链安全

## 核心观点

**安全边界已经从"网络边界"进入"身份边界"。**

过去企业安全的核心是：防火墙、VPN、内网隔离。那个时代相信"只要进了内网就默认可信"。但云计算、移动办公、SaaS、多云、K8s、AI Agent 出现后，系统不再运行在固定机房，员工不再固定坐在办公室。你根本无法再定义"哪里是内网"。

于是现代安全开始转向：不再信任网络位置，而是验证"身份"。

## 现代身份安全体系

```
用户身份(KC/ZITADEL)  工作负载身份(SPIFFE/SPIRE)  云资源身份(IRSA)
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  ▼
                     Envoy/Istio/Cilium
                     mTLS + Policy (每条链都验证)
                                  │
                     ┌────────────┴────────────┐
                     ▼                         ▼
                 Service A                   Service B
              (经过身份验证)               (经过身份验证)
```

## 六大安全域

| 安全域 | 解决的问题 | 代表技术 |
|--------|-----------|----------|
| 用户身份 | 谁能登录、以什么角色、能访问什么 | Keycloak、ZITADEL、Dex |
| 工作负载身份 | 服务之间不再靠 IP 信任 | SPIFFE/SPIRE、mTLS |
| 云资源身份 | 长期 AK/SK 是安全债 | IRSA、Workload Identity |
| CI/CD 身份 | 流水线不再保存永久密钥 | GitHub OIDC、Cosign Keyless |
| 密钥管理 | 生命周期治理 | Vault、KMS、External Secrets |
| 供应链安全 | 上线前验证 | Cosign、Trivy、SBOM、SLSA |

## 金句

> **过去安全相信"你在哪"；现在安全更关心"你是谁"。**

## 延伸阅读

- 书籍第 10 章：[安全与合规](../../10-security-compliance.md)
- [身份安全与零信任模型](../deep-dive/identity-zero-trust.md)
- [2026-05-18 身份与安全总揽规划](../../yitu-it-series/security/identity-security-plan.md)
