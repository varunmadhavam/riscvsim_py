
all: 
	$(MAKE) -C sw
	python3 cli.py
test:
	$(MAKE) -C sw test
	python3 cli.py test
disass:
	$(MAKE) -C sw disass
disasstest:
	$(MAKE) -C sw disasstest
clean:
	$(MAKE) -C sw clean
cleantest:
	$(MAKE) -C sw cleantest