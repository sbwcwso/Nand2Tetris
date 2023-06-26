#!/usr/bin/env python

import os
import subprocess
import unittest

from unittest.mock import mock_open, patch

from VMtranslator import Parser, VMtranslator


class TestParser(unittest.TestCase):
    def test_remove_extra_whitespace_comments(self):
        inputs = [
            "// comment",
            "//  comment",
            "//comment",
            "// comment  ",
            "add",
            " add",
            "  add",
            "add ",
            "add  ",
            "add// inline-comment",
            "add // inline-comment",
            "add // inline-comment",
            "push constant 10",
            "push   constant 10",
            "push   constant    10",
            "   label test  ",
            "if-goto label",
        ]
        target_outputs = [
            "",
            "",
            "",
            "",
            "add",
            "add",
            "add",
            "add",
            "add",
            "add",
            "add",
            "add",
            "push constant 10",
            "push constant 10",
            "push constant 10",
            "label test",
            "if-goto label",
        ]
        outputs = []
        for input in inputs:
            outputs.append(Parser.remove_extra_whitespace_comments(input))
        self.assertListEqual(target_outputs, outputs)

    def test_command_type(self):
        read_data = """\
add
sub
neg
eq
gt
lt
and
or
not
push constant 7
pop local 8
label loop
goto loop
if-goto symbol
function main 3
call main 3
return
"""
        real_command_types = [
            "C_ARITHMETIC",
            "C_ARITHMETIC",
            "C_ARITHMETIC",
            "C_ARITHMETIC",
            "C_ARITHMETIC",
            "C_ARITHMETIC",
            "C_ARITHMETIC",
            "C_ARITHMETIC",
            "C_ARITHMETIC",
            "C_PUSH",
            "C_POP",
            "C_LABEL",
            "C_GOTO",
            "C_IF",
            "C_FUNCTION",
            "C_CALL",
            "C_RETURN",
        ]
        with patch("builtins.open", new_callable=mock_open,
                   read_data=read_data):
            parser = Parser("test.txt")
            command_types = []
            while parser.has_more_commands():
                parser.advance()
                command_types.append(parser.command_type)
            self.assertListEqual(command_types, real_command_types)


class TestVMtranslator(unittest.TestCase):
    def test_run(self):
        vm_files_or_paths = [
            "../07/StackArithmetic/SimpleAdd/SimpleAdd.vm",
            "../07/StackArithmetic/StackTest",
            "../07/MemoryAccess/BasicTest/",
            "../07/MemoryAccess/PointerTest",
            "../07/MemoryAccess/StaticTest/StaticTest.vm",
            "./ProgramFlow/BasicLoop/BasicLoop.vm",
            "./ProgramFlow/FibonacciSeries/FibonacciSeries.vm",
            "./FunctionCalls/SimpleFunction/SimpleFunction.vm",
            "./FunctionCalls/NestedCall",
            "./FunctionCalls/FibonacciElement",
            "./FunctionCalls/StaticsTest",
        ]
        target_asm_files = [
            "../07/StackArithmetic/SimpleAdd/SimpleAdd.asm",
            "../07/StackArithmetic/StackTest/StackTest.asm",
            "../07/MemoryAccess/BasicTest/BasicTest.asm",
            "../07/MemoryAccess/PointerTest/PointerTest.asm",
            "../07/MemoryAccess/StaticTest/StaticTest.asm",
            "./ProgramFlow/BasicLoop/BasicLoop.asm",
            "./ProgramFlow/FibonacciSeries/FibonacciSeries.asm",
            "./FunctionCalls/SimpleFunction/SimpleFunction.asm",
            "./FunctionCalls/NestedCall/NestedCall.asm",
            "./FunctionCalls/FibonacciElement/FibonacciElement.asm",
            "./FunctionCalls/StaticsTest/StaticsTest.asm",
        ]
        tst_files = [
            "../07/StackArithmetic/SimpleAdd/SimpleAdd.tst",
            "../07/StackArithmetic/StackTest/StackTest.tst",
            "../07/MemoryAccess/BasicTest/BasicTest.tst",
            "../07/MemoryAccess/PointerTest/PointerTest.tst",
            "../07/MemoryAccess/StaticTest/StaticTest.tst",
            "./ProgramFlow/BasicLoop/BasicLoop.tst",
            "./ProgramFlow/FibonacciSeries/FibonacciSeries.tst",
            "./FunctionCalls/SimpleFunction/SimpleFunction.tst",
            "./FunctionCalls/NestedCall/NestedCall.tst",
            "./FunctionCalls/FibonacciElement/FibonacciElement.tst",
            "./FunctionCalls/StaticsTest/StaticsTest.tst",
        ]
        inits = [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
        ]

        for vm_file_or_path, target_asm_file, tst_file, init in zip(
                vm_files_or_paths, target_asm_files, tst_files, inits):
            try:
                os.remove(target_asm_file)
                print("Remove original {}".format(target_asm_file))
            except FileNotFoundError:
                pass
            VMtranslator(vm_file_or_path).run(init=init)
            command = "../../tools/CPUEmulator.sh  {}".format(tst_file)
            try:
                # 运行 shell 命令，并捕获输出结果
                subprocess.run(command, check=True, shell=True,
                               capture_output=True, text=True)
                print("{} Success".format(tst_file))
            except subprocess.CalledProcessError as e:
                # 打印命令运行失败的输出结果
                raise Exception("Error: {}".format(e.stderr))


if __name__ == "__main__":
    unittest.main()