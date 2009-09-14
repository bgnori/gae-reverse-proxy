
PYTHON = /usr/local/bin/python2.5
NOSE = nosetests-2.5
GAE_LIB_ROOT = /home/nori/Desktop/work/gae/google_appengine
NAME = proxy
USER = usr


all: build

build: $(USER)
	-mkdir -p build
	cp src/*py build
	$(PYTHON) util/mergeyaml.py src/app.yaml.template $(USER)/app.yaml > build/app.yaml
	$(PYTHON) util/mergeyaml.py src/cron.yaml.template $(USER)/cron.yaml > build/cron.yaml

start_dev_server:
	$(PYTHON) $(GAE_LIB_ROOT)/dev_appserver.py build

start_stubd:
	$(PYTHON) util/stubd.py localhost 8001

test: build
	$(NOSE) \
    --with-gae \
    --gae-lib-root=$(GAE_LIB_ROOT) \
    --gae-application=build \
    tests
#   --gae-datastore=$(DATASTORE) 
#    -x \

crawl:
	$(PYTHON) util/crawl.py $(USER)

guess:
	$(PYTHON) util/guess.py $(USER)/guess.yaml 

clean:
	-rm -rf build
	-rm  $(USER)/*pyc
	-rm  tests/*pyc
	-rm  src/*pyc
	-rm  lib/*pyc

install: app
	$(PYTHON) $(GAE_LIB_ROOT)/appcfg.py update build

