# 一图纵览账户与安全体系

<!-- yitu-r2-assets:start -->

## 相关文章配图

![小红书：账户与安全体系](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E5%B0%8F%E7%BA%A2%E4%B9%A6-%E8%B4%A6%E6%88%B7%E4%B8%8E%E5%AE%89%E5%85%A8%E4%BD%93%E7%B3%BB.png)

![账户与身份安全演进历史](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E8%B4%A6%E6%88%B7%E4%B8%8E%E8%BA%AB%E4%BB%BD%E5%AE%89%E5%85%A8-%E6%BC%94%E8%BF%9B%E5%8E%86%E5%8F%B2.png)

![账户安全体系概览](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E8%B4%A6%E6%88%B7%E5%AE%89%E5%85%A8%E4%BD%93%E7%B3%BB%E6%A6%82%E8%A7%88-%E5%B0%81%E9%9D%A2%E5%9B%BE%E7%89%87.png)

![一图解读账户与安全体系](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E4%B8%80%E5%9B%BE%E8%A7%A3%E8%AF%BB%E8%B4%A6%E6%88%B7%E4%B8%8E%E5%AE%89%E5%85%A8%E4%BD%93%E7%B3%BB.png)

![账户与安全演进史](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E7%B3%BB%E7%BB%9F%E5%A4%8D%E6%9D%82%E5%BA%A6/%E4%B8%80%E5%9B%BE%E6%A6%82%E8%A7%88%E8%B4%A6%E6%88%B7%E4%B8%8E%E5%AE%89%E5%85%A8%E6%BC%94%E8%BF%9B%E5%8F%B2.png)

<!-- yitu-r2-assets:end -->
> **演进主线**：网络边界 -> IAM / SSO -> Zero Trust -> Workload Identity -> Secret Lifecycle -> Software Supply Chain -> Agent Identity

## 核心观点

如果把过去二十年的企业安全真正串起来看，你会发现，整个安全体系其实一直在经历一次巨大的边界迁移。

过去安全相信“你在哪”。只要进入内网，只要通过 VPN，只要站在防火墙后面，系统就默认你更可信。

现代安全更关心“你是谁”。谁在访问，以什么身份访问，拿到的凭证是否可信，权限是否最小化，行为是否可审计，身份是否可撤销，才是 Zero Trust 真正的底层逻辑。

> 安全边界，已经从网络边界进入身份边界。

## 网络边界为什么失效

最早的企业安全，核心是网络边界。DMZ、ACL、堡垒机、边界防火墙、VPN、内外网隔离，构成了很长一段时间里的默认安全模型。

这个模型成立的前提是：人坐在办公室，服务跑在固定机房，系统边界可以被一条网络线划出来。

但云计算、移动办公、SaaS、多云、Kubernetes、CI/CD 和 AI Agent 出现之后，世界变了。员工不再固定坐在办公室，服务不再运行在固定机器，应用开始跨云漂移，流水线自动部署越来越频繁，大量工作负载甚至只存在几分钟。

过去“只要进入内网就默认可信”的模型，开始彻底崩塌。

现代安全最大的变化，不只是攻击越来越复杂，而是网络边界正在消失，身份边界正在崛起。

## 身份系统成为控制平面

IAM 开始成为现代企业真正的基础设施入口。

过去账号密码只是登录系统的方式，现在身份系统已经变成企业控制平面。Keycloak、ZITADEL、Dex、Okta、Auth0 这些系统真正解决的，已经不只是登录，而是 SSO、MFA、RBAC、OIDC、SAML、LDAP 联邦，以及跨系统身份治理。

现代企业真正危险的问题，不再是“有没有 VPN”，而是：

- 谁能登录
- 以什么角色登录
- 登录之后能访问什么资源
- 权限是否最小化
- 行为是否可审计

很多攻击本质上已经不是突破防火墙，而是盗取身份。一个拥有管理员权限的合法身份，往往比一万个外部扫描器更危险。

## 工作负载身份才是零信任核心

Zero Trust 真正改变的，不是某个产品，而是一种默认逻辑：任何访问都不再天然可信。

过去服务之间依赖 IP 信任，内网调用默认放行。现在，SPIFFE、SPIRE、mTLS、Service Mesh 开始要求 Service A 必须证明自己真的是 Service A，Service B 也必须被验证。

