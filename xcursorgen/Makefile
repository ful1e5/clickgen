all: xcursorgen.so

CC= gcc
LIBS= -lX11 -lXcursor -lpng -lz
OUT_DIR= ../clickgen
CP= cp -f

xcursorgen.so: xcursorgen.c
	$(CC) -Wl,-zdefs -shared -o xcursorgen.so -fPIC  xcursorgen.c $(LIBS) 
	$(CP) xcursorgen.so $(OUT_DIR)/xcursorgen.so

clean:
	@rm -rf *.o *.so $(OUT_DIR)/xcursorgen.so
