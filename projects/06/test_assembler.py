#!/usr/bin/env python

import filecmp
import os
import unittest

from assembler import Parser, AssemblerNoSymbols, Assembler
from unittest.mock import mock_open, patch


class TestParser(unittest.TestCase):
    # def test_remove_whitespace_comment(self):
    #     lines = [
    #         "// Computes R2 = max(R0, R1)",
    #         "@R0",
    #         "  D=M              // D = first number",
    #         " @R1 ",
    #         "D=D-M            // D = first number - second number",
    #         "",
    #     ]
    #     results = [
    #         "",
    #         "@R0",
    #         "D=M",
    #         "@R1",
    #         "D=D-M",
    #         "",
    #     ]
    #     for line, result in zip(lines, results):
    #         self.assertEqual(Parser.remove_whitespace_comments(line), result)

    read_data = """\
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/06/max/Max.asm

// Computes R2 = max(R0, R1)  (R0,R1,R2 refer to RAM[0],RAM[1],RAM[2])

   @R0
   D=M              // D = first number
   @R1
   D=D-M            // D = first number - second number
   @OUTPUT_FIRST
   D;JGT            // if D>0 (first is greater) goto output_first
   @R1
   D=M              // D = second number
   @OUTPUT_D
   0;JMP            // goto output_d
(OUTPUT_FIRST)
   @R0
   D=M              // D = first number
(OUTPUT_D)
   @R2
   M=D              // M[2] = D (greatest number)
 (INFINITE_LOOP)
   @INFINITE_LOOP  
   0;JMP            // infinite loop
"""

    commands = [
        "@R0",
        "D=M",
        "@R1",
        "D=D-M",
        "@OUTPUT_FIRST",
        "D;JGT",
        "@R1",
        "D=M",
        "@OUTPUT_D",
        "0;JMP",
        "(OUTPUT_FIRST)",
        "@R0",
        "D=M",
        "(OUTPUT_D)",
        "@R2",
        "M=D",
        "(INFINITE_LOOP)",
        "@INFINITE_LOOP",
        "0;JMP",
    ]

    command_types = [
        "A_COMMAND",
        "C_COMMAND",
        "A_COMMAND",
        "C_COMMAND",
        "A_COMMAND",
        "C_COMMAND",
        "A_COMMAND",
        "C_COMMAND",
        "A_COMMAND",
        "C_COMMAND",
        "L_COMMAND",
        "A_COMMAND",
        "C_COMMAND",
        "L_COMMAND",
        "A_COMMAND",
        "C_COMMAND",
        "L_COMMAND",
        "A_COMMAND",
        "C_COMMAND",
    ]

    def test_remove_whitespace_comment(self):
        with patch("builtins.open", new_callable=mock_open, read_data=self.read_data) as mock_file:
            parser = Parser("test.txt")
            self.assertListEqual(parser.commands, self.commands)

    def test_command_type(self):
        with patch("builtins.open", new_callable=mock_open, read_data=self.read_data) as mock_file:
            parser = Parser("test.txt")
            command_types = []
            while parser.has_more_commands():
                parser.advance()
                command_types.append(parser.command_type())
            self.assertListEqual(command_types, self.command_types)


class TestAssemblerNoSymbols(unittest.TestCase):
    def test_assembler_no_symbols(self):
        asm_files = ["./add/Add.asm", "./max/MaxL.asm", "./pong/PongL.asm"]
        target_hack_files = ["./add/Add.hack",
                             "./max/MaxL.hack", "./pong/PongL.hack"]
        correct_hack_files = ["./add/Add_correct.hack",
                              "./max/MaxL_correct.hack", "./pong/PongL_correct.hack"]
        for asm_file, target_hack_file, correct_hack_file in zip(asm_files, target_hack_files, correct_hack_files):
            try:
                os.remove(target_hack_file)
            except FileNotFoundError:
                pass
            AssemblerNoSymbols(asm_file).run()
            self.assertTrue(filecmp.cmp(target_hack_file, correct_hack_file))


class TestAssembler(unittest.TestCase):
    def test_assembler(self):
        asm_files = [
            "./add/Add.asm",
            "./max/MaxL.asm",
            "./max/Max.asm",
            "./pong/PongL.asm",
            "./pong/Pong.asm",
            "./rect/RectL.asm",
            "./rect/Rect.asm",
        ]
        target_hack_files = [
            "./add/Add.hack",
            "./max/MaxL.hack",
            "./max/Max.hack",
            "./pong/PongL.hack",
            "./pong/Pong.hack",
            "./rect/RectL.hack",
            "./rect/Rect.hack",
        ]
        correct_hack_files = [
            "./add/Add_correct.hack",
            "./max/MaxL_correct.hack",
            "./max/Max_correct.hack",
            "./pong/PongL_correct.hack",
            "./pong/Pong_correct.hack",
            "./rect/RectL_correct.hack",
            "./rect/Rect_correct.hack",
        ]
        for asm_file, target_hack_file, correct_hack_file in zip(asm_files, target_hack_files, correct_hack_files):
            try:
                os.remove(target_hack_file)
            except FileNotFoundError:
                pass
            Assembler(asm_file).run()
            self.assertTrue(filecmp.cmp(target_hack_file, correct_hack_file))


if __name__ == "__main__":
    unittest.main()
