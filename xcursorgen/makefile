all: xcursorgen.so

xcursorgen.so: xcursorgen.c
	gcc -c -fPIC xcursorgen.c
	gcc -static-libgcc -o xcursorgen.so -Wl,--whole-archive -L/usr/lib/x86_64-linux-gnu/ -I/usr/lib/x86_64-linux-gnu/ -lX11 -lpng -lXcursor -Wl,--no-whole-archive -shared xcursorgen.o
	cp xcursorgen.so ../clickgen/xcursorgen.so

clean:
	rm -f *.o *.so