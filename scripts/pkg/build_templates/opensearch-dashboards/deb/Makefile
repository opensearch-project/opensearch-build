all: install

install:
	mkdir -p $(CURDIR)/debian/opensearch-dashboards
	cp -a $(CURDIR)/etc $(CURDIR)/debian/opensearch-dashboards/etc
	cp -a $(CURDIR)/usr $(CURDIR)/debian/opensearch-dashboards/usr
	cp -a $(CURDIR)/var $(CURDIR)/debian/opensearch-dashboards/var

clean: ;

distclean: clean

.PHONY: all clean distclean install