因为现代基础设施里，大量存在的“用户”已经不再是人，而是 Pod、Container、Service、Agent、CI/CD Runner、AI Workflow。

未来每一个工作负载，都需要拥有可验证、可轮换、可撤销的机器身份。

真正的零信任，从来不只是员工 MFA，而是整个基础设施里的所有东西都需要身份。

## 长期密钥是安全债

云资源身份正在重构传统 AK/SK 模式。

过去企业常见做法，是把云密钥写进 Secret、环境变量、CI/CD 配置甚至代码仓库。可长期凭证本质上就是安全债。任何长期存在的密钥，最终都会泄漏。

AWS IRSA、GCP Workload Identity、Azure Workload Identity 开始把访问云资源的方式从“保存密钥”改成“动态签发短期身份”。Pod 在需要访问对象存储、数据库或云 API 时，通过 OIDC 换取短期凭证，使用后自动过期。

CI/CD 身份体系也在变化。GitHub Actions OIDC、GitLab OIDC、Cosign Keyless 解决的是同一个问题：流水线不应该再保存永久云密钥。

正确链路应该是：

```text
代码提交 -> OIDC 认证 -> 云 IAM 签发临时凭证 -> Terraform / Helm 部署
```

整个行业正在从“保存秘密”，进入“动态签发身份”的时代。

## Secret 与供应链是部署前门禁

很多企业以为，把 Secret 放进 Kubernetes 就完成了安全治理。

真正完整的 Secret 生命周期包括创建、分发、使用、轮换、吊销和审计。Vault、KMS、External Secrets 解决的，从来不只是存密码，而是密钥生命周期治理。

另一边，软件供应链安全正在变成新的部署前门禁。过去系统能跑就上线，现在越来越多企业开始要求镜像必须扫描、制品必须签名、来源必须可追溯、部署必须经过准入策略验证。

Cosign、Trivy、SBOM、SLSA、Kyverno 进入主流体系，是因为未来真正危险的不只是黑客入侵，而是：

> 你运行的东西，到底是谁构建的、从哪里来的、是否被篡改、是否可信。

## 一图结构

| 安全域 | 解决的问题 | 代表技术 |
|---|---|---|
| 用户身份 | 谁能登录、以什么角色、能访问什么 | Keycloak、ZITADEL、Dex、Okta |
| 工作负载身份 | 服务之间不再靠 IP 信任 | SPIFFE、SPIRE、mTLS、Service Mesh |
| 云资源身份 | 长期 AK/SK 是安全债 | IRSA、GCP Workload Identity、Azure Workload Identity |
| CI/CD 身份 | 流水线不再保存永久密钥 | GitHub Actions OIDC、GitLab OIDC、Cosign Keyless |
| 密钥管理 | Secret 生命周期治理 | Vault、KMS、External Secrets |
| 供应链安全 | 上线前验证来源与制品 | Cosign、Trivy、SBOM、SLSA、Kyverno |
| Agent 身份 | AI 代表谁行动、能调用什么工具 | Agent Identity、Tool Policy、AI Gateway |

## 一句话总结

真正完整的现代身份安全，是一条从用户身份、工作负载身份、云资源身份、CI/CD 身份，到密钥、策略、审计、供应链和 Agent 身份的长链路系统。

它背后真正回答的问题只有一句：

> 谁访问，用什么身份，拿什么凭证，是否可验证，是否可撤销，是否可审计。

## 封面图提示词

低信息密度封面图，主题为“安全边界从网络迁移到身份”。画面中央是一条从左到右的边界迁移路径：Firewall / VPN / DMZ 逐渐淡出，IAM / OIDC / Workload Identity / Zero Trust 逐渐变亮。背景使用深蓝到白色的企业基础设施风格，不堆技术小字，只保留 4 个大节点：Network Boundary、Identity Boundary、Workload Identity、Agent Identity。整体像一本技术史书籍的章节封面，简洁、克制、图示为主。

## 延伸阅读

- 书籍第 2 章：[安全与合规](../../10-security-compliance.md)
- [身份安全与零信任模型](../deep-dive/identity-zero-trust.md)
