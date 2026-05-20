# Illustrated Modern IT Infrastructure & Platform Engineering

[中文](./README.md)

## Project Overview

An open-source illustrated book covering modern IT infrastructure, platform engineering, observability, and AI Agent workflows.

The main narrative is evolving from a tool-by-tool tutorial into a technical-history view of infrastructure: technology, business pressure, organizational anxiety, and system complexity explain how infrastructure moves from hardware, virtualization, cloud control planes, runtime, networking, data systems, and platform engineering toward AI Infra and Agent control planes.

## Target Audience

- Infrastructure Engineers
- DevOps / SRE Engineers
- Platform Engineering Teams
- Technical Architects
- AI Agent Engineering Teams

## Read Online

- [GitHub Pages](https://haitaopanhq.github.io/modern-it-infrastructure-platform-engineering/)

## New Capability

### Merged PDF ebook: IT Infrastructure Evolution Road

The repository includes a dedicated Make target that merges the prologue and chapters 01-07 into one PDF ebook:

- Prologue: `docs/zh/00-it-infrastructure-evolution-road.md`
- Chapter 1: Modern IT Systems
- Chapter 2: Networking and Protocols
- Chapter 3: Database Systems
- Chapter 4: Storage Systems
- Chapter 5: Observability and Monitoring
- Chapter 6: From Manual Ops to Platform Engineering
- Chapter 7: Platform Engineering Core Capabilities

This merged PDF is intended for standalone reading, sharing, and GitHub Release distribution.

## Examples

Build the merged PDF ebook:

```bash
make ebook-it-infra-evolution
```

Or use the short alias:

```bash
make ebook
```

Output:

```text
dist/it-infrastructure-evolution-road.pdf
```

Build all PDF / DOCX / HTML outputs and keep the merged ebook:

```bash
make package
```

Validate the 50-day Modern Infrastructure Evolution content pack:

```bash
make check-content
```

List source files and the merged ebook chapter order:

```bash
make list
```

## Release Assets

GitHub Actions builds:

- PDF / DOCX / HTML for each Markdown file
- `dist/modern-it-infrastructure-platform-engineering-*.tar.gz`
- `dist/it-infrastructure-evolution-road.pdf`

`it-infra-evolution-promo/` is a local video/promo workspace. It is ignored by git and excluded from Markdown document discovery.

## Contributing

Issues and Pull Requests are welcome!

## License

MIT License
