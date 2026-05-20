# 《图解现代化 IT 基础架构与平台工程》

[English](./README.en.md)

## 项目定位

这是一本围绕现代化 IT 基础架构、平台工程、可观测性与 AI Agent 工作流的开源图解书。

当前主线正在从“工具教程”升级为“技术史叙事”：用技术、商业、组织焦虑和系统复杂度的视角，解释基础设施如何从硬件、虚拟化、云控制面、Runtime、网络、数据、平台工程一路演进到 AI Infra 与 Agent 控制面。

## 目标读者

- 基础设施工程师
- DevOps / SRE 工程师
- 平台工程团队
- 技术架构师
- AI Agent 工程团队

## 在线阅读

- [GitHub Pages](https://haitaopanhq.github.io/modern-it-infrastructure-platform-engineering/)

## 新增能力

### 《IT 基础设施演进之路》合并电子书

仓库新增了一个专用 Make target，用来把序章、01-07 核心章节和第 10 章安全主线合并为一本 PDF 电子书：

- 序章：`docs/zh/00-it-infrastructure-evolution-road.md`
- 第 1 章：现代 IT 系统全景
- 第 2 章：网络与协议
- 第 3 章：数据库系统
- 第 4 章：存储系统
- 第 5 章：可观测性与监控
- 第 6 章：从手工管理到现代平台工程
- 第 7 章：平台工程核心能力
- 第 10 章：安全与合规，账户与身份安全演进史

这本合并版 PDF 聚焦“基础设施演进之路”主叙事：资源效率解释虚拟化、云平台、Kubernetes 和平台工程为什么出现；信任边界解释账户、身份、零信任和 AI Agent 权限为什么会成为下一代控制面。它适合独立阅读、对外分享和 GitHub Release 发布。

### 内容风格

01-07 章已经补充技术史叙事的章首、章节过渡和结尾收束：

- 章首从“本章介绍什么工具”改为“本章回答什么现实问题”
- 章节中保留协议、架构、表格和示例，但把配置片段降级为技术旁注
- 章尾统一回到主线：基础设施演进不是工具越来越多，而是抽象、控制权、数据面和治理机制不断重组
- 第 7 章与第 10 章互链，串起平台工程、身份边界、密钥治理、审计和软件供应链安全

## 示例

生成合并版 PDF 电子书：

```bash
make ebook-it-infra-evolution
```

或使用简短别名：

```bash
make ebook
```

输出文件：

```text
dist/it-infrastructure-evolution-road.pdf
```

生成全量 PDF / DOCX / HTML，并同时保留合并版电子书：

```bash
make package
```

检查 50 天《现代基础设施演进史》内容包完整性：

```bash
make check-content
```

查看当前构建源文件与电子书章节顺序：

```bash
make list
```

## 发布产物

GitHub Actions 会在 `main` 分支构建：

- 单篇 Markdown 对应的 PDF / DOCX / HTML
- `dist/modern-it-infrastructure-platform-engineering-*.tar.gz`
- `dist/it-infrastructure-evolution-road.pdf`

`it-infra-evolution-promo/` 是本地视频/宣传片工程目录，不进入仓库提交，也不会参与 Markdown 文档构建。

## 参与贡献

欢迎提交 Issue 和 Pull Request！

## 许可

MIT License
