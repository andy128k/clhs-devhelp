ARCHIVE=HyperSpec-7-0.tar.gz

clhs/clhs.devhelp2: clhs clhs.devhelp.start toc index clhs.devhelp.end
	cat clhs.devhelp.start toc index clhs.devhelp.end > clhs/clhs.devhelp2

toc: clhs
	./scan-toc > toc

index: clhs
	./scan-index > index

clhs: $(ARCHIVE)
	mkdir clhs
	tar -zxf $(ARCHIVE) -C clhs

$(ARCHIVE):
	wget ftp://ftp.lispworks.com/pub/software_tools/reference/$(ARCHIVE)

