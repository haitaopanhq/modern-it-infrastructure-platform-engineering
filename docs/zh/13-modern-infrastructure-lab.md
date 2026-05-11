# 第 13 章：构建现代化基础设施学习实验室

## 本章概述

本章提供构建现代化基础设施学习实验室的完整指南，涵盖 Kubernetes 集群、网络、存储、可观测性等组件的部署和配置。

## 13.1 实验室架构

### 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                学习实验室架构                            │
├─────────────────────────────────────────────────────────┤
│   ┌─────────────────────────────────────────────────┐   │
│   │                 本地/云端                         │   │
│   │  ┌────────┐  ┌────────┐  ┌────────┐            │   │
│   │  │ Master │  │ Node 1 │  │ Node 2 │            │   │
│   │  │  3 台   │  │ Worker │  │ Worker │            │   │
│   │  └────────┘  └────────┘  └────────┘            │   │
│   │  ┌────────────────────────────────────────┐    │   │
│   │  │           K8s Cluster                   │    │   │
│   │  │  • CNI (Calico/Cilium)                  │    │   │
│   │  │  • Ingress (Nginx/Traefik)              │    │   │
│   │  │  • Service Mesh (Istio)                 │    │   │
│   │  └────────────────────────────────────────┘    │   │
│   └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 硬件要求

| 角色 | CPU | 内存 | 磁盘 | 数量 |
|------|-----|------|------|------|
| Master | 4核 | 8GB | 100GB | 3 |
| Worker | 8核 | 16GB | 200GB | 2+ |

## 13.2 Kubernetes 集群部署

### 使用 kubeadm 部署

```bash
# 1. 安装容器运行时
apt-get update
apt-get install -y containerd
mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# 2. 安装 kubeadm, kubelet, kubectl
apt-get update
apt-get install -y apt-transport-https ca-certificates curl
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /etc/apt/keyrings/kubernetes-archive-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list
apt-get update
apt-get install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl

# 3. 初始化集群
kubeadm init --pod-network-cidr=10.244.0.0/16

# 4. 安装 CNI (Calico)
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# 5. 加入节点
kubeadm token list
kubeadm join <master-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

## 13.3 可观测性部署

### Prometheus + Grafana

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

## 13.4 GitOps 部署

### ArgoCD 安装

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.9.3/manifests/install.yaml
```

## 学习目标

- [ ] 能部署 Kubernetes 集群
- [ ] 掌握 CNI 和 Ingress 配置
- [ ] 部署可观测性组件
- [ ] 配置存储和数据库
- [ ] 实现 GitOps 部署

## 延伸阅读

- [Kubernetes Docs](https://kubernetes.io/docs/)
- [ArgoCD Docs](https://argo-cd.readthedocs.io/)
