# 身份安全与零信任模型

> **安全边界从"网络"迁移到"身份"**

## 核心判断

**谁在访问、以什么身份、拿什么凭证、是否可验证、是否可撤销、是否可审计——这才是零信任真正的底层逻辑。**

## 演进路径

传统安全 → IAM 入口 → 工作负载身份 → 云资源身份 → CI/CD 身份 → 密钥管理 → 供应链安全

## 六大安全层

### 1. 用户身份

不再只是账号密码。Keycloak、ZITADEL、Dex 解决的是：SSO、MFA、RBAC、OIDC、SAML、LDAP 联邦。

真正的企业安全入口，不是 VPN，而是**谁能登录、以什么角色登录、能访问什么资源**。

### 2. 工作负载身份

SPIFFE/SPIRE、mTLS、Service Mesh。过去服务之间靠内网 IP 信任。现在必须变成：Service A 证明自己是 Service A，Service B 也必须被验证。

**每个 Pod、Service、Agent 都应该有可验证身份。**

### 3. 云资源身份

AWS IRSA、GCP Workload Identity、Azure Workload Identity。Pod 通过 OIDC 换取短期凭证，临时访问云资源。**长期密钥写进 Secret、环境变量、CI 变量，本质都是安全债。**

### 4. CI/CD 身份

GitHub Actions OIDC、GitLab OIDC、Cosign Keyless。流水线不应该保存永久云密钥。正确链路：代码提交 → OIDC 认证 → 云 IAM 颁发临时凭证 → Terraform/Helm 部署。

### 5. 密钥管理

Vault、KMS、External Secrets。真正的密钥生命周期：创建、分发、使用、轮换、吊销、审计。**没有轮换和审计的 Secret，只是换了个地方存密码。**

### 6. 软件供应链安全

Cosign、Trivy、SBOM、SLSA、Kyverno。镜像要扫描、制品要签名、来源要可追溯、部署要被准入策略验证。

## 架构图

```
用户身份(KC/ZITADEL)   工作负载身份(SPIFFE)   云资源身份(IRSA)
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                       Envoy/Istio/Cilium
                       mTLS + Policy
                              │
                     ┌────────┴────────┐
                     ▼                 ▼
                 Service A          Service B
```

## 延伸阅读

- [一图读懂 IT 安全体系](../security/security-overview.md)
- 书籍第 10 章：[安全与合规](../../10-security-compliance.md)
