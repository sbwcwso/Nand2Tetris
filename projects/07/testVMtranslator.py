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
            "./StackArithmetic/SimpleAdd/SimpleAdd.vm",
            "./StackArithmetic/StackTest",
            "./MemoryAccess/BasicTest/",
            "./MemoryAccess/PointerTest",
            "./MemoryAccess/StaticTest/StaticTest.vm",
        ]
        target_asm_files = [
            "./StackArithmetic/SimpleAdd/SimpleAdd.asm",
            "./StackArithmetic/StackTest/StackTest.asm",
            "./MemoryAccess/BasicTest/BasicTest.asm",
            "./MemoryAccess/PointerTest/PointerTest.asm",
            "./MemoryAccess/StaticTest/StaticTest.asm",
        ]
        tst_files = [
            "./StackArithmetic/SimpleAdd/SimpleAdd.tst",
            "./StackArithmetic/StackTest/StackTest.tst",
            "./MemoryAccess/BasicTest/BasicTest.tst",
            "./MemoryAccess/PointerTest/PointerTest.tst",
            "./MemoryAccess/StaticTest/StaticTest.tst",
        ]

        for vm_file_or_path, target_asm_file, tst_file in zip(
                vm_files_or_paths, target_asm_files, tst_files):
            try:
                os.remove(target_asm_file)
                print("Remove original {}".format(target_asm_file))
            except FileNotFoundError:
                pass
            VMtranslator(vm_file_or_path).run()
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