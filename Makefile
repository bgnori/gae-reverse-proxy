
PYTHON = /usr/local/bin/python2.5
NOSE = nosetests-2.5
GAE_LIB_ROOT = /home/nori/Desktop/work/gae/google_appengine
NAME = proxy
USER = usr
SRCDIR = src
BUILDDIR = build


all: app

app: source
	cp -r $(SRCDIR) $(BUILDDIR)/

source: build
	cp $(SRCDIR)/*py $(BUILDDIR)
	cp $(SRCDIR)/*yaml $(BUILDDIR)
	$(PYTHON) util/mergeyaml.py $(SRCDIR)/app.yaml.template $(USER)/app.yaml > $(BUILDDIR)/app.yaml


build:
	-mkdir -p $(BUILDDIR)

start_dev_server:
	$(PYTHON) $(GAE_LIB_ROOT)/dev_appserver.py $(BUILDDIR)

start_stubd:
	$(PYTHON) util/stubd.py localhost 8001

test: build
	$(NOSE) \
    --with-gae \
    --gae-lib-root=$(GAE_LIB_ROOT) \
    --gae-application=$(BUILDDIR) \
    tests
#   --gae-datastore=$(DATASTORE) 
#    -x \

unittest:
	$(NOSE) \
    --with-gae \
    --gae-lib-root=$(GAE_LIB_ROOT) \
    tests

clean:
	-rm -rf $(BUILDDIR)

install: app
	$(PYTHON) $(GAE_LIB_ROOT)/appcfg.py update $(BUILDDIR)


