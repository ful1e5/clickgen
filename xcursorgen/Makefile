all: clean xcursorgen.so
.PHONY: all

CC ?= gcc
LIBS = -lX11 -lXcursor -lpng -lz
OUT_DIR = ../clickgen

xcursorgen.so: xcursorgen.c
	$(CC) -Wextra -Wall $(CFLAGS) $(LDFLAGS) -Wl,-zdefs -shared -o $@ -fPIC  $< $(LIBS)
	cp $@ $(OUT_DIR)/xcursorgen.so

clean:
	@rm -rf *.o *.so $(OUT_DIR)/xcursorgen.so
