all: install

install:
	mkdir -p $(CURDIR)/debian/opensearch
	cp -a $(CURDIR)/etc $(CURDIR)/debian/opensearch/etc
	cp -a $(CURDIR)/usr $(CURDIR)/debian/opensearch/usr
	cp -a $(CURDIR)/var $(CURDIR)/debian/opensearch/var

clean: ;

distclean: clean

.PHONY: all clean distclean install
