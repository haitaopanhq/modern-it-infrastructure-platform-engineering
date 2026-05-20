# 一图看懂 存储虚拟化演进

<!-- yitu-r2-assets:start -->

## 相关文章配图

![存储虚拟化演进](https://assets.onwalk.net/%E8%87%AA%E5%AA%92%E4%BD%93/%E8%99%9A%E6%8B%9F%E5%8C%96/%E5%AD%98%E5%82%A8%E8%99%9A%E6%8B%9F%E5%8C%96%E6%BC%94%E8%BF%9B.png)

<!-- yitu-r2-assets:end -->
> **演进主线**：RAID → SAN/NAS → LVM → 分布式存储 → 云原生 → AI Storage

## 核心观点

**从 RAID 到 Ceph，数据如何被抽象成统一存储池。**

很多人以为存储只是“硬盘”。但如果真正回看过去二十年的基础设施演进，会发现现代存储的发展，本质上也是一场资源抽象史。

存储虚拟化不是“虚拟硬盘”，而是把离散物理磁盘抽象成统一存储资源池的过程。最早的本地磁盘时代，服务器直接挂载 HDD，依赖 RAID、ext4、XFS 管理数据。那个阶段，存储几乎完全绑定物理机器，扩容困难、迁移复杂、利用率低。后来 SAN/NAS、Fibre Channel、iSCSI、NFS 和存储阵列普及，存储第一次从单台服务器里抽离出来，变成机房里的集中式基础设施。

真正重要的变化，不只是容量变大，而是抽象层变厚。LVM、Thin Provision、Snapshot 把磁盘从“物理设备”变成“逻辑卷”；Ceph、GlusterFS、HDFS 又把离散磁盘抽象成统一存储池；云硬盘、对象存储、文件存储、归档存储和跨区域复制，则把存储进一步变成服务。到了云原生时代，CSI、Rook、Longhorn、OpenEBS 继续向上抽象，让存储开始与 Kubernetes 生命周期绑定。

AI 时代之后，存储再次成为核心竞争力。传统数据库时代拼的是 IOPS，AI Storage 开始拼吞吐、数据流和 GPU Feeding。NVMe-oF、GPUDirect Storage、Checkpoint 本质上都在解决同一个问题：GPU 不能等待 IO。

## 演进路径

| 时代 | 特点 | 代表技术 |
|------|------|----------|
| 本地磁盘 | 单机可靠 | HDD、RAID、ext4 |
| SAN/NAS | 存储网络化 | FC、iSCSI、NFS |
| LVM 抽象 | 逻辑卷管理 | LVM、Thin Provision |
| 分布式存储 | 统一存储池 | Ceph、GlusterFS、HDFS |
| 云原生 | CSI 标准化 | Rook、Longhorn |
| AI Storage | 高吞吐数据流 | NVMe-oF、GPUDirect Storage |

## 一句话收束

AI 时代，昂贵的不只是 GPU，还有计算等待 IO。

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
