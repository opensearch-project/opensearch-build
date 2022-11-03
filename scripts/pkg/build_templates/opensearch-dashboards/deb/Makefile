TMP_PATH = /tmp/$(notdir $(CURDIR))
OUTPUT_PATH = $(TMP_PATH)/debian/opensearch

all: install

install:
	mkdir -p $(OUTPUT_PATH)
	cp -a $(TMP_PATH)/etc $(OUTPUT_PATH)/etc
	cp -a $(TMP_PATH)/usr $(OUTPUT_PATH)/usr
	cp -a $(TMP_PATH)/var $(OUTPUT_PATH)/var

clean: ;

distclean: clean

.PHONY: all clean distclean install
