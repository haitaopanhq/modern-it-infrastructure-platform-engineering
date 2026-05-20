# 04. 重建信任

<!-- yitu-r2-assets:start -->

## 相关文章配图

![AD / LDAP / Kerberos 如何工作](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82-AD-LDAP-Kerberos-%E5%A6%82%E4%BD%95%E5%B7%A5%E4%BD%9C.png)

![IAM / OAuth / JWT](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E8%BA%AB%E4%BB%BD%E4%B8%8E%E5%AE%89%E5%85%A8/2026-05-21/02%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82-IAM-OAuth-JWT.png)

![现代系统为什么越来越像身份工厂](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E8%BA%AB%E4%BB%BD%E4%B8%8E%E5%AE%89%E5%85%A8/2026-05-21/04%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82%EF%BC%9A%E7%8E%B0%E4%BB%A3%E7%B3%BB%E7%BB%9F%E4%B8%BA%E4%BB%80%E4%B9%88%E8%B6%8A%E6%9D%A5%E8%B6%8A%E5%83%8F%E8%BA%AB%E4%BB%BD%E5%B7%A5%E5%8E%82.png)

![Token 正在变成新的攻击面](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E8%BA%AB%E4%BB%BD%E4%B8%8E%E5%AE%89%E5%85%A8/2026-05-21/03%E4%B8%80%E5%9B%BE%E7%9C%8B%E6%87%82-%E4%B8%BA%E4%BB%80%E4%B9%88%20Token%20%E6%AD%A3%E5%9C%A8%E5%8F%98%E6%88%90%E6%96%B0%E7%9A%84%E6%94%BB%E5%87%BB%E9%9D%A2.png)

<!-- yitu-r2-assets:end -->
本卷讲企业身份体系的出现：当系统、用户、服务和网络边界不断扩张，信任必须从“位置可信”迁移到“身份可信”。

| 顺序 | 标题 |
|---|---|
| 04-00 | 一图看懂账户与身份安全演进史 |
| 04-01 | 一图看懂：AD / LDAP / Kerberos 的出现 |

## 本卷主线

过去企业相信机房、内网、防火墙和管理员权限。互联网、云平台、API 化和远程办公把这些边界不断打穿之后，安全的核心问题不再是“外面的人能不能进来”，而是“谁正在用什么身份代表企业行动”。

从 DOS、Unix、Linux 的本地权限，到 AD、LDAP、Kerberos 的企业网络身份；从 Web 安全、防火墙、VPN，到 IAM、OAuth、Zero Trust，再到 AI Agent 与模型能力保护，账户与身份安全演进史本质上是信任边界不断迁移的历史。

本卷要把安全从产品清单重新写成基础设施史的一部分：资源效率让系统可以扩张，身份体系让系统扩张之后仍然可验证、可撤销、可审计。
