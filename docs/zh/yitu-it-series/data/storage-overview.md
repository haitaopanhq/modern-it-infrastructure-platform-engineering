# 一图读懂存储服务

<!-- yitu-r2-assets:start -->

## 相关文章配图

![一图读懂存储系统](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E4%B8%80%E5%9B%BE%E8%AF%BB%E6%87%82%E5%AD%98%E5%82%A8%E7%B3%BB%E7%BB%9F.png)

![小红书：存储演进之路](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/IT%E7%B3%BB%E7%BB%9F%E6%BC%94%E5%8F%98%E5%8E%86%E5%8F%B2/%E5%B0%8F%E7%BA%A2%E4%B9%A6-%E5%AD%98%E5%82%A8%E6%BC%94%E8%BF%9B%E4%B9%8B%E8%B7%AF.png)

<!-- yitu-r2-assets:end -->
> **演进主线**：RAID -> SAN / NAS -> Block Storage -> Object Storage -> Data Lake -> AI File System -> GPU Data Path

## 核心观点

如果把过去二十年的基础设施演进真正串起来看，存储一直是最容易被低估、却又最核心的底层能力之一。

很多人以前总觉得，存储不过就是硬盘、NAS、云盘，能把数据放进去就够了。但 AI 时代之后，存储第一次从配角重新变成基础设施里的核心竞争层。

因为现代系统真正困难的问题，已经不再是“数据能不能存下来”，而是：

- GPU 能不能高速读取数据
- 训练能不能并行加载
- Checkpoint 能不能快速保存
- 向量数据库能不能低延迟查询
- 上百张 GPU 能不能同时吃到数据

很多企业后来才发现：GPU 利用率低，并不一定是 GPU 不够，而是 GPU 在等 IO。

AI 时代最昂贵的，不只是算力，还有等待。

## 从 IOPS 到吞吐

过去传统存储世界，长期围绕事务型 IO 展开。

那个时代的关键词是 RAID、SAN、NAS、数据库盘、云硬盘。企业真正拼的是 IOPS、随机读写、可靠性和高可用。因为数据库时代的数据模型，本质是大量小文件、小事务、高频随机访问。

于是 SSD、RAID Cache、SAN 网络、FC 存储阵列成为核心基础设施。

AI 时代之后，数据模式突然变化。训练集、视频、图片、Embedding、Checkpoint、向量索引开始指数级增长。现代 AI 系统更像是在处理数据洪水，而不是小文件事务。

于是过去强调 IOPS 的世界，开始转向吞吐世界。几十张 GPU 同时训练时，会持续顺序读取 TB 级数据。真正决定系统上限的，越来越不是单次随机 IO，而是持续的数据流能力。

## 块存储退回系统盘

整个存储体系开始重新分层。

块存储正在慢慢退回系统盘角色。Local NVMe SSD、EBS、Ceph RBD、Longhorn、Kubernetes CSI，本质越来越偏向系统缓存、高速临时数据、本地持久卷和运行时数据层。

原因很简单：AI 系统越来越强调本地高速数据路径。

它不是说块存储不重要，而是块存储不再承担“一套 SAN 打天下”的角色。它会继续存在，但更多服务于运行时、本地缓存和可控延迟。

## 对象存储成为 AI 默认底座

对象存储开始快速崛起。

S3、MinIO、Ceph RGW、OSS 本质上都在解决同一个问题：如何低成本存储海量非结构化数据。

今天的数据已经不只是文件，而是图片、视频、Checkpoint、Embedding、向量索引组成的大规模对象集合。AI Pipeline、RAG、训练平台、数据湖，最后几乎都会走向 Object Storage。

对象存储真正重要的地方，并不是“高级”，而是天然适合横向扩展：容量大、成本低、分布式友好、云原生友好。

## 文件系统重新进化

对象存储并不能直接解决 GPU 高速训练问题。

于是文件系统开始重新进化。传统 NFS 曾经是很多企业共享存储默认答案，但 AI 时代之后，高并发训练、海量小文件、GPU 并发加载开始让传统共享存储暴露瓶颈。

JuiceFS、Lustre、CephFS、Alluxio 开始崛起。它们真正解决的问题，其实只有一句话：

> 如何让 GPU 更快吃到数据。

很多现代 AI 基础设施正在形成新的数据路径：

```text
Object Storage
  -> Distributed File System
  -> NVMe / Local Cache
  -> RDMA / RoCE
  -> GPUDirect Storage
  -> GPU
```

未来真正昂贵的，并不是存储空间，而是 GPU 等待数据的时间。

## 数据流成为竞争核心

越来越多 AI Infra 公司开始投入 NVMe、Spine-Leaf 网络、RDMA、RoCEv2、GPUDirect Storage、Alluxio、分层缓存、冷热数据分离。

因为现代基础设施已经开始从计算竞争进入数据流竞争。过去大家拼 CPU，后来拼 GPU，未来真正决定系统上限的，很可能是数据能否以更低延迟、更高吞吐、更少阻塞流向 GPU。

很多人以为 AI 拼的是模型参数、训练框架和推理优化。但真正走到大规模阶段之后，最后拼的往往是底层基础设施。

基础设施里最容易被忽略的一层，就是存储。

因为没有高效数据流，再强的大模型，也只是堵车中的 GPU。

## 一图结构

| 阶段 | 核心变化 | 代表技术 |
|---|---|---|
| 本地磁盘 | 数据绑定单机 | HDD、SSD、RAID、ext4、XFS |
| SAN / NAS | 存储网络化 | FC、iSCSI、NFS、存储阵列 |
| 块存储 | 系统盘与持久卷 | EBS、Ceph RBD、Longhorn、CSI |
| 对象存储 | 海量非结构化数据 | S3、MinIO、Ceph RGW、OSS |
| 数据湖 | AI Pipeline 默认底座 | Object Storage、Lakehouse、Metadata |
| AI 文件系统 | 高并发训练访问 | JuiceFS、Lustre、CephFS、Alluxio |
| GPU 数据路径 | 数据直达算力 | NVMe、RDMA、RoCE、GPUDirect Storage |

## 封面图提示词

低信息密度封面图，主题为“存储从硬盘演进为 GPU 数据流”。画面只展示一条从左到右的数据流：Data Lake -> Distributed File System -> NVMe Cache -> RDMA Network -> GPU。背景有淡化的数据中心和 GPU 机柜，不堆协议小字，不放密集表格。标题视觉焦点是“AI Storage / GPU Feeding”，整体像技术史书籍封面。

## 延伸阅读

- 书籍第 4 章：[存储系统](../../04-storage-systems.md)
- [一图看懂 存储虚拟化演进](../virtualization/storage-virtualization.md)
