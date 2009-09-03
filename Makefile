
PYTHON = /usr/local/bin/python2.5
NOSE = nosetests-2.5
GAE_LIB_ROOT = /home/nori/Desktop/work/gae/google_appengine
NAME = proxy
SRCDIR = src
BUILDDIR = build


all: app

app: source
	cp -r $(SRCDIR) $(BUILDDIR)/

source: build
	cp $(SRCDIR)/*py $(BUILDDIR)
	cp $(SRCDIR)/*yaml $(BUILDDIR)

build:
	-mkdir -p $(BUILDDIR)


start_dev_server:
	$(PYTHON) $(GAE_LIB_ROOT)/dev_appserver.py $(BUILDDIR)

test: build
	$(NOSE) \
    --with-gae \
    --gae-lib-root=$(GAE_LIB_ROOT) \
    --gae-application=$(BUILDDIR) \
    tests
#   --gae-datastore=$(DATASTORE) 
#    -x \

clean:
	-rm -rf $(BUILDDIR)


install:
	$(PYTHON) $(GAE_LIB_ROOT)/appcfg.py update builds

