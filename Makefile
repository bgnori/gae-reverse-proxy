

NOSE = nosetests-2.5
GAE_LIB_ROOT = /home/nori/Desktop/work/gae/google_appengine
NAME = proxy


build:
	echo 'build'

start_deb_server:
	$(GAE_LIB_ROOT)/dev_appserver.py proxy

test:
	$(NOSE) \
    --with-gae \
    --gae-lib-root= $(GAE_LIB_ROOT) \
    --gae-application=$(NAME) \
    test

install:
	$(GAE_LIB_ROOT)/appcfg.py update $(NAME)

