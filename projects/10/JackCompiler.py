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
        self.orignal_lines = list(jack_file.readlines())
        self.lines = JackTokenizer.preprocessor(self.orignal_lines)
        self.line_nums = len(self.lines)
        self.current_line_numer = 0
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

    def hasMoreTokens(self) -> bool:
        """Check if there is more tokens in the input."""
        return self.current_line_numer < self.line_nums

    @property
    def _current_char(self) -> str:
        return self.current_line[self.current_line_index]

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.

        This method should only be called if hasMoreTokens() is true.
        Initially there is no current token..
        """
        assert self.hasMoreTokens()
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
            self.current_line_numer += 1
            self.current_line_index = 0
            if self.current_line_numer < self.line_nums:
                self.current_line = self.lines[self.current_line_numer]
                self.current_line_length = len(self.current_line)

    @property
    def tokenType(self) -> str:
        """Return the type of the current token."""
        return self._cur_token_type

    @property
    def keyWord(self) -> str:
        """Returns the keyword which is the current token.

        Should be called only when self.tokenType() is KEYWORD.
        """
        assert self.tokenType == "keyword"
        return self._keyword

    @property
    def symbol(self) -> str:
        """Return the character which is the current token.

        Should be called only when self.tokenType() is SYMBOL
        """
        assert self.tokenType == "symbol"
        return self._symbol

    @property
    def identifier(self) -> str:
        """Return the identifier which is the current token.

        Should be called only when self.tokenType() is IDENTIFIER
        """
        assert self.tokenType == "identifier"
        return self._identifier

    @property
    def intVal(self) -> int:
        """Return the integar value of the current token.

        Should be called only when self.tokenType() is INT_CONST
        """
        assert self.tokenType == "integerConstant"
        return self._int_val

    @property
    def stringVal(self) -> str:
        """Return the string value of the current token, without the double quotes.

        Should be called only when self.tokenType() is STRING_CONST
        """
        assert self.tokenType == "stringConstant"
        return self._string_val

    @staticmethod
    def preprocessor(original_lines: List[str]) -> List[str]:
        """Remove extra space and comments. Add extra space around symbols"""
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
    This is done by a series of compilexxx() methods, where xxx is a corresponding syntactic element of the Jack grammar.
    The contract between these methods is that each compilexxx() method should read the syntactic construct xxx from the input, advance() the tokenizer exactly beyond xxx, and output the XML parsing of xxx.
    Thus, compilexxx()may only be called if indeed xxx is the next syntactic element of the input. In the next chapter, this module will be modified to output the compiled code rather than XML. 
    """

    OP = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
    UNARYOP = ["-", "~"]
    KEYWORDCONSTANT = ["true", "false", "null", "this"]

    def __init__(self, input_stream: IO, output_stream: IO) -> None:
        self.tokenizer = JackTokenizer(input_stream)
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.indent_level = 0
        self.dispatch = {
            "class": self.compileClass,
            "static": self.compileClassVarDec,
            "field": self.compileClassVarDec,
            "constructor": self.compileSubroutine,
            "function": self.compileSubroutine,
            "method": self.compileSubroutine,
            "var": self.compileVarDec,
            "do": self.compileDo,
            "let": self.compileLet,
            "while": self.compileWhile,
            "return": self.compileReturn,
            "if": self.compileIf,
        }

    def compileClass(self) -> None:
        """Compiles a complete class"""
        self._write_xml("<class>\n")
        self.indent_level += 1

        assert self.tokenizer.keyWord == "class"
        self.compileKeyword()

        self.compileIdentifier()

        self.compileGivenSymbol("{")

        while self._is_keyword(["static", "field"]):
            self.compileClassVarDec()
        while self._is_keyword(["constructor", "function", "method"]):
            self.compileSubroutine()

        self._write_xml("<symbol> {} </symbol>\n".format("}"))

        self.indent_level -= 1
        self._write_xml("</class>")

    def compileClassVarDec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self._write_xml("<classVarDec>\n")
        self.indent_level += 1
        assert self._is_keyword(["static", "field"])

        self.compileKeyword()
        self.compileType()
        self.compileIdentifier()
        while self._is_symbol(","):
            self.compileGivenSymbol(",")
            self.compileIdentifier()

        self.compileGivenSymbol(";")

        self.indent_level -= 1
        self._write_xml("</classVarDec>\n")

    def compileSubroutine(self) -> None:
        """Compiles a complete method, function or constructor."""
        self._write_xml("<subroutineDec>\n")
        self.indent_level += 1

        self.compileKeyword()

        if self._is_keyword("void"):
            self.compileKeyword()
        else:
            self.compileType()
        self.compileIdentifier()
        self.compileGivenSymbol("(")
        self.compileParameterList()
        self.compileGivenSymbol(")")

        self._write_xml("<subroutineBody>\n")
        self.indent_level += 1
        self.compileGivenSymbol("{")

        while self._is_keyword("var"):
            self.compileVarDec()

        self.compileStatements()

        self.compileGivenSymbol("}")

        self.indent_level -= 1
        self._write_xml("</subroutineBody>\n")

        self.indent_level -= 1
        self._write_xml("</subroutineDec>\n")

    def compileParameterList(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the enclosing '()'."""
        self._write_xml("<parameterList>\n")
        self.indent_level += 1
        while not self._is_symbol(")"):
            self.compileType()
            self.compileIdentifier()
            if (self._is_symbol(",")):
                self.compileGivenSymbol(",")

        self.indent_level -= 1
        self._write_xml("</parameterList>\n")

    def compileVarDec(self) -> None:
        """Compiles a var declaration."""
        self._write_xml("<varDec>\n")
        self.indent_level += 1

        assert self._is_keyword("var")
        self.compileKeyword()  # var keyword
        self.compileType()
        self.compileIdentifier()

        while self._is_symbol(","):
            self.compileGivenSymbol(",")
            self.compileIdentifier()

        self.compileGivenSymbol(";")
        self.indent_level -= 1
        self._write_xml("</varDec>\n")

    def compileStatements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing '{}'."""
        self._write_xml("<statements>\n")
        self.indent_level += 1

        while self._is_keyword(["let", "if", "while", "do", "return"]):
            self.dispatch[self.tokenizer.keyWord]()

        self.indent_level -= 1
        self._write_xml("</statements>\n")

    def compileDo(self) -> None:
        """Compiles a do statement."""
        self._write_xml("<doStatement>\n")
        self.indent_level += 1

        assert self._is_keyword("do")
        self.compileKeyword()
        self.compileIdentifier()

        if self._is_symbol("."):
            self.compileGivenSymbol(".")
            self.compileIdentifier()

        self.compileGivenSymbol("(")
        self.compileExpressionList()
        self.compileGivenSymbol(")")
        self.compileGivenSymbol(";")

        self.indent_level -= 1
        self._write_xml("</doStatement>\n")

    def compileLet(self) -> None:
        """Compiles a let statement."""
        self._write_xml("<letStatement>\n")
        self.indent_level += 1

        assert self._is_keyword("let")
        self.compileKeyword()
        self.compileIdentifier()

        if self._is_symbol("["):
            self.compileGivenSymbol("[")
            self.compileExpression()
            self.compileGivenSymbol("]")

        self.compileGivenSymbol("=")
        self.compileExpression()
        self.compileGivenSymbol(";")

        self.indent_level -= 1
        self._write_xml("</letStatement>\n")

    def compileWhile(self) -> None:
        """Compiles a while statement."""
        self._write_xml("<whileStatement>\n")
        self.indent_level += 1

        assert self._is_keyword("while")
        self.compileKeyword()

        self.compileGivenSymbol("(")
        self.compileExpression()
        self.compileGivenSymbol(")")

        self.compileGivenSymbol("{")
        self.compileStatements()
        self.compileGivenSymbol("}")

        self.indent_level -= 1
        self._write_xml("</whileStatement>\n")

    def compileReturn(self) -> None:
        """Compiles a return statement."""
        self._write_xml("<returnStatement>\n")
        self.indent_level += 1

        assert self._is_keyword("return")
        self.compileKeyword()

        if not self._is_symbol(";"):
            self.compileExpression()
        self.compileGivenSymbol(";")

        self.indent_level -= 1
        self._write_xml("</returnStatement>\n")

    def compileIf(self) -> None:
        """Compiles an if statement, possibly with a trailing else clause."""
        self._write_xml("<ifStatement>\n")
        self.indent_level += 1

        assert self._is_keyword("if")
        self.compileKeyword()

        self.compileGivenSymbol("(")
        self.compileExpression()
        self.compileGivenSymbol(")")

        self.compileGivenSymbol("{")
        self.compileStatements()
        self.compileGivenSymbol("}")

        if (self._is_keyword("else")):
            self.compileKeyword()
            self.compileGivenSymbol("{")
            self.compileStatements()
            self.compileGivenSymbol("}")

        self.indent_level -= 1
        self._write_xml("</ifStatement>\n")

    def compileExpression(self) -> None:
        """Compiles an expression."""
        self._write_xml("<expression>\n")
        self.indent_level += 1

        self.compileTerm()
        while self._is_symbol(CompilationEngine.OP):
            self.compileGivenSymbol(self.tokenizer.symbol)
            self.compileTerm()

        self.indent_level -= 1
        self._write_xml("</expression>\n")

    def compileTerm(self) -> None:
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

        if self.tokenizer.tokenType == "integerConstant":
            self._write_xml("<integerConstant> {} </integerConstant>\n".format(
                self.tokenizer.intVal))
            self.tokenizer.advance()
        elif self.tokenizer.tokenType == "stringConstant":
            self._write_xml("<stringConstant> {} </stringConstant>\n".format(
                self.tokenizer.stringVal))
            self.tokenizer.advance()
        elif self._is_keyword(CompilationEngine.KEYWORDCONSTANT):
            self.compileKeyword()
        elif self._is_symbol("("):
            self.compileGivenSymbol("(")
            self.compileExpression()
            self.compileGivenSymbol(")")
        elif self._is_symbol(CompilationEngine.UNARYOP):
            self.compileGivenSymbol(self.tokenizer.symbol)
            self.compileTerm()
        elif self.tokenizer.tokenType == "identifier":
            self.compileIdentifier()
            if self._is_symbol("["):
                self.compileGivenSymbol("[")
                self.compileExpression()
                self.compileGivenSymbol("]")
            elif self._is_symbol("("):
                self.compileGivenSymbol("(")
                self.compileExpressionList()
                self.compileGivenSymbol(")")
            elif self._is_symbol("."):
                self.compileGivenSymbol(".")
                self.compileIdentifier()
                self.compileGivenSymbol("(")
                self.compileExpressionList()
                self.compileGivenSymbol(")")
        else:
            raise Exception("Error term.")

        self.indent_level -= 1
        self._write_xml("</term>\n")

    def compileExpressionList(self) -> None:
        """Compiles a (possible empty) comma-separated list of expression."""
        self._write_xml("<expressionList>\n")
        self.indent_level += 1
        while not self._is_symbol(")"):
            self.compileExpression()
            if self._is_symbol(","):
                self.compileGivenSymbol(",")

        self.indent_level -= 1
        self._write_xml("</expressionList>\n")

    def compileType(self) -> None:
        """Compile a type."""
        if self.tokenizer.tokenType == "identifier":
            self.compileIdentifier()
        elif self.tokenizer.tokenType == "keyword" and self.tokenizer.keyWord in [
                "int", "char", "boolean"
        ]:
            self.compileKeyword()
        else:
            raise Exception("Current token is not a type!")

    def compileKeyword(self):
        """Compile a Keyword"""
        self._write_xml("<keyword> {} </keyword>\n".format(
            self.tokenizer.keyWord))
        self.tokenizer.advance()

    def compileIdentifier(self) -> None:
        """Compile an Identifier."""
        self._write_xml("<identifier> {} </identifier>\n".format(
            self.tokenizer.identifier))
        self.tokenizer.advance()

    def compileGivenSymbol(self, symbol: str) -> None:
        """Compile a symbol, make sure the symbol equals to the input."""
        assert self.tokenizer.symbol == symbol
        if symbol in JackAnalyzer.xmlTokenConvert:
            symbol = JackAnalyzer.xmlTokenConvert[symbol]
        self._write_xml("<symbol> {} </symbol>\n".format(symbol))
        self.tokenizer.advance()

    def _is_symbol(self, symbol: Union[str, List[str]]) -> bool:
        """Return True if current token is the given symbol."""
        if type(symbol) == str:
            return self.tokenizer.tokenType == "symbol" and self.tokenizer.symbol == symbol
        else:
            return self.tokenizer.tokenType == "symbol" and self.tokenizer.symbol in symbol

    def _is_keyword(self, keyword: Union[str, List[str]]) -> bool:
        """Return True is current token is the given keyword."""
        if type(keyword) == str:
            return self.tokenizer.tokenType == "keyword" and self.tokenizer.keyWord == keyword
        else:
            return self.tokenizer.tokenType == "keyword" and self.tokenizer.keyWord in keyword

    def _write_xml(self, contents: str):
        """Write contents to the output, and add indent according to self.indent_level"""
        self.output_stream.write("  " * self.indent_level + contents)


class JackAnalyzer():
    """A main driver that organizes and invokes everything."""

    xmlTokenConvert = {
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
        xml_token = JackAnalyzer.xmlTokenConvert.get(token, None)
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
                    while tokenizer.hasMoreTokens():
                        tokenizer.advance()
                        token_type = tokenizer.tokenType
                        cur_token = ""
                        if token_type == "keyword":
                            cur_token = tokenizer.keyWord.lower()
                        elif token_type == "symbol":
                            cur_token = self.convert_token_for_xml(
                                tokenizer.symbol)
                        elif token_type == "identifier":
                            cur_token = tokenizer.identifier
                        elif token_type == "integerConstant":
                            cur_token = str(tokenizer.intVal)
                        elif token_type == "stringConstant":
                            cur_token = tokenizer.stringVal
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
                    compilation_engine.compileClass()
                    try:
                       assert compilation_engine.tokenizer.hasMoreTokens() is False
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
            # 运行 shell 命令，并捕获输出结果
            subprocess.run(command,
                           check=True,
                           shell=True,
                           capture_output=True,
                           text=True)
            print("{} and {} is the same!".format(file, target_file))
        except subprocess.CalledProcessError as e:
            # 打印命令运行失败的输出结果
            raise Exception("Error: {}".format(e.stdout))


if __name__ == "__main__":
    assert len(sys.argv) == 2
    JackAnalyzer(sys.argv[1]).generate_xml(compare=False)
