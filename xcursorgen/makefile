all: xcursorgen.so

CC= gcc
LIBS= -lX11 -lpng -lXcursor
L_FLAG= -L /usr/lib/x86_64-linux-gnu/

xcursorgen.so: xcursorgen.c
	$(CC) -c -fPIC xcursorgen.c
	$(CC) -o xcursorgen.so -Wl,--whole-archive $(L_FLAG) $(LIBS) -Wl,--no-whole-archive -shared xcursorgen.o
	cp xcursorgen.so ../clickgen/xcursorgen.so

clean:
	rm -f *.o *.so