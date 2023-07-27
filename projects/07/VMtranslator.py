#!/usr/bin/env python

import os
import sys


UnaryOperatorAsm = """\
// {command}
    @SP
    M = M - 1
    A = M
    {asm_command} // push ({command} y)
    @SP
    M = M + 1
"""

BinaryOperatorAsm = """\
// {command}
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    {asm_command}  // push (M[x] {command} D[y])
    @SP
    M = M + 1
"""

CompareOperatorAsm = """\
// {command}
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    D = M - D 	    // M = x, D = y, D = x - y
    @SP             // push true(-1) or false(0)
    A = M
    M = -1          // push true
    @{label_true}
    {jump_command}
    @SP
    A = M
    M = 0         // push false
    @SP      	   // lable_true
    M = M + 1
"""

PushConstantAsm = """\
// {command}
    @{int_number}
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
"""

MemorySegmentBase = {
    "local":    "LCL",
    "argument": "ARG",
    "this":     "THIS",
    "that":     "THAT",
}

PushMemorySegmentAsm = """\
// {command}
    @{index}
    D = A
    @{base_label}
    A = D + M
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
"""

PopMemorySegmentAsm = """\
// {command}
    @{index}  // address = segment + index
    D = A
    @{base_label}
    D = D + M
    @R13
    M = D
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @R13  // RAM[address] = data
    A = M
    M = D
"""

PushTempSegmentAsm = """\
// {command}
    @{index}
    D = A
    @5
    A = D + A
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
"""

PopTempSegmentAsm = """\
// {command}
    @{index}  // address = 5 + index
    D = A
    @5
    D = D + A
    @R13 
    M = D
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @R13
    A = M
    M = D
"""

PushPointStaticSegmentAsm = """\
// {command}
    @{memory_index}
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
"""

PopPointStaticSegmentAsm = """\
// {command}
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @{memory_index}
    M = D
"""

ArithmeticCommands = {
    "neg": 	"M = -M",
    "not": 	"M = !M",
    "add": 	"M = D + M",
    "sub": 	"M = M - D",
    "and": 	"M = D & M",
    "or":  	"M = D | M",
    "eq":  	"D;JEQ",
    "gt":  	"D;JGT",
    "lt":  	"D;JLT",
}

NoArgCommands = {
    "return": "C_RETURN",
}

NoArgCommands.update(dict.fromkeys(ArithmeticCommands.keys(), "C_ARITHMETIC"))

OneArgCommands = {
    "label": 	 "C_LABEL",
    "goto": 	 "C_GOTO",
    "if-goto": 	 "C_IF",
}

TwoArgCommands = {
    "push":			"C_PUSH",
    "pop":			"C_POP",
    "function":	 	"C_FUNCTION",
    "call":		 	"C_CALL",
}


class Parser():
    """Handles the parsing of single .vm file"""
    def __init__(self, vm_file: str) -> None:
        self.commands = []
        with open(vm_file, encoding="utf-8") as f:
            for line in f.readlines():
                line = self.remove_extra_whitespace_comments(line)
                if line:
                    self.commands.append(line)
        self.line = 0
        self.current_command = ""
        self._command_type = None

    def has_more_commands(self) -> bool:
        return self.line < len(self.commands)

    def advance(self):
        """Update current command."""
        assert self.has_more_commands()
        self.current_command = self.commands[self.line]
        self.line += 1
        self._parse_current_command()

    @property
    def command_type(self):
        """Returns the types of current VM command."""
        assert self._command_type is not None
        return self._command_type

    @property
    def arg1(self):
        """
        Returns the first argument of the current command.
        In the case of C_ARITHMETIC, the command itself is returned
        """
        assert self._command_type != "C_RETURN", "C_RETURN doesn't have arg1."
        return self._arg1

    @property
    def arg2(self):
        """
        Returns the second argument of the current command.
        """
        assert self._command_type in TwoArgCommands.values()
        return self._arg2

    def _parse_current_command(self):
        """Confirm current command's type and corresponding args."""
        # Get items split by blank in the current command
        items = self.current_command.split(" ")
        self._command_type = None
        if len(items) == 1:
            self._command = items[0]
            self._arg1 = items[0]
            self._command_type = NoArgCommands.get(self._command, None)
        elif len(items) == 2:
            self._command = items[0]
            self._arg1 = items[1]
            self._command_type = OneArgCommands.get(self._command, None)
        elif len(items) == 3:
            self._command = items[0]
            self._arg1 = items[1]
            self._arg2 = items[2]
            self._command_type = TwoArgCommands.get(self._command, None)

        if self._command_type in ["C_PUSH", "C_POP"]:
            assert self._arg1 in ["argument", "local", "static",
                                  "constant", "this", "that",
                                  "pointer", "temp"], \
                    "Illegal command {}: illegal segment {}!".format(
                        self.current_command, self._arg1)
            assert self._arg2.isdecimal(), \
                "Illegal command {}: {} is not a int number".format(
                    self.current_command, self._arg2)
            if self._arg1 == "tmp":
                assert 0 <= int(self._arg2) <= 7, \
                    "temp index {} error".format(self._arg2)
            assert not (
                self._command_type == "C_POP" and self._arg1 == "constant"),\
                "Illegal command {}".format(self.current_command)
        elif self._command_type in ["C_FUNCTION", "C_CALL"]:
            assert self._arg2.isdecimal(), \
                "Illegal command {}: {} is not a int number".format(
                    self.current_command, self._arg2)

        elif self._command_type is None:
            raise Exception(
                "Illegal command: {} !".format(self.current_command))

    @staticmethod
    def remove_extra_whitespace_comments(line: str) -> str:
        res = ""
        for i in range(len(line)):
            if line[i].isspace() and i + 1 < len(line) and line[i+1].isspace():
                # Remove the extra space
                continue
            if line[i:i+2] == "//":
                break
            res += line[i]
        return res.strip()


