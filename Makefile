# -----------------------------
# 《图解现代化 IT 基础架构与平台工程》
# Auto-build all Markdown files recursively
# Unified CJK + Latin fonts for PDFs
# -----------------------------

# OS & tools
OS := $(shell uname -s)
ifeq ($(OS),Linux)
    MAIN_FONT := DejaVu Serif
    CJK_FONT  := Noto Sans CJK SC
    PANDOC    := pandoc
    RM_CMD    := rm -rvf
else ifeq ($(OS),Darwin)
    MAIN_FONT := Times New Roman
    CJK_FONT  := PingFang SC
    PANDOC    := pandoc
    RM_CMD    := rm -rvf
else ifeq ($(OS),Windows_NT)
    MAIN_FONT := Times New Roman
    CJK_FONT  := Microsoft YaHei
    PANDOC    := pandoc.exe
    RM_CMD    := del /Q
else
    MAIN_FONT := Times New Roman
    CJK_FONT  := Noto Sans CJK SC
    PANDOC    := pandoc
    RM_CMD    := rm -rvf
endif

# Discover files recursively. Keep generated output, VCS metadata, and
# dependency folders out of the source set.
MD_FILES := $(shell find . -name '*.md' -not -path './.git/*' -not -path './output/*' -not -path './dist/*' -not -path './node_modules/*' -not -path './it-infra-evolution-promo/*' | sed 's,^\./,,' | sort)

# Outputs preserve source-relative paths under output/.
PDFS  := $(patsubst %.md,output/%.pdf,$(MD_FILES))
DOCXS := $(patsubst %.md,output/%.docx,$(MD_FILES))
HTMLS := $(patsubst %.md,output/%.html,$(MD_FILES))

OUTPUT_DIR := output
DIST_DIR := dist
PACKAGE_BASENAME := modern-it-infrastructure-platform-engineering
PACKAGE_TGZ := $(DIST_DIR)/$(PACKAGE_BASENAME).tar.gz
PDF_PACKAGE_TGZ := $(DIST_DIR)/$(PACKAGE_BASENAME)-pdf.tar.gz
DOCX_PACKAGE_TGZ := $(DIST_DIR)/$(PACKAGE_BASENAME)-docx.tar.gz
HTML_PACKAGE_TGZ := $(DIST_DIR)/$(PACKAGE_BASENAME)-html.tar.gz
IT_INFRA_EVOLUTION_BOOK_TITLE := IT 基础设施演进之路
IT_INFRA_EVOLUTION_BOOK_MD := \
	docs/zh/00-it-infrastructure-evolution-road.md \
	docs/zh/01-modern-it-systems.md \
	docs/zh/02-networking-protocols.md \
	docs/zh/03-database-systems.md \
	docs/zh/04-storage-systems.md \
	docs/zh/05-observability.md \
	docs/zh/06-devops-to-platform-engineering.md \
	docs/zh/07-platform-engineering-core.md \
	docs/zh/10-security-compliance.md
IT_INFRA_EVOLUTION_BOOK_PDF := $(DIST_DIR)/it-infrastructure-evolution-road.pdf

# Pandoc common opts
GEOMETRY := -V geometry:margin=1in
FONTSIZE := -V fontsize=12pt
TOC := --toc --toc-depth=3
HTML_CSS := assets/pandoc.css

.PHONY: all pdf docx html ebook ebook-it-infra-evolution package clean help list check-content

all: pdf docx html

help:
	@echo "Usage:"
	@echo "  make [all]       - build pdf, docx, html for all Markdown files"
	@echo "  make pdf         - build PDFs only"
	@echo "  make docx        - build DOCX only"
	@echo "  make html        - build HTML only"
	@echo "  make ebook       - build the merged IT infrastructure evolution PDF ebook"
	@echo "  make ebook-it-infra-evolution - build dist/it-infrastructure-evolution-road.pdf"
	@echo "  make package     - build all outputs and package all/pdf/docx/html archives"
	@echo "  make check-content - validate generated content pack"
	@echo "  make clean       - remove generated files"
	@echo "  make list        - show detected files"

