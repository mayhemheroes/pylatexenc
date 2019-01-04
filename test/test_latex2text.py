
from __future__ import unicode_literals, print_function

import unittest

import re


from pylatexenc.latexwalker import LatexWalker
from pylatexenc.latex2text import LatexNodes2Text


class TestLatexNodes2Text(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestLatexNodes2Text, self).__init__(*args, **kwargs)
        self.maxDiff = None
    
    def test_basic(self):

        self.assertEqual(
            LatexNodes2Text().nodelist_to_text(LatexWalker(r'\textbf{A}').get_latex_nodes()[0]),
            'A'
        )

        latex = r'''\textit{hi there!} This is {\em an equation}:
\begin{equation}
    x + y i = 0
\end{equation}

where $i$ is the imaginary unit.
'''
        self.assertEqualUpToWhitespace(
            LatexNodes2Text().nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            r'''hi there! This is an equation:

    x + y i = 0

where i is the imaginary unit.
'''
        )
        self.assertEqualUpToWhitespace(
            LatexNodes2Text(keep_inline_math=True).nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            r'''hi there! This is an equation:

    x + y i = 0

where $i$ is the imaginary unit.
'''
        )

        self.assertEqual(
            LatexNodes2Text().nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            LatexNodes2Text().latex_to_text(latex)
        )
        
    def test_accents(self):
        self.assertEqual(
            LatexNodes2Text().nodelist_to_text(LatexWalker(r"Fran\c cais").get_latex_nodes()[0]),
            '''Fran\N{LATIN SMALL LETTER C WITH CEDILLA}ais'''
        )
        self.assertEqual(
            LatexNodes2Text().nodelist_to_text(LatexWalker(r"Fr\'en{\'{e}}tique").get_latex_nodes()[0]),
            '''Fr\N{LATIN SMALL LETTER E WITH ACUTE}n\N{LATIN SMALL LETTER E WITH ACUTE}tique'''
        )
        

    def test_keep_braced_groups(self):
        self.assertEqual(
            LatexNodes2Text(keep_braced_groups=True)
            .nodelist_to_text(LatexWalker(r"\textit{Voil\`a du texte}. Il est \'{e}crit {en fran{\c{c}}ais}")
                              .get_latex_nodes()[0]),
            '''Voil\N{LATIN SMALL LETTER A WITH GRAVE} du texte. Il est \N{LATIN SMALL LETTER E WITH ACUTE}crit {en fran\N{LATIN SMALL LETTER C WITH CEDILLA}ais}'''
        )

        self.assertEqual(
            LatexNodes2Text(keep_braced_groups=True, keep_braced_groups_minlen=4)
            .nodelist_to_text(LatexWalker(r"A{XYZ}{ABCD}").get_latex_nodes()[0]),
            '''AXYZ{ABCD}'''
        )
        self.assertEqual(
            LatexNodes2Text(keep_braced_groups=True, keep_braced_groups_minlen=0)
            .nodelist_to_text(LatexWalker(r"{A}{XYZ}{ABCD}").get_latex_nodes()[0]),
            '''{A}{XYZ}{ABCD}'''
        )


    def test_input(self):
        latex = r'''ABCDEF fdksanfkld safnkd anfklsa

\input{test_input_1.tex}

MORENKFDNSN'''
        correct_text = r'''ABCDEF fdksanfkld safnkd anfklsa

hi there! This is an equation:

    x + y i = 0

where i is the imaginary unit.

MORENKFDNSN'''

        l2t = LatexNodes2Text()
        l2t.set_tex_input_directory('.')

        self.assertEqualUpToWhitespace(
            l2t.nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            correct_text
        )

        latex = r'''ABCDEF fdksanfkld safnkd anfklsa

\input{test_input_1}

MORENKFDNSN'''

        self.assertEqualUpToWhitespace(
            l2t.nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            correct_text
        )

        latex = r'''ABCDEF fdksanfkld safnkd anfklsa

\input{../test_input_1}

MORENKFDNSN'''

        correct_text_unsafe = correct_text # as before
        correct_text_safe = r'''ABCDEF fdksanfkld safnkd anfklsa

MORENKFDNSN'''

        # make sure that the \input{} directive failed to include the file.
        l2t = LatexNodes2Text()
        l2t.set_tex_input_directory('./dummy')
        self.assertEqualUpToWhitespace(
            l2t.nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            correct_text_safe
        )
        # but without the strict_input flag, it can access it.
        l2t.set_tex_input_directory('./dummy', strict_input=False)
        self.assertEqualUpToWhitespace(
            l2t.nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            correct_text_unsafe
        )




    def assertEqualUpToWhitespace(self, a, b):
        a2 = re.sub(r'\s+', ' ', a).strip()
        b2 = re.sub(r'\s+', ' ', b).strip()
        self.assertEqual(a2, b2)




if __name__ == '__main__':
    unittest.main()
#

