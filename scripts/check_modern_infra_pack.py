#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "zh"
PLAN_DIR = DOCS / "content-planning" / "modern-infrastructure-evolution"
DIAGRAM_DIR = DOCS / "diagrams" / "modern-infrastructure-evolution"
PROMPT_DIR = DIAGRAM_DIR / "prompts"

REQUIRED_SECTIONS = [
    "## 核心观点",
    "## 图表结构",
    "## 演进脉络",
    "## 关键技术栈",
    "## 误区与现实",
    "## 最佳实践",
    "## 与长文互链",
    "## 关键词",
]

TOPIC_PATHS = [
    "foundation/01-linux-kernel/01-linux-never-left.md",
    "foundation/02-hardware/02-ai-back-to-baremetal.md",
    "foundation/03-numa/03-numa-modern-server.md",
    "foundation/04-cpu-gpu-dpu/04-cpu-gpu-dpu-evolution.md",
    "foundation/05-bios-k8s/05-bios-to-kubernetes.md",
    "virtualization/01-compute-virt/01-compute-virtualization-evolution.md",
    "virtualization/02-storage-virt/02-storage-virtualization-evolution.md",
    "virtualization/03-network-virt/03-network-virtualization-evolution.md",
    "virtualization/04-resource-pooling/04-resource-pooling.md",
    "virtualization/05-hypervisor/05-hypervisor-evolution.md",
    "cloud-platform/01-openstack/01-openstack-decline.md",
    "cloud-platform/02-k8s-unified/02-kubernetes-unified.md",
    "cloud-platform/03-cloud-control-plane/03-cloud-control-plane.md",
    "cloud-platform/04-cloud-agnostic/04-cloud-agnostic.md",
    "cloud-platform/05-multi-cloud/05-multi-cloud-challenges.md",
    "runtime/01-oci-runtime/01-oci-runtime.md",
    "runtime/02-containerd-docker/02-containerd-docker.md",
    "runtime/03-gvisor-kata/03-gvisor-kata.md",
    "runtime/04-sandbox/04-sandbox-evolution.md",
    "runtime/05-runtime-k8s/05-runtime-k8s.md",
    "network/01-c10k-ai-fabric/01-c10k-to-ai-fabric.md",
    "network/02-ebpf-network/02-ebpf-network-revolution.md",
    "network/03-api-gateway/03-api-gateway-evolution.md",
    "network/04-service-mesh/04-service-mesh-rise-fall.md",
    "network/05-rdma-nvlink-nccl/05-rdma-nvlink-nccl.md",
    "data/01-redis/01-redis-evolution.md",
    "data/02-kafka/02-kafka-evolution.md",
    "data/03-distributed-db/03-distributed-db-evolution.md",
    "data/04-cap/04-cap-theorem.md",
    "data/05-data-lakehouse/05-data-lakehouse.md",
    "platform/01-devops/01-devops-evolution.md",
    "platform/02-gitops/02-gitops.md",
    "platform/03-platform-engineering/03-platform-engineering.md",
    "platform/04-idp/04-idp-internal-developer-platform.md",
    "platform/05-control-plane-migration/05-control-plane-migration.md",
    "observability/01-monitoring-history/01-monitoring-evolution.md",
    "observability/02-opentelemetry/02-opentelemetry.md",
    "observability/03-ebpf-observability/03-ebpf-observability.md",
    "observability/04-finops/04-finops.md",
    "observability/05-iam-zero-trust/05-iam-zero-trust.md",
    "ai-infra/01-ai-runtime/01-ai-runtime.md",
    "ai-infra/02-vllm/02-vllm.md",
    "ai-infra/03-ray/03-ray.md",
    "ai-infra/04-gpu-scheduling/04-gpu-scheduling.md",
    "ai-infra/05-ai-gateway/05-ai-gateway.md",
    "agent/01-mcp-acp/01-mcp-acp.md",
    "agent/02-agent-runtime/02-agent-runtime.md",
    "agent/03-ai-gateway/03-ai-gateway.md",
    "agent/04-multi-agent/04-multi-agent.md",
    "agent/05-ai-tool-protocol/05-ai-tool-protocol.md",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_articles(errors: list[str]) -> None:
    for rel in TOPIC_PATHS:
        path = DOCS / rel
        if not path.exists():
            fail(errors, f"missing article: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                fail(errors, f"{rel} missing section {section}")
        if len(re.findall(r"[\u4e00-\u9fff]", text)) < 1200:
            fail(errors, f"{rel} has fewer than 1200 Han characters")


def check_longforms(errors: list[str]) -> None:
    longforms = [p for p in DOCS.glob("*/longform/*.md") if p.name != "README.md"]
    if len(longforms) != 40:
        fail(errors, f"expected 40 longforms, found {len(longforms)}")
    for path in longforms:
        text = path.read_text(encoding="utf-8")
        if len(re.findall(r"[\u4e00-\u9fff]", text)) < 2200:
            fail(errors, f"{path.relative_to(ROOT)} has fewer than 2200 Han characters")


def check_planning(errors: list[str]) -> None:
    conflicts = sorted((PLAN_DIR / "conflicts").glob("*.md"))
    recaps = sorted((PLAN_DIR / "recaps").glob("*.md"))
    if len(conflicts) != 50:
        fail(errors, f"expected 50 conflict files, found {len(conflicts)}")
    if len(recaps) != 10:
        fail(errors, f"expected 10 recap files, found {len(recaps)}")
    matrix = PLAN_DIR / "publishing-matrix.md"
    if not matrix.exists():
        fail(errors, "missing publishing matrix")
    else:
        rows = [line for line in matrix.read_text(encoding="utf-8").splitlines() if line.startswith("| 2026-")]
        if len(rows) != 50:
            fail(errors, f"expected 50 publishing matrix rows, found {len(rows)}")


def check_images(errors: list[str]) -> None:
    pngs = sorted(DIAGRAM_DIR.glob("*.png"))
    prompts = sorted(PROMPT_DIR.glob("*.md"))
    if len(pngs) != 50:
        fail(errors, f"expected 50 PNG files, found {len(pngs)}")
    if len(prompts) != 50:
        fail(errors, f"expected 50 prompt files, found {len(prompts)}")
    for path in pngs:
        with Image.open(path) as img:
            if img.size != (1024, 1536):
                fail(errors, f"{path.relative_to(ROOT)} has size {img.size}, expected 1024x1536")


def main() -> int:
    errors: list[str] = []
    check_articles(errors)
    check_longforms(errors)
    check_planning(errors)
    check_images(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("modern infrastructure content pack check passed")
    print("articles=50 longforms=40 conflicts=50 recaps=10 prompts=50 png=50")
    return 0


if __name__ == "__main__":
    sys.exit(main())