list:
	@echo "MD_FILES:"
	@printf '  %s\n' $(MD_FILES)
	@echo "PDFS:  $(words $(PDFS))"
	@echo "DOCXS: $(words $(DOCXS))"
	@echo "HTMLS: $(words $(HTMLS))"
	@echo "IT_INFRA_EVOLUTION_BOOK_MD:"
	@printf '  %s\n' $(IT_INFRA_EVOLUTION_BOOK_MD)
	@echo "IT_INFRA_EVOLUTION_BOOK_PDF: $(IT_INFRA_EVOLUTION_BOOK_PDF)"

# -----------------------------
# Pattern rules
# -----------------------------

output/%.pdf: %.md
	@mkdir -p "$(dir $@)"
	$(PANDOC) "$<" -o "$@" --pdf-engine=xelatex \
	  --resource-path=".:$(dir $<)" \
	  -V mainfont="$(MAIN_FONT)" \
	  -V CJKmainfont="$(CJK_FONT)" \
	  -V sansfont="$(MAIN_FONT)" \
	  -V monofont="$(MAIN_FONT)" \
	  $(GEOMETRY) $(FONTSIZE) $(TOC)

output/%.docx: %.md
	@mkdir -p "$(dir $@)"
	$(PANDOC) "$<" -o "$@" \
	  --resource-path=".:$(dir $<)" \
	  --variable mainfont="$(MAIN_FONT)" \
	  --variable fontsize=12pt \
	  $(TOC)

output/%.html: %.md
	@mkdir -p "$(dir $@)"
	$(PANDOC) "$<" -o "$@" \
	  --resource-path=".:$(dir $<)" \
	  --variable mainfont="$(MAIN_FONT)" \
	  --variable fontsize=12pt \
	  --embed-resources --standalone \
	  --css="$(HTML_CSS)"

# -----------------------------
# Batch targets
# -----------------------------

pdf: $(PDFS)
docx: $(DOCXS)
html: $(HTMLS)

ebook: ebook-it-infra-evolution

ebook-it-infra-evolution:
	@missing=0; \
	for file in $(IT_INFRA_EVOLUTION_BOOK_MD); do \
	  if [ ! -f "$$file" ]; then \
	    echo "Missing ebook source: $$file" >&2; \
	    missing=1; \
	  fi; \
	done; \
	if [ "$$missing" -ne 0 ]; then \
	  echo "Cannot build $(IT_INFRA_EVOLUTION_BOOK_PDF): create the missing source files first." >&2; \
	  exit 1; \
	fi
	@mkdir -p "$(DIST_DIR)"
	$(PANDOC) $(IT_INFRA_EVOLUTION_BOOK_MD) -o "$(IT_INFRA_EVOLUTION_BOOK_PDF)" --pdf-engine=xelatex \
	  --standalone \
	  --resource-path=".:docs/zh" \
	  --metadata title="$(IT_INFRA_EVOLUTION_BOOK_TITLE)" \
	  -V title="$(IT_INFRA_EVOLUTION_BOOK_TITLE)" \
	  -V mainfont="$(MAIN_FONT)" \
	  -V CJKmainfont="$(CJK_FONT)" \
	  -V sansfont="$(MAIN_FONT)" \
	  -V monofont="$(MAIN_FONT)" \
	  $(GEOMETRY) $(FONTSIZE) $(TOC)

package: all ebook-it-infra-evolution
	python3 scripts/package_outputs.py --output-dir "$(OUTPUT_DIR)" --dist-dir "$(DIST_DIR)"

check-content:
	python3 scripts/check_modern_infra_pack.py

clean:
	$(RM_CMD) "$(OUTPUT_DIR)" "$(DIST_DIR)"
