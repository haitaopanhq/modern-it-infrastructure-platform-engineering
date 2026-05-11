# -----------------------------
# 《图解现代化 IT 基础架构与平台工程》
# Auto-build all Markdown files
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

# Discover files - look in docs/zh and docs/en
ZH_MD_FILES := $(wildcard docs/zh/*.md)
EN_MD_FILES := $(wildcard docs/en/*.md)
ROOT_MD_FILES := $(wildcard *.md)

ZH_BASES := $(ZH_MD_FILES:.md=)
EN_BASES := $(EN_MD_FILES:.md=)
ROOT_BASES := $(ROOT_MD_FILES:.md=)

# Outputs - PDF
PDFS := $(ZH_BASES:=.pdf) $(EN_BASES:=.pdf) $(ROOT_BASES:=.pdf)
PDFS := $(filter-out %.pdf,$(PDFS))
PDFS := $(patsubst docs/zh/%.pdf,output/zh/%.pdf,$(PDFS))
PDFS := $(patsubst docs/en/%.pdf,output/en/%.pdf,$(PDFS))

# Outputs - DOCX
DOCXS := $(ZH_MD_FILES:.md=.docx) $(EN_MD_FILES:.md=.docx) $(ROOT_MD_FILES:.md=.docx)
DOCXS := $(patsubst docs/zh/%.docx,output/zh/%.docx,$(DOCXS))
DOCXS := $(patsubst docs/en/%.docx,output/en/%.docx,$(DOCXS))

# Outputs - HTML
HTMLS := $(ZH_MD_FILES:.md=.html) $(EN_MD_FILES:.md=.html) $(ROOT_MD_FILES:.md=.html)
HTMLS := $(patsubst docs/zh/%.html,output/zh/%.html,$(HTMLS))
HTMLS := $(patsubst docs/en/%.html,output/en/%.html,$(HTMLS))

# Pandoc options
GEOMETRY := -V geometry:margin=1in
FONTSIZE := -V fontsize=12pt
TOC := --toc --toc-depth=3

# Directories
OUTPUT_DIR := output
ZH_OUTPUT := $(OUTPUT_DIR)/zh
EN_OUTPUT := $(OUTPUT_DIR)/en

.PHONY: all pdf docx html clean help list

all: directories pdf docx html

directories:
	mkdir -p $(ZH_OUTPUT) $(EN_OUTPUT)

help:
	@echo "Usage:"
	@echo "  make all    - build pdf, docx, html for all *.md"
	@echo "  make pdf    - build PDFs only"
	@echo "  make docx   - build DOCX only"
	@echo "  make html   - build HTML only"
	@echo "  make clean  - remove generated files"
	@echo "  make list   - show detected files"

list:
	@echo "ZH_MD_FILES: $(ZH_MD_FILES)"
	@echo "EN_MD_FILES: $(EN_MD_FILES)"
	@echo "ROOT_MD_FILES: $(ROOT_MD_FILES)"
	@echo "PDFS: $(PDFS)"
	@echo "DOCXS: $(DOCXS)"
	@echo "HTMLS: $(HTMLS)"

# -----------------------------
# PDF rules (xelatex)
# -----------------------------
$(ZH_OUTPUT)/%.pdf: docs/zh/%.md
	$(PANDOC) $< -o $@ --pdf-engine=xelatex \
	  -V mainfont="$(MAIN_FONT)" \
	  -V CJKmainfont="$(CJK_FONT)" \
	  -V sansfont="$(MAIN_FONT)" \
	  -V monofont="$(MAIN_FONT)" \
	  $(GEOMETRY) $(FONTSIZE) $(TOC)

$(EN_OUTPUT)/%.pdf: docs/en/%.md
	$(PANDOC) $< -o $@ --pdf-engine=xelatex \
	  -V mainfont="$(MAIN_FONT)" \
	  -V sansfont="$(MAIN_FONT)" \
	  -V monofont="$(MAIN_FONT)" \
	  $(GEOMETRY) $(FONTSIZE) $(TOC)

output/%.pdf: %.md
	$(PANDOC) $< -o $@ --pdf-engine=xelatex \
	  -V mainfont="$(MAIN_FONT)" \
	  -V CJKmainfont="$(CJK_FONT)" \
	  -V sansfont="$(MAIN_FONT)" \
	  -V monofont="$(MAIN_FONT)" \
	  $(GEOMETRY) $(FONTSIZE) $(TOC)

# -----------------------------
# DOCX rules
# -----------------------------
$(ZH_OUTPUT)/%.docx: docs/zh/%.md
	$(PANDOC) $< -o $@ --variable mainfont="$(MAIN_FONT)" --variable fontsize=12pt $(TOC)

$(EN_OUTPUT)/%.docx: docs/en/%.md
	$(PANDOC) $< -o $@ --variable mainfont="$(MAIN_FONT)" --variable fontsize=12pt $(TOC)

output/%.docx: %.md
	$(PANDOC) $< -o $@ --variable mainfont="$(MAIN_FONT)" --variable fontsize=12pt $(TOC)

# -----------------------------
# HTML rules
# -----------------------------
$(ZH_OUTPUT)/%.html: docs/zh/%.md
	$(PANDOC) $< -o $@ --variable mainfont="$(MAIN_FONT)" --variable fontsize=12pt \
	  --self-contained --css=https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css

$(EN_OUTPUT)/%.html: docs/en/%.md
	$(PANDOC) $< -o $@ --variable mainfont="$(MAIN_FONT)" --variable fontsize=12pt \
	  --self-contained --css=https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css

output/%.html: %.md
	$(PANDOC) $< -o $@ --variable mainfont="$(MAIN_FONT)" --variable fontsize=12pt \
	  --self-contained --css=https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css

# -----------------------------
# Batch targets
# -----------------------------
pdf: directories $(PDFS)
docx: directories $(DOCXS)
html: directories $(HTMLS)

clean:
	$(RM_CMD) -r $(OUTPUT_DIR)
