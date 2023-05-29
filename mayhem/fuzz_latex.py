#!/usr/bin/env python3
import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports():
    from pylatexenc.latex2text import LatexNodes2Text
    from pylatexenc.latexencode import unicode_to_latex
    import pylatexenc.latexwalker

ctr = 0

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    text = fdp.ConsumeRemainingString()
    choice = fdp.ConsumeIntInRange(0, 3)
    global ctr
    ctr += 1
    try:
        if choice == 0:
            LatexNodes2Text().latex_to_text(text)
        elif choice == 1:
            pylatexenc.latexwalker(text)
        elif choice == 2:
            unicode_to_latex(text)
        else:
            pylatexenc.latexencode(text)
    except Exception:
        return -1
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
