#!/usr/bin/env python

import os
import sys


class Parser():
    """Parses the input."""

    def __init__(self, file_name: str):
        self.commands = []
        with open(file_name, encoding="utf-8") as f:
            for line in f.readlines():
                line = self.remove_whitespace_comments(line)
                if line:
                    self.commands.append(line)
        self.line = 0
        self.current_command = ""

    def has_more_commands(self) -> bool:
        return self.line < len(self.commands)

    def advance(self):
        "Update current command."
        assert self.has_more_commands()
        self.current_command = self.commands[self.line]
        self.line += 1

    def reset(self):
        "Reset to the first command."
        self.line = 0

    def command_type(self):
        "Return the type of current command."
        buffer = ""
        self.dest = ""
        self.comp = ""
        self.jump = ""
        self.symbol = ""
        jump_exist = False
        if self.current_command.startswith("@"):
            self.symbol = self.current_command[1:]
            return "A_COMMAND"
        for i in range(len(self.current_command)):
            if self.current_command[i] == "=":
                self.dest = buffer if buffer else None
                buffer = ""
            elif self.current_command[i] == ";":
                self.comp = buffer if buffer else None
                buffer = ""
                jump_exist = True
            else:
                buffer += self.current_command[i]
        if jump_exist:
            self.jump = buffer if buffer else None
        else:
            self.comp = buffer if buffer else None
        if self.dest in Code.DEST.keys() and \
                self.comp in Code.COMP.keys() and \
                self.jump in Code.JUMP.keys():
            return "C_COMMAND"
        if self.current_command[0] == "(" and self.current_command[-1] == ")":
            self.symbol = self.current_command[1:-1]
            return "L_COMMAND"
        raise Exception("{} is not a valid command, {}, {}, {}, {}".format(self.current_command,
                                                                           self.dest,
                                                                           self.comp,
                                                                           self.jump,
                                                                           self.symbol))

    @staticmethod
    def remove_whitespace_comments(line: str) -> str:
        res = ""
        for i in range(len(line)):
            if line[i].isspace():
                continue
            if line[i:i+2] == "//":
                break
            res += line[i]
        return res


class Code():
    """Provide the binary codes of all the assembly mnemonics."""
    DEST = {
        "":     "000",
        "M":    "001",
        "D":    "010",
        "MD":   "011",
        "A":    "100",
        "AM":   "101",
        "AD":   "110",
        "AMD":  "111",
    }

    JUMP = {
        "":     "000",
        "JGT":  "001",
        "JEQ":  "010",
        "JGE":  "011",
        "JLT":  "100",
        "JNE":  "101",
        "JLE":  "110",
        "JMP":  "111",
    }

    COMP = {
        "0":    "0101010",
        "1":    "0111111",
        "-1":   "0111010",
        "D":    "0001100",
        "A":    "0110000",
        "M":    "1110000",
        "!D":   "0001101",
        "!A":   "0110001",
        "!M":   "1110001",
        "-D":   "0001111",
        "-A":   "0110011",
        "-M":   "1110011",
        "D+1":  "0011111",
        "A+1":  "0110111",
        "M+1":  "1110111",
        "D-1":  "0001110",
        "A-1":  "0110010",
        "M-1":  "1110010",
        "D+A":  "0000010",
        "D+M":  "1000010",
        "D-A":  "0010011",
        "D-M":  "1010011",
        "A-D":  "0000111",
        "M-D":  "1000111",
        "D&A":  "0000000",
        "D&M":  "1000000",
        "D|A":  "0010101",
        "D|M":  "1010101",
    }


SymbolTablePreDefined = {
    "SP":       0,
    "LCL":      1,
    "ARG":      2,
    "THIS":     3,
    "THAT":     4,
    "R0":       0,
    "R1":       1,
    "R2":       2,
    "R3":       3,
    "R4":       4,
    "R5":       5,
    "R6":       6,
    "R7":       7,
    "R8":       8,
    "R9":       9,
    "R10":      10,
    "R11":      11,
    "R12":      12,
    "R13":      13,
    "R14":      14,
    "R15":      15,
    "SCREEN":   16384,
    "KBD":      24576,
}


class AssemblerNoSymbols():
    def __init__(self, asm_file: str):
        self.hack_file = os.path.join(os.path.splitext(asm_file)[0] + ".hack")
        self.parse = Parser(asm_file)
        self.hack_content = ""

    def translate(self):
        while self.parse.has_more_commands():
            command = ""
            self.parse.advance()
            command_type = self.parse.command_type()
            assert command_type != "L_COMMAND"
            if command_type == "A_COMMAND":
                assert self.parse.symbol.isdigit()
                command = "0" + bin(int(self.parse.symbol))[2:].zfill(15)[-15:]
            else:
                command = "111" + \
                    Code.COMP[self.parse.comp] + \
                    Code.DEST[self.parse.dest] + Code.JUMP[self.parse.jump]
            self.hack_content += command + "\n"

    def write_to_hack_file(self):
        with open(self.hack_file, "w", encoding="utf-8",) as f:
            f.write(self.hack_content)

    def run(self):
        self.translate()
        self.write_to_hack_file()


class Assembler(AssemblerNoSymbols):
    def __init__(self, asm_file: str):
        super().__init__(asm_file)
        self.SymbolTable = SymbolTablePreDefined.copy()

    def first_pass(self):
        address = 0
        while self.parse.has_more_commands():
            self.parse.advance()
            if self.parse.command_type() == "L_COMMAND":
                assert self.parse.symbol not in self.SymbolTable
                self.SymbolTable[self.parse.symbol] = address
            else:
                address = address + 1
        self.parse.reset()

    def second_pass(self):
        next_data_address = 16
        while self.parse.has_more_commands():
            command = ""
            self.parse.advance()
            command_type = self.parse.command_type()
            if command_type == "L_COMMAND":
                continue
            if command_type == "A_COMMAND":
                if self.parse.symbol.isdigit():
                    value = int(self.parse.symbol)
                else:
                    if self.parse.symbol in self.SymbolTable:
                        value = self.SymbolTable[self.parse.symbol]
                    else:
                        value = next_data_address
                        self.SymbolTable[self.parse.symbol] = next_data_address
                        next_data_address += 1
                command = "0" + bin(value)[2:].zfill(15)[-15:]
            else:
                command = "111" + \
                    Code.COMP[self.parse.comp] + \
                    Code.DEST[self.parse.dest] + Code.JUMP[self.parse.jump]
            self.hack_content += command + "\n"

    def translate(self):
        self.first_pass()
        self.second_pass()


if __name__ == "__main__":
    Assembler(sys.argv[1]).run()
