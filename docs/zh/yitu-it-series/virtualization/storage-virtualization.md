# 一图看懂 存储虚拟化演进

> **演进主线**：RAID → SAN/NAS → LVM → 分布式存储 → 云原生 → AI Storage

## 核心观点

**从 RAID 到 Ceph，数据如何被抽象成统一存储池。**

存储虚拟化不是"虚拟硬盘"，而是把离散物理磁盘抽象成统一存储资源池的过程。AI 时代之后，存储再次成为核心竞争力——因为 GPU 等待 IO 是最昂贵的浪费。

## 演进路径

| 时代 | 特点 | 代表技术 |
|------|------|----------|
| 本地磁盘 | 单机可靠 | HDD、RAID、ext4 |
| SAN/NAS | 存储网络化 | FC、iSCSI、NFS |
| LVM 抽象 | 逻辑卷管理 | LVM、Thin Provision |
| 分布式存储 | 统一存储池 | Ceph、GlusterFS、HDFS |
| 云原生 | CSI 标准化 | Rook、Longhorn |
| AI Storage | 高吞吐数据流 | NVMe-oF、GPUDirect Storage |

## 信息图 Prompt

```
《存储虚拟化演进》

风格：NetApp / Ceph 官方架构图风格
时间轴：RAID → SAN → LVM → Ceph → CSI → AI Storage
底部金句：
"AI 时代最贵的不是 GPU，而是 GPU 等 IO。"
```

## 延伸阅读

- [一图读懂 存储服务](../data/storage-overview.md)
- 书籍第 4 章：[存储系统](../../04-storage-systems.md)
