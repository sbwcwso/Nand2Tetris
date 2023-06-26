#!/usr/bin/env python

import os
import subprocess
import unittest

from unittest.mock import mock_open, patch

from JackCompiler import JackTokenizer, CompilationEngine, JackAnalyzer

class TestJackTokenizer(unittest.TestCase):
    def test_preprocessor(self):
        inputs = [
            "  return True;   ",
            "// inline comment",
            "a = a + 1; // inline comment",
            "/**/",
            "/***/",
            "b = b +  1;   /* comment block */",
            "/** api comment */",
            "/* multiple comment block  ",
            "* multiple comment block  ",
            "* multiple comment block */  c = c + 1;",
            "/* multiple comment block */  d = d + 1;",
            "a=-1;"
        ]
        target_outputs = [
            "return True ;",
            "a = a + 1 ;",
            "b = b + 1 ;",
            "c = c + 1 ;",
            "d = d + 1 ;",
            "a = - 1 ;",
        ]
        self.assertListEqual(target_outputs, JackTokenizer.preprocessor(inputs))

    def test_tokenizer(self):
        """Write to xml file in the output directory and compare with the correct one"""
        jack_filepaths = [
            "./ArrayTest/Main.jack",
            "./ExpressionLessSquare",
            "./Square",
        ]
        for jack_filepath in jack_filepaths:
            JackAnalyzer(jack_filepath).test_tokenizer()

    def test_analyzer(self):
        jack_filepaths = [
            "./ArrayTest",
            "./ExpressionLessSquare",
            "./Square"
        ]
        for jack_filepath in jack_filepaths:
            JackAnalyzer(jack_filepath).generate_xml()
        

if __name__ == "__main__":
    unittest.main()
