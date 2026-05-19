# 一图读懂 存储服务

> **演进主线**：RAID → SAN/NAS → LVM → Ceph/S3 → CSI → NVMe-oF → GPUDirect Storage

## 核心观点

**AI 时代最贵的，不是 GPU，而是 GPU 等 IO。**

很多人以为：存储 = 硬盘。买块 SSD、上个 NAS、挂个云盘就够了。但 AI 时代之后，存储第一次从"配角"变成基础设施核心竞争层。真正的问题已经不是"数据能不能存下来"，而是：GPU 能不能高速读取、训练能不能并行加载、Checkpoint 能不能快速保存。

几十张 GPU 同时训练时会疯狂读取 TB 级数据。如果存储吞吐跟不上，再贵的 GPU 也会"空转"。

## 演进路径

| 时代 | 核心 | 代表技术 |
|------|------|----------|
| 本地磁盘 | 单机 IOPS | HDD、RAID、ext4、XFS |
| SAN/NAS 时代 | 存储网络化 | FC、iSCSI、NFS、存储阵列 |
| Volume 抽象 | 逻辑卷管理 | LVM、Thin Provision、Snapshot |
| 分布式存储 | 统一存储池 | Ceph、GlusterFS、HDFS |
| 云原生存储 | CSI 标准化 | Rook、Longhorn、OpenEBS |
| AI Storage | 高吞吐数据流 | NVMe-oF、GPUDirect Storage |

## 冲突认知

传统世界拼 IOPS（数据库随机读写），AI 世界拼吞吐（TB/s 数据流）。过去大家拼 CPU，后来拼 GPU，而未来真正决定系统上限的，是数据能否以更低延迟、更高吞吐流向 GPU。

## 信息图 Prompt

```
《一图读懂存储服务》

风格：NetApp / Ceph / Dell EMC 官方架构图风格
时间演进轴：本地磁盘 → SAN/NAS → LVM → 分布式存储 → 云原生 → AI Storage
右侧重点：
- 传统世界：拼 IOPS、数据库存储
- AI 世界：拼吞吐、TB/s 数据流、GPU Feeding
底部金句：
"AI 时代最贵的不是 GPU，而是 GPU 等 IO。"
```

## 延伸阅读

- 书籍第 4 章：[存储系统](../../04-storage-systems.md)
- [一图看懂 存储虚拟化演进](../virtualization/storage-virtualization.md)
