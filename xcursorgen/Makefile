all: clean xcursorgen.so
.PHONY: all

CC = gcc
LIBS = -lX11 -lXcursor -lpng -lz
OUT_DIR = ../clickgen

xcursorgen.so: xcursorgen.c
	$(CC) -Wextra -Wall -g -Wl,-zdefs -shared -o xcursorgen.so -fPIC  xcursorgen.c $(LIBS) 
	cp -r xcursorgen.so $(OUT_DIR)/xcursorgen.so

clean:
	@rm -rf *.o *.so $(OUT_DIR)/xcursorgen.so
