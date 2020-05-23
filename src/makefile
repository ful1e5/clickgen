all: xcursorgen.so

xcursorgen.so: xcursorgen.c
	gcc -Wl,-zdefs -shared -o xcursorgen.so -fPIC  xcursorgen.c  -lc -lpng16 -lXcursor -lX11
	cp xcursorgen.so ../clickgen/xcursorgen.so

clean:
	rm -f *.o *.so