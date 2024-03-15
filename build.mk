rootdir = $(ROOTDIR)
PYTHON?= python
YAML2RST= $(PYTHON) $(rootdir)/tools/yaml2rst/yaml2rst.py -b $(rootdir) -l $(lang)

ifneq ($(BASE_URL),)
html_baseurl = $(BASE_URL)
else
html_baseurl =
endif
baseurl_ja = $(html_baseurl)
baseurl_en = $(html_baseurl)en/
base_url_options=-D html_baseurl=$(html_baseurl)$(base_url_suffix) -A baseurl_ja=$(baseurl_ja) -A baseurl_en=$(baseurl_en)

SPHINXOPTS= $(sphinx_options) $(base_url_options)
SOURCEDIR     = source
BUILDDIR      = build
INCLUDED_FILES := $(shell grep -ohRE '^\.\. include:: +.+' $(SOURCEDIR) | sed -r "s%^\.\. include:: +%$(CURDIR)/$(SOURCEDIR)%")

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help incfiles clean Makefile $(SPHINX_PREDEFINED_TARGETS)

incfiles.mk:
	@${YAML2RST} incfiles.mk 

incfiles:| $(SOURCEDIR)/inc $(SOURCEDIR)/faq

include incfiles.mk

#
# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
$(SPHINX_PREDEFINED_TARGETS): incfiles.mk incfiles Makefile $(BUILDDIR)/.all-rst $(ALL_RST_FILES)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

$(BUILDDIR)/.all-rst:
	@$(YAML2RST)
	@touch $@

clean:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@$(RM) -rf $(SOURCEDIR)/inc $(SOURCEDIR)/faq incfiles.mk

$(SOURCEDIR)/inc $(SOURCEDIR)/faq:
	@$(YAML2RST)
	@touch $(BUILDDIR)/.all-rst

check-includes:
	@for file in $(ALL_INC_FILES); do \
		if ! echo $(INCLUDED_FILES) | grep -q $$file; then \
			echo "Error: File $$file is not referenced"; \
			exit 1; \
		fi; \
	done
