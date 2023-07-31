#!/usr/bin/env python

import os
import re
import sys
import subprocess

from typing import IO, List, Tuple, Union


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


class CompilationEngine():
    """A recursive top-down syntax analyzer.

    This module effects the actual compilation into XML form.
    It gets its input from a JackTokenizer and writes its parsed XML structure into an output file/stream.
    This is done by a series of compile_xxx() methods, where xxx is a corresponding syntactic element of the Jack grammar.
    The contract between these methods is that each compile_xxx() method should read the syntactic construct xxx from the input, advance() the tokenizer exactly beyond xxx, and output the XML parsing of xxx.
    Thus, compile_xxx()may only be called if indeed xxx is the next syntactic element of the input. In the next chapter, this module will be modified to output the compiled code rather than XML. 
    """

    OP = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
    UNARY_OP = ["-", "~"]
    KEYWORD_CONSTANT = ["true", "false", "null", "this"]

    def __init__(self, input_stream: IO, output_stream: IO) -> None:
        self.tokenizer = JackTokenizer(input_stream)
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.indent_level = 0
        self.dispatch = {
            "class": self.compile_class,
            "static": self.compile_class_var_dec,
            "field": self.compile_class_var_dec,
            "constructor": self.compile_subroutine,
            "function": self.compile_subroutine,
            "method": self.compile_subroutine,
            "var": self.compile_var_dec,
            "do": self.compile_do,
            "let": self.compile_let,
            "while": self.compile_while,
            "return": self.compile_return,
            "if": self.compile_if,
        }

    def compile_class(self) -> None:
        """Compiles a complete class"""
        self._write_xml("<class>\n")
        self.indent_level += 1

        assert self.tokenizer.keyword == "class"
        self.compile_keyword()

        self.compile_identifier()

        self.compile_given_symbol("{")

        while self._is_keyword(["static", "field"]):
            self.compile_class_var_dec()
        while self._is_keyword(["constructor", "function", "method"]):
            self.compile_subroutine()

        self._write_xml("<symbol> {} </symbol>\n".format("}"))

        self.indent_level -= 1
        self._write_xml("</class>")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self._write_xml("<classVarDec>\n")
        self.indent_level += 1
        assert self._is_keyword(["static", "field"])

        self.compile_keyword()
        self.compile_type()
        self.compile_identifier()
        while self._is_symbol(","):
            self.compile_given_symbol(",")
            self.compile_identifier()

        self.compile_given_symbol(";")

        self.indent_level -= 1
        self._write_xml("</classVarDec>\n")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function or constructor."""
        self._write_xml("<subroutineDec>\n")
        self.indent_level += 1

        self.compile_keyword()

        if self._is_keyword("void"):
            self.compile_keyword()
        else:
            self.compile_type()
        self.compile_identifier()
        self.compile_given_symbol("(")
        self.compile_parameter_list()
        self.compile_given_symbol(")")

        self._write_xml("<subroutineBody>\n")
        self.indent_level += 1
        self.compile_given_symbol("{")

        while self._is_keyword("var"):
            self.compile_var_dec()

        self.compile_statements()

        self.compile_given_symbol("}")

        self.indent_level -= 1
        self._write_xml("</subroutineBody>\n")

        self.indent_level -= 1
        self._write_xml("</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the enclosing '()'."""
        self._write_xml("<parameterList>\n")
        self.indent_level += 1
        while not self._is_symbol(")"):
            self.compile_type()
            self.compile_identifier()
            if (self._is_symbol(",")):
                self.compile_given_symbol(",")

        self.indent_level -= 1
        self._write_xml("</parameterList>\n")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self._write_xml("<varDec>\n")
        self.indent_level += 1

        assert self._is_keyword("var")
        self.compile_keyword()  # var keyword
        self.compile_type()
        self.compile_identifier()

        while self._is_symbol(","):
            self.compile_given_symbol(",")
            self.compile_identifier()

        self.compile_given_symbol(";")
        self.indent_level -= 1
        self._write_xml("</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing '{}'."""
        self._write_xml("<statements>\n")
        self.indent_level += 1

        while self._is_keyword(["let", "if", "while", "do", "return"]):
            self.dispatch[self.tokenizer.keyword]()

        self.indent_level -= 1
        self._write_xml("</statements>\n")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self._write_xml("<doStatement>\n")
        self.indent_level += 1

        assert self._is_keyword("do")
        self.compile_keyword()
        self.compile_identifier()

        if self._is_symbol("."):
            self.compile_given_symbol(".")
            self.compile_identifier()

        self.compile_given_symbol("(")
        self.compile_expression_list()
        self.compile_given_symbol(")")
        self.compile_given_symbol(";")

        self.indent_level -= 1
        self._write_xml("</doStatement>\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self._write_xml("<letStatement>\n")
        self.indent_level += 1

        assert self._is_keyword("let")
        self.compile_keyword()
        self.compile_identifier()

        if self._is_symbol("["):
            self.compile_given_symbol("[")
            self.compile_expression()
            self.compile_given_symbol("]")

        self.compile_given_symbol("=")
        self.compile_expression()
        self.compile_given_symbol(";")

        self.indent_level -= 1
        self._write_xml("</letStatement>\n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self._write_xml("<whileStatement>\n")
        self.indent_level += 1

        assert self._is_keyword("while")
        self.compile_keyword()

        self.compile_given_symbol("(")
        self.compile_expression()
        self.compile_given_symbol(")")

        self.compile_given_symbol("{")
        self.compile_statements()
        self.compile_given_symbol("}")

        self.indent_level -= 1
        self._write_xml("</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self._write_xml("<returnStatement>\n")
        self.indent_level += 1

        assert self._is_keyword("return")
        self.compile_keyword()

        if not self._is_symbol(";"):
            self.compile_expression()
        self.compile_given_symbol(";")

        self.indent_level -= 1
        self._write_xml("</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles an if statement, possibly with a trailing else clause."""
        self._write_xml("<ifStatement>\n")
        self.indent_level += 1

        assert self._is_keyword("if")
        self.compile_keyword()

        self.compile_given_symbol("(")
        self.compile_expression()
        self.compile_given_symbol(")")

        self.compile_given_symbol("{")
        self.compile_statements()
        self.compile_given_symbol("}")

        if (self._is_keyword("else")):
            self.compile_keyword()
            self.compile_given_symbol("{")
            self.compile_statements()
            self.compile_given_symbol("}")

        self.indent_level -= 1
        self._write_xml("</ifStatement>\n")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self._write_xml("<expression>\n")
        self.indent_level += 1

        self.compile_term()
        while self._is_symbol(CompilationEngine.OP):
            self.compile_given_symbol(self.tokenizer.symbol)
            self.compile_term()

        self.indent_level -= 1
        self._write_xml("</expression>\n")

    def compile_term(self) -> None:
        """Compiles a term.

        This method is faced with a slight difficulty when trying to decide between
        some of the alternative rules.Specifically, if the current token is an identifier,
        it must still distinguish between a variable, an array entry, and a subroutine call.
        The distinction can be made by looking ahead one extra token.A single look-ahead token,
        which may be one of “[“, “(“, “.”, suffices to distinguish between the three possibilities.
        Any other token is not part of this term and should not be advanced over. 
        """
        self._write_xml("<term>\n")
        self.indent_level += 1

        if self.tokenizer.token_type == "integerConstant":
            self._write_xml("<integerConstant> {} </integerConstant>\n".format(
                self.tokenizer.int_val))
            self.tokenizer.advance()
        elif self.tokenizer.token_type == "stringConstant":
            self._write_xml("<stringConstant> {} </stringConstant>\n".format(
                self.tokenizer.string_val))
            self.tokenizer.advance()
        elif self._is_keyword(CompilationEngine.KEYWORD_CONSTANT):
            self.compile_keyword()
        elif self._is_symbol("("):
            self.compile_given_symbol("(")
            self.compile_expression()
            self.compile_given_symbol(")")
        elif self._is_symbol(CompilationEngine.UNARY_OP):
            self.compile_given_symbol(self.tokenizer.symbol)
            self.compile_term()
        elif self.tokenizer.token_type == "identifier":
            self.compile_identifier()
            if self._is_symbol("["):
                self.compile_given_symbol("[")
                self.compile_expression()
                self.compile_given_symbol("]")
            elif self._is_symbol("("):
                self.compile_given_symbol("(")
                self.compile_expression_list()
                self.compile_given_symbol(")")
            elif self._is_symbol("."):
                self.compile_given_symbol(".")
                self.compile_identifier()
                self.compile_given_symbol("(")
                self.compile_expression_list()
                self.compile_given_symbol(")")
        else:
            raise Exception("Error term.")

        self.indent_level -= 1
        self._write_xml("</term>\n")

    def compile_expression_list(self) -> None:
        """Compiles a (possible empty) comma-separated list of expression."""
        self._write_xml("<expressionList>\n")
        self.indent_level += 1
        while not self._is_symbol(")"):
            self.compile_expression()
            if self._is_symbol(","):
                self.compile_given_symbol(",")

        self.indent_level -= 1
        self._write_xml("</expressionList>\n")

    def compile_type(self) -> None:
        """Compile a type."""
        if self.tokenizer.token_type == "identifier":
            self.compile_identifier()
        elif self.tokenizer.token_type == "keyword" and self.tokenizer.keyword in [
                "int", "char", "boolean"
        ]:
            self.compile_keyword()
        else:
            raise Exception("Current token is not a type!")

    def compile_keyword(self):
        """Compile a Keyword"""
        self._write_xml("<keyword> {} </keyword>\n".format(
            self.tokenizer.keyword))
        self.tokenizer.advance()

    def compile_identifier(self) -> None:
        """Compile an Identifier."""
        self._write_xml("<identifier> {} </identifier>\n".format(
            self.tokenizer.identifier))
        self.tokenizer.advance()

    def compile_given_symbol(self, symbol: str) -> None:
        """Compile a symbol, make sure the symbol equals to the input."""
        assert self.tokenizer.symbol == symbol
        if symbol in JackAnalyzer.XML_token_convert:
            symbol = JackAnalyzer.XML_token_convert[symbol]
        self._write_xml("<symbol> {} </symbol>\n".format(symbol))
        self.tokenizer.advance()

    def _is_symbol(self, symbol: Union[str, List[str]]) -> bool:
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


class JackAnalyzer():
    """A main driver that organizes and invokes everything."""

    XML_token_convert = {
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "&": "&amp;",
    }

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
        self.output_path = os.path.join(self.base_fold, "output")
        os.makedirs(self.output_path, exist_ok=True)

    def get_output_file_name(self, jack_file: str) -> Tuple[str, str, str, str]:
        """Return the tokenizer xml file path and the analyzer output file path of the input jack_file path"""
        jack_file_name_without_extension = os.path.splitext(
            os.path.basename(jack_file))[0]
        tokenizer_file = os.path.join(
            self.output_path, jack_file_name_without_extension + "T.xml")
        analyzer_output_file = os.path.join(
            self.output_path, jack_file_name_without_extension + ".xml")
        real_tokenizer_file = os.path.join(
            self.base_fold, jack_file_name_without_extension + "T.xml")
        real_analyzer_output_file = os.path.join(
            self.base_fold, jack_file_name_without_extension + ".xml")

        return tokenizer_file, analyzer_output_file, real_tokenizer_file, real_analyzer_output_file

    @staticmethod
    def convert_token_for_xml(token):
        """Convert the '<' '>' '"' '&' to '&lt;' '&gt;' '&quot;' '&amp;'"""
        xml_token = JackAnalyzer.XML_token_convert.get(token, None)
        return xml_token if xml_token is not None else token

    def test_tokenizer(self):
        """Write the tokenizer to corresponding xml file."""
        for jack_file in self.jack_files:
            with open(jack_file, "r", encoding="utf-8") as jack_file_io:
                tokenizer = JackTokenizer(jack_file_io)
                tokenizer_file, _, real_tokenizer_file, _ = self.get_output_file_name(
                    jack_file)
                with open(tokenizer_file, "w",
                          encoding="utf-8") as tokenizer_file_io:
                    tokenizer_file_io.write("<tokens>\n")
                    while tokenizer.has_more_tokens():
                        tokenizer.advance()
                        token_type = tokenizer.token_type
                        cur_token = ""
                        if token_type == "keyword":
                            cur_token = tokenizer.keyword.lower()
                        elif token_type == "symbol":
                            cur_token = self.convert_token_for_xml(
                                tokenizer.symbol)
                        elif token_type == "identifier":
                            cur_token = tokenizer.identifier
                        elif token_type == "integerConstant":
                            cur_token = str(tokenizer.int_val)
                        elif token_type == "stringConstant":
                            cur_token = tokenizer.string_val
                        else:
                            assert False
                        tokenizer_file_io.write("<{}>".format(token_type))
                        tokenizer_file_io.write(cur_token)
                        tokenizer_file_io.write("</{}>".format(token_type))
                        tokenizer_file_io.write("\n")
                    tokenizer_file_io.write("</tokens>")
                self.compare_xml_files(tokenizer_file,
                                        real_tokenizer_file)
                print("Output the tokenizer of {} Success".format(
                        jack_file))

    def generate_xml(self, compare: bool = True) -> None:
        """Generate the corresponding xml file for each jack file in the output path."""
        for jack_file in self.jack_files:
            print("Start generating xml file for {}.".format(jack_file))
            with open(jack_file, "r", encoding="utf-8") as jack_file_io:
                _, analyzer_output_file, _, real_analyzer_output_file = self.get_output_file_name(
                    jack_file)
                with open(analyzer_output_file, "w",
                          encoding="utf-8") as analyzer_file_io:
                    compilation_engine = CompilationEngine(
                        jack_file_io, analyzer_file_io)
                    compilation_engine.tokenizer.advance()
                    compilation_engine.compile_class()
                    try:
                       assert compilation_engine.tokenizer.has_more_tokens() is False
                    except:
                        compilation_engine.tokenizer.advance()
                        print("addition token:", compilation_engine.tokenizer.cur_token)
            if compare:
                self.compare_xml_files(analyzer_output_file,
                                       real_analyzer_output_file)
            print("Generating xml file for {} at {} success.".format(jack_file, analyzer_output_file))

    @staticmethod
    def compare_xml_files(file: str, target_file: str):
        command = "../../tools/TextComparer.sh {} {}".format(file, target_file)
        try:
            subprocess.run(command,
                           check=True,
                           shell=True,
                           capture_output=True,
                           text=True)
            print("{} and {} is the same!".format(file, target_file))
        except subprocess.CalledProcessError as e:
            raise Exception("Error: {}".format(e.stdout))


if __name__ == "__main__":
    assert len(sys.argv) == 2
    JackAnalyzer(sys.argv[1]).generate_xml(compare=False)
