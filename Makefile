PYTHON?= python
YAML2RST= $(PYTHON) tools/yaml2rst/yaml2rst.py

# Minimal makefile for Sphinx documentation
#
# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build
SPHINX_PREDEFINED_TARGETS := $(shell $(SPHINXBUILD) -M help . .|sed -r '/^\S+/d;s/^\s+(\S+).+/\1/;/^clean/d')
PREDEFINED_TARGETS = $(SPHINX_PREDEFINED_TARGETS) check-includes
INCLUDED_FILES := $(shell grep -ohRE '^\.\. include:: +.+' $(SOURCEDIR) | sed -r "s%^\.\. include:: +%$(SOURCEDIR)%")

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help incfiles clean Makefile

incfiles.mk: $(wildcard data/yaml/gl/*/*.yaml data/yaml/checks/*/*.yaml data/yaml/faq/**/*.yaml)
	@if [ ! -f incfiles.mk ]; then \
		${YAML2RST}; \
	else \
		${YAML2RST} incfiles.mk; \
	fi

incfiles:| $(SOURCEDIR)/inc

ifneq ($(filter $(MAKECMDGOALS),$(PREDEFINED_TARGETS)),)
include incfiles.mk
endif

#
# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
$(SPHINX_PREDEFINED_TARGETS): incfiles.mk incfiles Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@$(RM) -rf $(SOURCEDIR)/inc $(SOURCEDIR)/faq incfiles.mk

$(SOURCEDIR)/inc:
	@$(YAML2RST)

check-includes:
	@for file in $(ALL_INC_FILES); do \
		if ! echo $(INCLUDED_FILES) | grep -q $$file; then \
			echo "Error: File $$file is not referenced"; \
			exit 1; \
		fi; \
	done
