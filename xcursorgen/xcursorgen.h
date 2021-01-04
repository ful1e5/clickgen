/*
 * xcursorgen.h
 *
 * Copyright (C) 2020 Kaiz Khatri
 *
 * Permission to use, copy, modify, distribute, and sell this software and its
 * documentation for any purpose is hereby granted without fee, provided that
 * the above copyright notice appear in all copies and that both that
 * copyright notice and this permission notice appear in supporting
 * documentation, and that the name of Kaiz Khatri not be used in
 * advertising or publicity pertaining to distribution of the software without
 * specific, written prior permission.  Kaiz Khatri makes no
 * representations about the suitability of this software for any purpose.  It
 * is provided "as is" without express or implied warranty.
 *
 * KAIZ KHATRI DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
 * INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
 * EVENT SHALL KAIZ KHATRI BE LIABLE FOR ANY SPECIAL, INDIRECT OR
 * CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
 * DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
 * TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
 * PERFORMANCE OF THIS SOFTWARE.
 */

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xcursor/Xcursor.h>

#include <png.h>

#define PACKAGE_VERSION "1.0.0"

struct flist
{
    int size;
    int xhot, yhot;
    int delay;
    char *pngfile;
    struct flist *next;
};

#ifndef XCURSORGEN_H

#define XCURSORGEN_H

static void usage(const char *name);
static int read_config_file(const char *config, struct flist **list);
static void premultiply_data(png_structp png, png_row_infop row_info, png_bytep data);
static XcursorImage *load_image(struct flist *list, const char *prefix);
static int write_cursors(int count, struct flist *list, const char *filename, const char *prefix);
static int check_image(char *image);
int main(int argc, char *argv[]);

#endif