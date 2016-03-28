#!/usr/bin/env python
"""
simple example script for scrubping solution code cells from IPython notebooks
Usage: `scrub_code.py foo.ipynb [bar.ipynb [...]]`
Marked code cells are scrubbed from the notebook
"""

import io
import os
import sys

from nbformat import read, write, NO_CONVERT

def scrub_code_cells(nb):
    scrubbed = 0
    cells = 0
    #for ws in nb.worksheets:
    #    for cell in ws.cells:
    for cell in nb.cells:
        if cell.cell_type != 'code':
            continue
        cells += 1
        # scrub cells marked with initial '# Solution' comment
        # any other marker will do, or it could be unconditional
        if cell.source.startswith("# Solution"):
            cell.source = u'# Solution goes here'
            scrubbed += 1
            cell.outputs = []

    print
    print("scrubbed %i/%i code cells from notebook" % (scrubbed, cells))

if __name__ == '__main__':
    for ipynb in sys.argv[1:]:
        print("scrubbing %s" % ipynb)
        with io.open(ipynb, encoding='utf8') as f:
            nb = read(f, NO_CONVERT)
        scrub_code_cells(nb)
        base, ext = os.path.splitext(ipynb)
        new_ipynb = "%s_blank%s" % (base, ext)
        with io.open(new_ipynb, 'w', encoding='utf8') as f:
            write(nb, f)
        print("wrote %s" % new_ipynb)
