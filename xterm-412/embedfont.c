/*
 * Copyright 2026 by Peter Marquardt <wwwutz@users.noreply.github.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE ABOVE LISTED COPYRIGHT HOLDER(S) BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * Except as contained in this notice, the name(s) of the above copyright
 * holders shall not be used in advertising or otherwise to promote the
 * sale, use or other dealings in this Software without prior written
 * authorization.
 */

/*
 * Register the TrueType fonts compiled into xterm (see mkembedfont.sh) with
 * fontconfig, so that the default faceName works without installing them.
 *
 * fontconfig only adds application fonts from files, so each font is copied
 * into an anonymous memory file (memfd) and added by its /proc/self/fd path.
 * fontconfig then sees all of its styles and named instances (e.g., Bold in a
 * variable font), and Xft opens them through that path.  The descriptors stay
 * open for the life of the process, and are not inherited by the shell.
 */

#define _GNU_SOURCE		/* memfd_create */

#include <xterm.h>
#include <fontutils.h>

#if OPT_RENDERFONT

#include <sys/mman.h>
#include <unistd.h>

#include <embedded_fonts.h>

void
xtermAddEmbeddedFonts(void)
{
    static Bool done = False;
    size_t n;

    if (done)
	return;
    done = True;

    for (n = 0; n < XtNumber(embedded_fonts); ++n) {
	const unsigned char *data = embedded_fonts[n].data;
	size_t left = embedded_fonts[n].size;
	char path[40];
	int fd;

	if ((fd = memfd_create("xterm-font", MFD_CLOEXEC)) < 0) {
	    TRACE(("xtermAddEmbeddedFonts: memfd_create failed\n"));
	    return;
	}
	while (left != 0) {
	    ssize_t wrote = write(fd, data, left);
	    if (wrote <= 0)
		break;
	    data += wrote;
	    left -= (size_t) wrote;
	}
	sprintf(path, "/proc/self/fd/%d", fd);
	if (left != 0
	    || !FcConfigAppFontAddFile(NULL, (const FcChar8 *) path)) {
	    TRACE(("xtermAddEmbeddedFonts: cannot add %s\n", path));
	    close(fd);
	}
    }
}

#endif /* OPT_RENDERFONT */
