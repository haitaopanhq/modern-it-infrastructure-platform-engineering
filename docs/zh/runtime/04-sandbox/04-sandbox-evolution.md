# 04-04: 一图看懂沙箱隔离演进

## 核心观点

沙箱不是某一种单独技术，而是一组不断变化的隔离边界。从浏览器 iframe 到 Chrome 多进程，从 Linux namespace 到 seccomp，从容器到微虚拟机，再到 WebAssembly 和机密计算，沙箱的目标始终是同一个：允许不完全可信的代码运行，同时限制它能访问的资源、系统调用、网络和数据。

理解沙箱演进，关键不是记住技术名，而是看隔离边界从哪里建立、信任谁、牺牲什么。越靠近硬件，隔离通常越强，开销也更大；越靠近应用，性能和体验越好，但需要更细的策略和更高的实现质量。

## 图表结构

```text
应用级隔离
  iframe / CSP / Permission Policy
      |
      v
进程级隔离
  Chrome Site Isolation / OS Process / UID
      |
      v
内核策略隔离
  namespace / cgroups / capabilities / seccomp / AppArmor / SELinux
      |
      v
运行时隔离
  gVisor / WASM Runtime / language sandbox
      |
      v
虚拟化隔离
  Kata / Firecracker / Cloud Hypervisor
      |
      v
硬件与加密隔离
  TEE / SEV / TDX / Nitro Enclaves
```

这张图展示的是隔离层级而不是替代顺序。真实系统通常组合多层沙箱：浏览器用进程和站点隔离，容器用内核策略和 runtime，Serverless 用微虚拟机，敏感数据处理再叠加机密计算。

## 演进脉络

最早的沙箱来自应用内部。浏览器需要执行网页脚本，却不能让网页随意读取本地文件和其他站点数据，于是同源策略、iframe、CSP 和权限模型逐步形成。

第二阶段进入操作系统层。多用户系统依赖进程、用户、权限和文件系统隔离；Linux namespace 与 cgroups 出现后，容器把这些内核能力组合成轻量运行环境。

第三阶段是容器安全强化。seccomp 限制系统调用，AppArmor 和 SELinux 限制访问路径，capabilities 拆分 root 权限，镜像签名和扫描进入供应链环节。

第四阶段是多租户和 Serverless 需求推动更强隔离。gVisor、Kata、Firecracker、WASM runtime 和机密计算把隔离边界继续前移或下沉，使平台能够运行更多不可信代码。

## 关键技术栈

| 层级 | 技术 | 主要防御目标 |
|------|------|--------------|
| 浏览器 | Same-Origin Policy, CSP, Site Isolation | 跨站访问、脚本越权 |
| Linux 内核 | namespace, cgroups, capabilities | 资源视图、资源用量、权限拆分 |
| 系统调用 | seccomp-bpf | 限制高风险 syscall |
| 强制访问控制 | AppArmor, SELinux | 限制文件、网络和进程访问 |
| 安全容器 | gVisor, Kata, Firecracker | 降低共享内核风险 |
| WASM | Wasmtime, WasmEdge, WASI | 轻量插件和边缘执行隔离 |
| 机密计算 | AMD SEV, Intel TDX, Nitro Enclaves | 保护运行中数据免受宿主侧窥探 |

沙箱工程的难点在组合。单独打开 seccomp 不等于安全，单独使用 VM 也不等于可运营；策略、可观测性、补丁、镜像供应链和默认权限必须一起设计。

## 误区与现实

误区一是认为容器就是沙箱。现实是容器是一组 Linux 隔离能力的打包方式，默认共享宿主机内核，不能直接等同于强安全边界。

误区二是认为沙箱越多越安全。现实是层数增加会带来调试难度、性能损耗和兼容性问题。如果边界不清晰，叠加技术反而会制造盲区。

误区三是认为 WASM 可以替代所有容器。WASM 在插件、边缘计算和轻量函数场景很有吸引力，但系统调用、语言生态、状态管理、调试和传统服务兼容仍需谨慎评估。

## 最佳实践

按信任等级设计沙箱。可信内部服务、第三方插件、客户上传代码、模型推理任务、CI 任务不应使用同一隔离策略。

默认最小权限。关闭特权容器，限制 hostPath，减少 Linux capabilities，启用 seccomp profile 和只读文件系统，敏感 namespace 不共享。

把策略变成默认模板，而不是依赖人工记忆。平台可以提供标准 Pod Security、NetworkPolicy、seccomp profile、镜像签名和只读根文件系统模板，让团队从安全基线开始申请例外。例外必须有过期时间、负责人和审计记录，否则沙箱策略会在长期运行中被逐步掏空。

把沙箱纳入观测。需要记录 syscall 拒绝、策略命中、容器逃逸告警、异常网络连接、镜像漏洞和 runtime 事件，否则安全策略会变成黑盒。

持续更新隔离层。沙箱依赖内核、VMM、runtime 和浏览器实现，补丁策略必须跟上。越是安全边界，越不能长期停留在旧版本。

最后要把沙箱失败场景写进应急预案。策略误杀、运行时崩溃、逃逸漏洞公告和镜像供应链事件，都需要对应的降级、隔离和恢复步骤。

## 与长文互链

本篇是第 04 子系列的隔离技术总览，长文入口见[容器运行时长文目录](../longform/README.md)。可向前阅读[04-03 gVisor/Kata](../03-gvisor-kata/03-gvisor-kata.md)理解安全容器两条路线，向后阅读[04-05 Runtime 与 Kubernetes 的关系](../05-runtime-k8s/05-runtime-k8s.md)理解这些隔离能力如何被集群调度。

## 关键词

沙箱, namespace, cgroups, seccomp, AppArmor, SELinux, WASM, Firecracker, gVisor, Kata, 机密计算
