
NOSE = nosetests-2.5
GAE_LIB_ROOT = /home/nori/Desktop/work/gae/google_appengine
NAME = proxy
SRCDIR = src
BUILDDIR = builds


build:
	-mkdir -p $(BUILDDIR) ;\
  cp -r $(SRCDIR) $(BUILDDIR)/


start_deb_server:
	$(GAE_LIB_ROOT)/dev_appserver.py proxy

test: build
	$(NOSE) \
    --with-gae \
    --gae-lib-root= $(GAE_LIB_ROOT) \
    --gae-application=$(NAME) \
    $(BUILDDIR)

clean:
	-rm -rf $(BUILDDIR)


install:
	$(GAE_LIB_ROOT)/appcfg.py update builds

