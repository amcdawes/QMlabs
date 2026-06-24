Quantum Mechanics in Python
======

## Bug-fix only
I am no longer actively teaching so this content is maintained only for bug-fixes. I have migrated it to use QuTip 5 but I don't plan to continue to expand the scope of the content. Instead, I will be using this content as the starting point for a more general [QuTip book](https://github.com/amcdawes/qutip-book)

[![Test Notebooks](https://github.com/amcdawes/QMlabs/actions/workflows/test-notebooks.yml/badge.svg)](https://github.com/amcdawes/QMlabs/actions/workflows/test-notebooks.yml)

This is a set of Jupyter notebooks (running python) for use in a Quantum Mechanics class. The material is based on (and in sequence with) Mark Beck's book "Quantum Mechanics: Theory and Experiment" but the notebooks can be used independently and with or without a QM textbook.

These are a mix of in-class activities (organized by Chapter title) or longer lab-length activities ("Lab" title). The labs are numbered in order, and the title corresponds to book chapter titles.

To run interactive versions of these notebooks, please: [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/amcdawes/QMlabs/master)

## Examples:
The file `AAPTWM2018.pdf` contains slides for my talk presented at the AAPT Winter Meeting in 2018. Additionally, a longer version of the talk was presented at PyCon 2017 and is available on [YouTube](https://www.youtube.com/watch?v=1ze-Zzn4TAA&feature=youtu.be&t=2m32s). 

## Installation:

The notebooks require [QuTiP 5](http://qutip.org) (Quantum Toolbox in Python). For additional documentation on this requirement, please see the [project page](http://qutip.org).

I recommend using [uv](https://docs.astral.sh/uv/) to manage your Python environment and install dependencies:

```
uv pip install qutip
```

Or with plain pip:

```
pip install "qutip>=5"
```