class CodeWriter():
    """Translate VM commands into Hack assembly code."""
    def __init__(self, asm_file):
        self.fd = open(asm_file, "w")
        self.command_nums = 0

    def set_file_name(self, vm_file):
        self.file_name = os.path.basename(os.path.splitext(vm_file)[0])
        self.static_index = 0

    def write_arithmetic(self, command: str):
        """
        Writes the assembly code that is the translation of the given
        arithmetic command.
        """
        if command in ["neg", "not"]:
            self.fd.write(UnaryOperatorAsm.format(
                command=command,
                asm_command=ArithmeticCommands[command]))
            self.command_nums += 6
        elif command in ["add", "sub", "and", "or"]:
            self.fd.write(BinaryOperatorAsm.format(
                command=command, asm_command=ArithmeticCommands[command]))
            self.command_nums += 12
        elif command in ["eq", "gt", "lt"]:
            self.fd.write(CompareOperatorAsm.format(
                command=command,
                label_true=self.command_nums + 18,
                jump_command=ArithmeticCommands[command]))
            self.command_nums += 20

    def write_push_pop(self, command: str, segment: str, index: int):
        """
        Writes the assembly code that is the translation of the given command,
        where command is either C_PUSH or C_POP
        """
        if command == "C_PUSH":
            command = "push " + segment + " " + str(index)
            if segment == "constant":  # push constant
                self.fd.write(PushConstantAsm.format(
                    command=command,
                    int_number=index))
                self.command_nums += 7
            elif segment in ["argument", "local", "this", "that"]:
                self.fd.write(PushMemorySegmentAsm.format(
                    command=command,
                    index=index,
                    base_label=MemorySegmentBase[segment]))
                self.command_nums += 10
            elif segment == "temp":
                self.fd.write(PushTempSegmentAsm.format(
                    command=command,
                    index=index))
                self.command_nums += 10
            elif segment == "pointer":
                self.fd.write(PushPointStaticSegmentAsm.format(
                    command=command,
                    memory_index=index+3))
                self.command_nums += 7
            elif segment == "static":
                self.fd.write(PushPointStaticSegmentAsm.format(
                    command=command,
                    memory_index="{}.{}".format(self.file_name, index)))
                self.command_nums += 7
        elif command == "C_POP":
            command = "pop " + segment + " " + str(index)
            if segment in ["argument", "local", "this", "that"]:
                self.fd.write(PopMemorySegmentAsm.format(
                    command=command,
                    index=index,
                    base_label=MemorySegmentBase[segment]))
                self.command_nums += 13
            elif segment == "temp":
                self.fd.write(PopTempSegmentAsm.format(
                    command=command,
                    index=index))
                self.command_nums += 13
            elif segment == "pointer":
                self.fd.write(PopPointStaticSegmentAsm.format(
                    command=command,
                    memory_index=index+3))
                self.command_nums += 6
            elif segment == "static":
                self.fd.write(PopPointStaticSegmentAsm.format(
                    command=command,
                    memory_index="{}.{}".format(self.file_name, index)))
                self.command_nums += 6
        else:
            assert False, "Not support command type {}".format(command)

    def close(self):
        """Close the output file."""
        self.fd.close()


class VMtranslator():
    def __init__(self, vm_file_or_path: str):
        self.vm_files = []
        if os.path.isfile(vm_file_or_path):
            assert os.path.splitext(vm_file_or_path)[1] == ".vm"
            self.vm_files = [vm_file_or_path]
            self.asm_file_name = os.path.join(
                os.path.splitext(vm_file_or_path)[0] + ".asm")
        elif os.path.isdir(vm_file_or_path):
            vm_file_or_path = vm_file_or_path.rstrip(os.path.sep)
            self.vm_files = [os.path.join(vm_file_or_path, file)
                             for file in os.listdir(vm_file_or_path)
                             if file.endswith(".vm")]
            self.asm_file_name = os.path.join(
                vm_file_or_path, os.path.basename(vm_file_or_path) + ".asm")
        else:
            raise Exception("Must input a vm file or a directory.")
        assert self.vm_files

    def run(self):
        code_writer = CodeWriter(self.asm_file_name)
        for vm_file in self.vm_files:
            code_writer.set_file_name(vm_file)
            parser = Parser(vm_file)
            while parser.has_more_commands():
                parser.advance()
                if parser.command_type == "C_ARITHMETIC":
                    code_writer.write_arithmetic(parser.arg1)
                elif parser.command_type in ["C_PUSH", "C_POP"]:
                    code_writer.write_push_pop(parser.command_type,
                                               parser.arg1, int(parser.arg2))
        code_writer.close()


if __name__ == "__main__":
    VMtranslator(sys.argv[1]).run()
