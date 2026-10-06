#!/usr/bin/env python3
"""Probe exact pixel colors from a PNG using only the standard library.

Vision models cannot reliably separate near-identical dark colors, so assert a
diagram's canvas or fill against decoded pixels instead of eyeballing a screenshot.

Usage:
    python png_probe.py IMAGE.png                    # four corners (canvas check)
    python png_probe.py IMAGE.png --at 2,2 --at -3,-3 # explicit coordinates
    python png_probe.py IMAGE.png --bg                # most common color

Coordinates are 0-based; negatives count from the far edge (-1 = last column/row).
Prints "x,y  #RRGGBB" per probe. Exits 1 with a message if the PNG cannot be read.

Requires Python 3.8+ and nothing else -- no PIL, no numpy.
"""

import argparse
import struct
import sys
import zlib
from collections import Counter

# PNG color type -> samples per pixel. 3 (indexed) is resolved through PLTE.
CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}


def read_png(path):
    """Decode an 8-bit non-interlaced PNG into a list of raw row bytearrays."""
    data = open(path, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")

    pos, idat, plte = 8, b"", None
    w = h = depth = ctype = interlace = None
    while pos + 8 <= len(data):
        length, tag = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + length]
        if tag == b"IHDR":
            w, h, depth, ctype, _comp, _filt, interlace = struct.unpack(">IIBBBBB", chunk)
        elif tag == b"PLTE":
            plte = chunk
        elif tag == b"IDAT":
            idat += chunk
        elif tag == b"IEND":
            break
        pos += 12 + length

    if w is None or h is None or not idat:
        raise ValueError("missing IHDR or IDAT chunk")
    if depth != 8:
        raise ValueError("bit depth %s unsupported (only 8-bit)" % depth)
    if interlace:
        raise ValueError("interlaced PNG unsupported")
    if ctype not in CHANNELS:
        raise ValueError("color type %s unsupported" % ctype)

    raw = zlib.decompress(idat)
    nch = CHANNELS[ctype]
    stride = w * nch
    if len(raw) < (stride + 1) * h:
        raise ValueError("truncated image data")

    rows, prev, i = [], bytearray(stride), 0
    for _ in range(h):
        ftype = raw[i]
        i += 1
        line = bytearray(raw[i:i + stride])
        i += stride
        if ftype == 1:            # Sub
            for x in range(nch, stride):
                line[x] = (line[x] + line[x - nch]) & 0xFF
        elif ftype == 2:          # Up
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 0xFF
        elif ftype == 3:          # Average
            for x in range(stride):
                a = line[x - nch] if x >= nch else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 0xFF
        elif ftype == 4:          # Paeth
            for x in range(stride):
                a = line[x - nch] if x >= nch else 0
                b = prev[x]
                c = prev[x - nch] if x >= nch else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                if pa <= pb and pa <= pc:
                    pred = a
                elif pb <= pc:
                    pred = b
                else:
                    pred = c
                line[x] = (line[x] + pred) & 0xFF
        elif ftype != 0:
            raise ValueError("unknown filter type %s" % ftype)
        rows.append(bytes(line))
        prev = line
    return w, h, ctype, nch, plte, rows


def pixel(rows, ctype, nch, plte, x, y):
    """Return the (r, g, b) triple at x, y."""
    offset = x * nch
    line = rows[y]
    if ctype == 3:
        if plte is None:
            raise ValueError("indexed PNG missing PLTE chunk")
        idx = line[offset]
        return tuple(plte[idx * 3:idx * 3 + 3])
    if ctype in (0, 4):           # grayscale (+ alpha)
        g = line[offset]
        return (g, g, g)
    return tuple(line[offset:offset + 3])


def _normalize_argv(argv):
    """Let '--at -3,-3' be written naturally.

    argparse only excuses a token that matches a *bare* negative number ('-3');
    an 'X,Y' coordinate carries a comma, so a from-end probe is read as an
    unknown flag and dies with "expected one argument". Re-attach such values
    with '=' before parsing.
    """
    out = []
    for tok in argv:
        if out and out[-1] == "--at" and tok.startswith("-"):
            out[-1] = "--at=" + tok
        else:
            out.append(tok)
    return out


def main():
    ap = argparse.ArgumentParser(
        description="Probe exact PNG pixel colors (stdlib only, no PIL).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Coordinates are 0-based; negatives count from the far edge.",
    )
    ap.add_argument("image", help="path to a PNG file")
    ap.add_argument("--at", action="append", default=[], metavar="X,Y",
                    help="probe a coordinate; repeatable")
    ap.add_argument("--bg", action="store_true",
                    help="report the most common color (page background)")
    args = ap.parse_args(_normalize_argv(sys.argv[1:]))

    w, h, ctype, nch, plte, rows = read_png(args.image)
    print("%s: %dx%d colortype=%d" % (args.image, w, h, ctype))

    def resolve(spec):
        xs, ys = spec.split(",", 1)
        x, y = int(xs.strip()), int(ys.strip())
        return (w + x if x < 0 else x, h + y if y < 0 else y)

    probes = [resolve(s) for s in args.at]
    if not probes and not args.bg:
        probes = [(1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)]

    for x, y in probes:
        if not (0 <= x < w and 0 <= y < h):
            print("%d,%d  OUT OF BOUNDS (image is %dx%d)" % (x, y, w, h))
            continue
        r, g, b = pixel(rows, ctype, nch, plte, x, y)
        print("%d,%d  #%02X%02X%02X" % (x, y, r, g, b))

    if args.bg:
        # Subsample large renders so --bg stays interactive; a flat page
        # background is overwhelmingly dominant either way.
        step = max(1, int((w * h / 2_000_000) ** 0.5) + 1)
        counts, total = Counter(), 0
        for y in range(0, h, step):
            for x in range(0, w, step):
                counts[pixel(rows, ctype, nch, plte, x, y)] += 1
                total += 1
        (r, g, b), n = counts.most_common(1)[0]
        print("bg    #%02X%02X%02X  (%.1f%% of sampled pixels)"
              % (r, g, b, 100.0 * n / total))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:      # argparse already handles -h / bad args
        sys.exit("png_probe: %s" % exc)
