all: xcursorgen.so

CC= gcc
LIBS= -lX11 -lXcursor -lpng -lz

xcursorgen.so: xcursorgen.c
	$(CC) -Wl,-zdefs -shared -o xcursorgen.so -fPIC  xcursorgen.c $(LIBS) 
	cp xcursorgen.so ../clickgen/xcursorgen.so

clean:
	rm -f *.o *.so