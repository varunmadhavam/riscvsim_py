
all: 
	$(MAKE) -C sw
	python3 soc.py
disass:
	$(MAKE) -C sw disass
clean:
	$(MAKE) -C sw clean