BUILD_PROCEDURE_VERSION = 1
SUBDIRS = ja en

export ROOTDIR = $(CURDIR)
export SPHINXBUILD   ?= sphinx-build
export SPHINX_PREDEFINED_TARGETS := $(shell $(SPHINXBUILD) -M help . .|sed -r '/^\S+/d;s/^\s+(\S+).+/\1/;/^clean/d')
export PREDEFINED_TARGETS = check-includes clean
export ALL_PREDEFINED_TARGETS = $(SPHINX_PREDEFINED_TARGETS) $(PREDEFINED_TARGETS)

.PHONY: all $(SUBDIRS) $(ALL_PREDEFINED_TARGETS) build-procedure-version

all: html

$(ALL_PREDEFINED_TARGETS):
	@for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir $@ || exit 1; \
	done

# $(SUBDIRS):
# 	@target="$(MAKECMDGOALS)"; \
# 	for subdir_target in $(ALL_PREDEFINED_TARGETS); do \
# 		if [ "$$target" = "$$subdir_target" ]; then \
# 			echo "Running make $$target in subdirectory $@"; \
# 			$(MAKE) -C $@ $$target || exit 1; \
# 			break; \
# 		fi; \
# 	done

# %: $(SUBDIRS)
# 	@:

build-procedure-version:
	@echo $(BUILD_PROCEDURE_VERSION)
