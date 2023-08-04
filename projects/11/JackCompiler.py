#!/usr/bin/env python

import os
import re
import sys
import subprocess

from enum import Enum

from typing import Dict, IO, List, NamedTuple, Tuple, Union, Iterable


class Segment(Enum):
    """The VM segments."""
    CONSTANT =  "constant"
    ARGUMENT = "argument"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"


class Arithmetic(Enum):
    """The arithmetic commands"""
    ADD = "add"
    SUB = "sub"
    AND = "and"
    OR = "or"
    LT = "lt"
    GT = "gt"
    EQ = "eq"
    NEG = "neg"
    NOT = "not"


class VarKind(Enum):
    """The variable type."""
    STATIC = Segment.STATIC
    FIELD = Segment.THIS
    ARGUMENT = Segment.ARGUMENT
    VAR = Segment.LOCAL


class JackTokenizer():
    """A tokenizer.

    The tokenizer removes all comments and white space from the input stream and breaks it into Jack-
    language tokens, as specified in the Jack grammar.
    """

    Keywords = [
        "class", "constructor", "function", "method", "field", "static", "var",
        "int", "char", "boolean", "void", "true", "false", "null", "this",
        "let", "do", "if", "else", "while", "return"
    ]

    Symbols = [
        "{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&",
        "|", "<", ">", "=", "~"
    ]

    def __init__(self, jack_file: IO) -> None:
        """Opens the input file/stream and gets ready to tokenize it"""
        self.original_lines = list(jack_file.readlines())
        self.lines = JackTokenizer.preprocessor(self.original_lines)
        self.line_nums = len(self.lines)
        self.current_line_number = 0
        self.current_line_index = 0
        self.current_line_length = len(
            self.lines[0]) if self.line_nums > 0 else 0
        self.current_line = self.lines[0] if self.line_nums > 0 else []
        self.cur_token = ""
        self._cur_token_type = ""
        self._keyword = ""
        self._symbol = ""
        self._identifier = ""
        self._int_val = 0
        self._string_val = ""

    def has_more_tokens(self) -> bool:
        """Check if there is more tokens in the input."""
        return self.current_line_number < self.line_nums

    @property
    def _current_char(self) -> str:
        return self.current_line[self.current_line_index]

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.

        This method should only be called if hasMoreTokens() is true.
        Initially there is no current token..
        """
        assert self.has_more_tokens()
        if self._current_char in self.Symbols:
            self._cur_token_type = "symbol"
            self._symbol = self._current_char
            self.current_line_index += 1
        elif self._current_char == "\"":
            self._cur_token_type = "stringConstant"
            self._string_val = ""
            self.current_line_index += 1
            while self.current_line_index < self.current_line_length:
                if self._current_char != "\"":
                    self._string_val += self._current_char
                    self.current_line_index += 1
                else:
                    self.current_line_index += 1
                    break
            else:
                raise Exception("String mismatch!")
        else:  # get token
            cur_token = ""
            while self._current_char != " ":
                cur_token += self._current_char
                self.current_line_index += 1
            if cur_token in self.Keywords:
                self._cur_token_type = "keyword"
                self._keyword = cur_token
            elif cur_token.isdecimal():
                self._cur_token_type = "integerConstant"
                self._int_val = int(cur_token)
            else:
                assert re.match(r'^[a-zA-Z_][\w]*$', cur_token),\
                    "{} is not a valid identifier!".format(cur_token)
                self._cur_token_type = "identifier"
                self._identifier = cur_token

        # eat the extra space
        while self.current_line_index < self.current_line_length and self._current_char == " ":
            self.current_line_index += 1

        if self.current_line_index >= self.current_line_length:
            self.current_line_number += 1
            self.current_line_index = 0
            if self.current_line_number < self.line_nums:
                self.current_line = self.lines[self.current_line_number]
                self.current_line_length = len(self.current_line)

    @property
    def token_type(self) -> str:
        """Return the type of the current token."""
        return self._cur_token_type

    @property
    def keyword(self) -> str:
        """Returns the keyword which is the current token.

        Should be called only when self.tokenType() is KEYWORD.
        """
        assert self.token_type == "keyword"
        return self._keyword

    @property
    def symbol(self) -> str:
        """Return the character which is the current token.

        Should be called only when self.tokenType() is SYMBOL
        """
        assert self.token_type == "symbol"
        return self._symbol

    @property
    def identifier(self) -> str:
        """Return the identifier which is the current token.

        Should be called only when self.tokenType() is IDENTIFIER
        """
        assert self.token_type == "identifier"
        return self._identifier

    @property
    def int_val(self) -> int:
        """Return the integar value of the current token.

        Should be called only when self.tokenType() is INT_CONST
        """
        assert self.token_type == "integerConstant"
        return self._int_val

    @property
    def string_val(self) -> str:
        """Return the string value of the current token, without the double quotes.

        Should be called only when self.tokenType() is STRING_CONST
        """
        assert self.token_type == "stringConstant"
        return self._string_val

    @staticmethod
    def preprocessor(original_lines: List[str]) -> List[str]:
        """Remove extra space and comments.

        Make sure there is a space around the symbol.
        """
        line_num = 0
        lines = []
        is_inside_comment = False  # is inside the comment of /* */ or /** /
        is_inside_string = False
        total_lines = len(original_lines)
        while line_num < total_lines:
            cur_line = original_lines[line_num]
            line = ""
            cur_line_length = len(cur_line)
            i = 0
            while i < cur_line_length:
                if is_inside_comment is False and is_inside_string is False:
                    if cur_line[i].isspace():
                        if line and line[-1] != " ":
                            line += " "
                        i += 1
                    elif cur_line[i:i + 2] == "//":
                        break
                    elif cur_line[i] == "/" and i + 1 < len(
                            cur_line) and cur_line[i + 1] == "*":
                        is_inside_comment = True
                        i += 2
                    elif cur_line[i] == "\"":
                        is_inside_string = True
                        line += cur_line[i]
                        i += 1
                    elif cur_line[i] in JackTokenizer.Symbols:
                        if line and line[-1] != " ":
                            line += " "
                        line += cur_line[i] + " "
                        i += 1
                    else:
                        line += cur_line[i]
                        i += 1
                elif is_inside_comment is True:
                    if cur_line[i] == "*" and i + 1 < len(
                            cur_line) and cur_line[i + 1] == "/":
                        is_inside_comment = False
                        i += 2
                    else:
                        i += 1
                elif is_inside_string is True:
                    if cur_line[i] == "\"":
                        is_inside_string = False
                    line += cur_line[i]
                    i += 1

            line = line.strip()
            if line: lines.append(line)
            line_num += 1

        return lines


class SymbolTable():
    """Implement SymbolTable."""

    class SymbolItem(NamedTuple):
        """The item in the symbol table."""
        type: str
        kind: VarKind
        index: int

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """Reset the symbol table."""
        self.items: Dict[str, SymbolTable.SymbolItem] = {}
        self.indexes = {
            VarKind.STATIC: 0,
            VarKind.VAR: 0,
            VarKind.FIELD: 0,
            VarKind.ARGUMENT: 0
        }

    def get_varkind_nums(self, varkind: VarKind) -> int:
        """Return the total nums of the given varkind"""
        return self.indexes[varkind]

    def define(self, name: str, type: str, kind: VarKind)-> None:
        """Define(adds to the table) a new variable of the given name."""
        assert name not in self.items
        self.items[name] = SymbolTable.SymbolItem(
            type,
            kind,
            self.indexes[kind]
        )
        self.indexes[kind] += 1

    def __contains__(self, el: str) -> bool:
        return el in self.items

    def kind_of(self, name: str) -> Union[VarKind, None]:
        """Return the kind of the named identifier.

        If the identifier is not found, returns None.
        """
        item = self.items.get(name, None)
        return None if item is None else item.kind

    def type_of(self, name: str) -> Union[str, None]:
        """Return the type of the named identifier.

        If the identifier is not found, returns None.
        """
        item = self.items.get(name, None)
        return None if item is None else item.type

    def index_of(self, name: str) -> Union[int, None]:
        """Return the index of the named identifier.

        If the identifier is not found, returns None.
        """
        item = self.items.get(name, None)
        return None if item is None else item.index


class VMWriter():
    "A simple module that writes individual VM commands to the output .vm file."

    def __init__(self, output_stream: IO):
        self.stream = output_stream

    def write_push(self, segment: Segment, index: int) -> None:
        """Writes a VM push command."""
        self.stream.write("push {} {}\n".format(segment.value, index))

    def write_pop(self, segment: Segment, index: int) -> None:
        """Writes a VM pop command."""
        self.stream.write("pop {} {}\n".format(segment.value, index))

    def write_arithmetic(self, command: Arithmetic) -> None:
        """Writes a VM arithmetic-logical command."""
        self.stream.write("{}\n".format(command.value))

    def write_label(self, label_name: str) -> None:
        """Writes a VM label command."""
        self.stream.write("label {}\n".format(label_name))

    def write_goto(self, label_name: str) -> None:
        """Writes a VM goto command."""
        self.stream.write("goto {}\n".format(label_name))

    def write_if(self, label_name: str) -> None:
        """Writes a VM if-goto command"""
        self.stream.write("if-goto {}\n".format(label_name))

    def write_call(self, name: str, var_nums: int) -> None:
        """Writes a VM call command."""
        self.stream.write("call {} {}\n".format(name, var_nums))

    def write_function(self, name: str, n_vars: int) -> None:
        """Writes a VM function command."""
        self.stream.write("function {} {}\n".format(name, n_vars))

    def write_return(self) -> None:
        """Writes a VM return command."""
        self.stream.write("return\n");

    def write_keyword_constant(self, keyword_constant: str) -> None:
        """Writes a given VM keyword constant."""
        if keyword_constant == "true":
            self.write_push(Segment.CONSTANT, 0)
            self.write_arithmetic(Arithmetic.NOT)
        elif keyword_constant == "false" or keyword_constant == "null":
            self.write_push(Segment.CONSTANT, 0)
        elif keyword_constant == "this":  # TODO need to be make sure
            self.write_push(Segment.POINTER, 0)
        else:
            raise Exception("No handle program for {}.".format(keyword_constant))

    def write_string_constant(self, string: str) -> None:
        """Writes a given StringConstant"""
        self.write_push(Segment.CONSTANT, len(string))
        self.write_call("String.new", 1)
        for char in string:
            self.write_push(Segment.CONSTANT, ord(char))
            self.write_call("String.appendChar", 2)


class CompilationEngine():
    """A recursive top-down syntax analyzer.

    This module effects the actual compilation into Vm code.
    It gets its input from a JackTokenizer and writes its parsed Vm code into an output stream.
    This is done by a series of compile_xxx() methods, where xxx is a corresponding syntactic element of the Jack grammar.
    The contract between these methods is that each compile_xxx() method should read the syntactic construct xxx from the input, advance() the tokenizer exactly beyond xxx.
    """

    OP = [ "+", "-", "*", "/", "&", "|", "<", ">", "="]
    BinaryOpArithmetic = {
        "+": Arithmetic.ADD,
        "-": Arithmetic.SUB,
        "&": Arithmetic.AND,
        "|": Arithmetic.OR,
        "<": Arithmetic.LT,
        ">": Arithmetic.GT,
        "=": Arithmetic.EQ,
        }
    UnaryOp = {
        "-": Arithmetic.NEG,
        "~": Arithmetic.NOT
        }
    KEYWORD_CONSTANT = ["true", "false", "null", "this"]

    def __init__(self, input_stream: IO, output_stream: IO) -> None:
        self.input_stream: IO = input_stream
        self.output_stream: IO = output_stream

        self.tokenizer = JackTokenizer(self.input_stream)

        self.indent_level = 0  # TODO delete this

        self.class_name: str = ""

        self.class_symbol_table: SymbolTable = SymbolTable()
        self.subroutine_symbol_table: SymbolTable = SymbolTable()

        self.subroutine_name: str = ""
        self.subroutine_type: str = ""
        self.local_var_nums: int = 0
        self.while_index:int = 0
        self.if_index:int = 0

        self.vm_writer = VMWriter(self.output_stream)

        self.dispatch_statement_compile: dict = {
            "do": self.compile_do,
            "let": self.compile_let,
            "while": self.compile_while,
            "return": self.compile_return,
            "if": self.compile_if,
        }

    def compile_class(self) -> None:
        """Compiles a complete class"""

        assert self.tokenizer.keyword == "class"
        self.tokenizer.advance()

        self.class_name = self.get_identifier()

        self.get_specified_symbol("{")

        while self._is_keyword(["static", "field"]):
            self.compile_class_var_dec()
        while self._is_keyword(["constructor", "function", "method"]):
            self.compile_subroutine()

        assert self.tokenizer.symbol == "}"

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""

        var_kind_str =  self.get_keyword()
        if var_kind_str == "static":
            var_kind = VarKind.STATIC
        elif var_kind_str == "field":
            var_kind = VarKind.FIELD
        else:
            raise Exception("Unsupport var kind {}".format(var_kind_str))
        var_type = self.get_type()
        var_name = self.get_identifier()
        self.class_symbol_table.define(var_name, var_type, var_kind)
        while self._is_symbol(","):
            self.get_specified_symbol(",")
            var_name = self.get_identifier()
            self.class_symbol_table.define(var_name, var_type, var_kind)

        self.get_specified_symbol(";")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function or constructor."""
        self.subroutine_symbol_table.reset()

        self.subroutine_name = ""
        self.subroutine_type = ""
        self.local_var_nums = 0
        self.while_index = 0
        self.if_index = 0

        self.subroutine_type = self.get_keyword()
        assert self.subroutine_type in ["constructor", "function", "method"]

        if self._is_keyword("void"):
            self.get_keyword()
        else:
            self.get_type()

        self.subroutine_name = "{}.{}".format(self.class_name, self.get_identifier())


        if self.subroutine_type == "method":
            self.subroutine_symbol_table.define("this", self.class_name, VarKind.ARGUMENT)

        self.get_specified_symbol("(")
        # No VM write here, but will add argumnet to the self.subroutine_symbol_table
        self.compile_parameter_list()
        self.get_specified_symbol(")")

        self.get_specified_symbol("{")

        while self._is_keyword("var"):
            # NO VM write here, but will update the self.local_var_nums
            self.compile_var_dec()

        self.vm_writer.write_function(self.subroutine_name, self.local_var_nums)

        if self.subroutine_type == "method":
            # Set this to the first argument
            self.vm_writer.write_push(Segment.ARGUMENT, 0)
            self.vm_writer.write_pop(Segment.POINTER, 0)
        elif self.subroutine_type == "constructor":
            # call Memory.alloc to alloc memory from the new object, and set the return address to this
            field_nums = self.class_symbol_table.get_varkind_nums(VarKind.FIELD)
            self.vm_writer.write_push(Segment.CONSTANT, field_nums)
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop(Segment.POINTER, 0)


        self.compile_statements()

        self.get_specified_symbol("}")

    def compile_parameter_list(self) -> None:  # DONE
        """Compiles a (possibly empty) parameter list, not including the enclosing '()'."""
        while not self._is_symbol(")"):
            type = self.get_type()
            identifier = self.get_identifier()
            self.subroutine_symbol_table.define(identifier, type, VarKind.ARGUMENT)
            if (self._is_symbol(",")):
                self.get_specified_symbol(",")

    def compile_var_dec(self) -> None:  # DONE
        """Compiles a var declaration."""
        assert self.get_keyword() == "var"
        type = self.get_type()
        identifier = self.get_identifier()
        self.subroutine_symbol_table.define(identifier, type, VarKind.VAR)
        self.local_var_nums += 1

        while self._is_symbol(","):
            self.get_specified_symbol(",")
            identifier = self.get_identifier()
            self.subroutine_symbol_table.define(identifier, type, VarKind.VAR)
            self.local_var_nums += 1

        self.get_specified_symbol(";")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing '{}'."""
        while self._is_keyword(["let", "if", "while", "do", "return"]):
            self.dispatch_statement_compile[self.tokenizer.keyword]()

    def compile_do(self) -> None:
        """Compiles a do statement."""
        assert self._is_keyword("do")
        self.get_keyword()

        module_name = self.get_identifier()

        if self._is_symbol("."):
            self.get_specified_symbol(".")
            subroutine_name = self.get_identifier()
        else:  # The subroutine call without dot is always call current object's method
            subroutine_name = module_name
            module_name = "this"

        self._compile_subroutine_call(module_name, subroutine_name)
        self.get_specified_symbol(";")
        self.vm_writer.write_pop(Segment.TEMP, 0)  # do statement will not use it's return value

    def compile_let(self) -> None:  # TODO
        """Compiles a let statement."""

        assert self.get_keyword() == "let"
        var_name = self.get_identifier()

        if self._is_symbol("["):
            # left side is a array
            self._compile_array_address(var_name)
            self.get_specified_symbol("=")
            self.compile_expression()
            self.vm_writer.write_pop(Segment.TEMP, 0)
            self.vm_writer.write_pop(Segment.POINTER, 1)
            self.vm_writer.write_push(Segment.TEMP, 0)
            self.vm_writer.write_pop(Segment.THAT, 0)
        else:
            var_type, var_kind, var_index = self._consult_symbol_table(var_name)
            assert var_type is not None and var_kind is not None and var_index is not None
            self.get_specified_symbol("=")
            self.compile_expression()
            self.vm_writer.write_pop(var_kind.value, var_index)

        self.get_specified_symbol(";")


    def compile_while(self) -> None:
        """Compiles a while statement."""
        ex_label = "WHILE_EXP{}".format(self.while_index)
        end_label = "WHILE_END{}".format(self.while_index)
        self.while_index += 1
        assert self._is_keyword("while")
        self.get_keyword()

        self.vm_writer.write_label(ex_label)
        self.get_specified_symbol("(")
        self.compile_expression()
        self.get_specified_symbol(")")

        self.vm_writer.write_arithmetic(Arithmetic.NOT)
        self.vm_writer.write_if(end_label)

        self.get_specified_symbol("{")
        self.compile_statements()
        self.get_specified_symbol("}")

        self.vm_writer.write_goto(ex_label)
        self.vm_writer.write_label(end_label)

    def compile_return(self) -> None:
        """Compiles a return statement."""

        assert self._is_keyword("return")
        self.get_keyword()

        if not self._is_symbol(";"):
            self.compile_expression()
        else:
            self.vm_writer.write_push(Segment.CONSTANT, 0)

        self.vm_writer.write_return()
        self.get_specified_symbol(";")

    def compile_if(self) -> None:  # DONE
        """Compiles an if statement, possibly with a trailing else clause."""
        assert self.get_keyword() == "if"

        label_true = "IF_TRUE{}".format(self.if_index)
        label_false = "IF_FALSE{}".format(self.if_index)
        label_end = "IF_END{}".format(self.if_index)
        self.if_index += 1

        self.get_specified_symbol("(")
        self.compile_expression()
        self.get_specified_symbol(")")

        self.vm_writer.write_if(label_true)
        self.vm_writer.write_goto(label_false)

        self.vm_writer.write_label(label_true)
        self.get_specified_symbol("{")
        self.compile_statements()
        self.get_specified_symbol("}")

        if (self._is_keyword("else")):
            self.vm_writer.write_goto(label_end)  # If there is no else, this goto is not needed

            self.vm_writer.write_label(label_false)
            self.get_keyword()
            self.get_specified_symbol("{")
            self.compile_statements()
            self.get_specified_symbol("}")

            self.vm_writer.write_label(label_end)  # If there is no else, this label is not needed
        else:
            self.vm_writer.write_label(label_false)


    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.compile_term()
        while self._is_symbol(CompilationEngine.OP):
            operator = self.tokenizer.symbol
            self.tokenizer.advance()
            self.compile_term()
            if operator in CompilationEngine.BinaryOpArithmetic:
                self.vm_writer.write_arithmetic(CompilationEngine.BinaryOpArithmetic[operator])
            elif operator == "*":
                self.vm_writer.write_call("Math.multiply", 2)
            elif operator == "/":
                self.vm_writer.write_call("Math.divide", 2)

    def compile_term(self) -> None:
        """Compiles a term.

        This method is faced with a slight difficulty when trying to decide between
        some of the alternative rules. Specifically, if the current token is an identifier,
        it must still distinguish between a variable, an array entry, and a subroutine call.
        The distinction can be made by looking ahead one extra token.A single look-ahead token,
        which may be one of “[“, “(“, “.”, suffices to distinguish between the three possibilities.
        Any other token is not part of this term and should not be advanced over.
        """

        if self.tokenizer.token_type == "integerConstant":
            self.vm_writer.write_push(Segment.CONSTANT, self.tokenizer.int_val)
            self.tokenizer.advance()
        elif self.tokenizer.token_type == "stringConstant":
            string = self.tokenizer.string_val
            self.vm_writer.write_string_constant(string)
            self.tokenizer.advance()
        elif self._is_keyword(CompilationEngine.KEYWORD_CONSTANT):  # TODO is this.variable exist?
            keyword_constant = self.get_keyword()
            self.vm_writer.write_keyword_constant(keyword_constant)
        elif self._is_symbol("("):
            self.get_specified_symbol("(")
            self.compile_expression()
            self.get_specified_symbol(")")
        elif self._is_symbol(CompilationEngine.UnaryOp):
            operator = self.get_specified_symbol(CompilationEngine.UnaryOp)
            self.compile_term()
            self.vm_writer.write_arithmetic(CompilationEngine.UnaryOp[operator])
        elif self.tokenizer.token_type == "identifier":
            identifier = self.get_identifier()
            if self._is_symbol("["): # get value form the array
                self._compile_array_address(identifier)
                self.vm_writer.write_pop(Segment.POINTER, 1)
                self.vm_writer.write_push(Segment.THAT, 0)
            elif self._is_symbol("("):  # call this.method
                self._compile_subroutine_call("this", identifier)
            elif self._is_symbol("."):  # DONE
                self.get_specified_symbol(".")
                subroutine_name = self.get_identifier()
                self._compile_subroutine_call(identifier, subroutine_name)
            else:  # Just a single varName
                self._compile_term_single_varname(identifier)
        else:
            raise Exception("Error term.")

    def compile_expression_list(self) -> int:  # DONE
        """Compiles a (possible empty) comma-separated list of expression."""
        argument_nums = 0
        while not self._is_symbol(")"):
            self.compile_expression()
            argument_nums += 1
            if self._is_symbol(","):
                self.get_specified_symbol(",")
        return argument_nums

    def compile_type(self) -> None:  # DONE
        """Compile a type."""
        if self.tokenizer.token_type == "identifier":
            self.compile_identifier()
        elif self.tokenizer.token_type == "keyword" and self.tokenizer.keyword in [
                "int", "char", "boolean"
        ]:
            self.compile_keyword()
        else:
            raise Exception("Current token is not a type!")
    
    def _compile_subroutine_call(self, module_name: str, subroutine_name: str) -> None:
        """Compile a class subroutine or a object subroutine. The token should start at the `(`, and eat the corresponding `)`"""

        if module_name == "this":  # method of current class
            argument_nums = 1
            class_name = self.class_name
            self.vm_writer.write_push(Segment.POINTER, 0)
        else:
            var_type, var_kind, var_index = self._consult_symbol_table(module_name)
            if var_type is None or var_kind is None or var_index is None:  # function
                argument_nums = 0
                class_name = module_name
            else:  # method of var_type
                argument_nums = 1
                class_name = var_type
                self.vm_writer.write_push(var_kind.value, var_index)

        self.get_specified_symbol("(")
        argument_nums += self.compile_expression_list()
        self.get_specified_symbol(")")

        self.vm_writer.write_call("{}.{}".format(class_name, subroutine_name), argument_nums)

    def _compile_term_single_varname(self, varname: str) -> None:  # DONE
        """Compile term that is the given single varname. Don't advance the tokenizer."""
        _, var_kind, var_index = self._consult_symbol_table(varname)
        if var_kind is None or var_index is None:
            raise Exception("Can't find var {} in the symbol table!".format(varname))
        self.vm_writer.write_push(var_kind.value, var_index)

    def _compile_array_address(self, var_name) -> None:
        """Push the array address into the stack, The token should start at `[`, after calling this function, the corresponding `]` will be consumed."""
        var_type, var_kind, var_index = self._consult_symbol_table(var_name)
        assert var_type is not None and var_kind is not None and var_index is not None
        self.get_specified_symbol("[")
        self.compile_expression()
        self.get_specified_symbol("]")
        self.vm_writer.write_push(var_kind.value, var_index)
        self.vm_writer.write_arithmetic(Arithmetic.ADD)

    def compile_keyword(self):
        """Compile a Keyword"""
        self._write_xml("<keyword> {} </keyword>\n".format(
            self.tokenizer.keyword))
        self.tokenizer.advance()

    def get_identifier(self) -> str:
        """Return the current identifier and advance the tokenizer."""
        identifier = self.tokenizer.identifier
        self.tokenizer.advance()
        return identifier

    def get_type(self) -> str:
        """Get a type and advance the tokenizer."""
        if self.tokenizer.token_type == "identifier":
            return self.get_identifier()
        elif self.tokenizer.token_type == "keyword" and self.tokenizer.keyword in [
                "int", "char", "boolean"
        ]:
            return self.get_keyword()
        else:
            raise Exception("Current token is not a type!")

    def get_keyword(self) -> str:
        """Return the current keyword and advance the tokenizer."""
        keyword = self.tokenizer.keyword
        self.tokenizer.advance()
        return keyword

    def compile_identifier(self) -> None:  # TODO delete
        """Compile an Identifier."""
        self._write_xml("<identifier> {} </identifier>\n".format(
            self.tokenizer.identifier))
        self.tokenizer.advance()

    def get_specified_symbol(self, symbol: Union[str, Iterable[str]]) -> str:
        """Return the specified symbol, and advanced the tokenizer."""
        assert self.tokenizer.symbol == symbol or self.tokenizer.symbol in symbol
        current_symbol = self.tokenizer.symbol
        self.tokenizer.advance()
        return current_symbol

    def compile_given_symbol(self, symbol: str) -> None:  # TODO delete
        """Compile a symbol, make sure the symbol equals to the input."""
        assert self.tokenizer.symbol == symbol
        if symbol in JackAnalyzer.XML_token_convert:
            symbol = JackAnalyzer.XML_token_convert[symbol]
        self._write_xml("<symbol> {} </symbol>\n".format(symbol))
        self.tokenizer.advance()

    def _consult_symbol_table(self, varname:str) -> tuple[Union[str, None], Union[VarKind, None], Union[int, None]]:
        """Consult the given varname in the symbol."""
        var_type, var_kind, var_index = None, None, None
        if varname in self.subroutine_symbol_table:
            var_type = self.subroutine_symbol_table.type_of(varname)
            var_kind = self.subroutine_symbol_table.kind_of(varname)
            var_index = self.subroutine_symbol_table.index_of(varname)
        elif varname in self.class_symbol_table:
            var_type = self.class_symbol_table.type_of(varname)
            var_kind = self.class_symbol_table.kind_of(varname)
            var_index = self.class_symbol_table.index_of(varname)
        return var_type, var_kind, var_index

    def _is_symbol(self, symbol: Union[str, Iterable[str]]) -> bool:
        """Return True if current token is the given symbol."""
        if type(symbol) == str:
            return self.tokenizer.token_type == "symbol" and self.tokenizer.symbol == symbol
        else:
            return self.tokenizer.token_type == "symbol" and self.tokenizer.symbol in symbol

    def _is_keyword(self, keyword: Union[str, List[str]]) -> bool:
        """Return True is current token is the given keyword."""
        if type(keyword) == str:
            return self.tokenizer.token_type == "keyword" and self.tokenizer.keyword == keyword
        else:
            return self.tokenizer.token_type == "keyword" and self.tokenizer.keyword in keyword

    def _write_xml(self, contents: str):
        """Write contents to the output, and add indent according to self.indent_level"""
        self.output_stream.write("  " * self.indent_level + contents)


class JackCompiler():
    """Top-most module."""
    def __init__(self, jack_file_or_path: str):
        self.jack_files = []
        if os.path.isfile(jack_file_or_path):
            assert os.path.splitext(jack_file_or_path)[1] == ".jack"
            self.jack_files = [jack_file_or_path]
            self.base_fold = os.path.split(jack_file_or_path)[0]
        elif os.path.isdir(jack_file_or_path):
            self.base_fold = jack_file_or_path.rstrip(os.path.sep)
            self.jack_files = [
                os.path.join(self.base_fold, file)
                for file in os.listdir(self.base_fold)
                if file.endswith(".jack")
            ]
        else:
            raise Exception("Must input a jack file or a directory.")
        assert self.jack_files

    def get_vm_file_name(self, jack_file: str) -> str:
        """Return the vm file name of the given jack_file path."""
        jack_file_name_without_extension = os.path.splitext(
            os.path.basename(jack_file))[0]
        return os.path.join(self.base_fold, jack_file_name_without_extension + ".vm")

    def generate_vm_files(self) -> None:
        """Generate the corresponding vm file for each jack file."""
        for jack_file in self.jack_files:
            print("Start generating vm file for {}.".format(jack_file))
            with open(jack_file, "r", encoding="utf-8") as jack_file_io:
                vm_file = self.get_vm_file_name(jack_file)
                with open(vm_file, "w", encoding="utf-8") as vm_file_io:
                    compilation_engine = CompilationEngine(jack_file_io, vm_file_io)
                    compilation_engine.tokenizer.advance()
                    compilation_engine.compile_class()
                    assert compilation_engine.tokenizer.has_more_tokens() is False
            print("Generating vm file for {} at {} success.".format(jack_file, vm_file))


if __name__ == "__main__":
    assert len(sys.argv) == 2
    JackCompiler(sys.argv[1]).generate_vm_files()
