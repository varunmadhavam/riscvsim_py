
all: 
	$(MAKE) -C sw
	python3 soc.py
test:
	$(MAKE) -C sw/test
	python3 soc.py test
disass:
	$(MAKE) -C sw disass
disasstest:
	$(MAKE) -C sw/test disass
clean:
	$(MAKE) -C sw clean
cleantest:
	$(MAKE) -C sw/test clean