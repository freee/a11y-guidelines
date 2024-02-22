SUBDIRS = ja en
export ROOTDIR = $(CURDIR)

.PHONY: all $(SUBDIRS)
all: $(SUBDIRS)

$(SUBDIRS):
	@$(MAKE) -C $@ $(MAKECMDGOALS)

%: $(SUBDIRS)
	@:
