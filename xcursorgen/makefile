all: xcursorgen.so

CC= gcc
LIBS= -lX11 -lXcursor -lpng -lz
MKDIR_P= mkdir -p
OUT_DIR= ../libs
CP= cp -f

xcursorgen.so: xcursorgen.c
	$(CC) -Wl,-zdefs -shared -o xcursorgen.so -fPIC  xcursorgen.c $(LIBS) 
	$(MKDIR_P) $(OUT_DIR)
	$(CP) xcursorgen.so $(OUT_DIR)/xcursorgen.so

clean:
	rm -rf *.o *.so $(OUT_DIR)