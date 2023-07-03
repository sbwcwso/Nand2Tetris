#!/usr/bin/env python

import os
import subprocess
import unittest


from JackCompiler import JackCompiler


def compare_files(file: str, target_file: str) -> bool:
    command = "diff {} {} 2>&1".format(file, target_file)
    try:
        # 运行 shell 命令，并捕获输出结果
        subprocess.run(command,
                        check=True,
                        shell=True,
                        capture_output=True,
                        text=True)
        print("{} and {} is the same!".format(file, target_file))
    except subprocess.CalledProcessError as e:
        print("diff returned non-zero exit status. Output:")
        print(e.stdout)
        return False
    return True


class TestJackCompiler(unittest.TestCase):
    """Test JackCompiler with the given Jack project."""
    def test_Seven(self):
        """ A simple program
        
        An arithmetic expression involving constants only.
        A do statement
        A return statement
        """
        JackCompiler("./Seven").generate_vm_files()
        self.assertTrue(compare_files("./Seven/Main.vm", "./Seven/correct/Main.vm"))

    def test_ConvertToBin(self):
        """ Test how your compiler handles
        
        Expressions(without arrays, without method calls)
        Statements: if, while, do, let, return
        """
        JackCompiler("./ConvertToBin").generate_vm_files()
        self.assertTrue(compare_files("./ConvertToBin/Main.vm", "./ConvertToBin/correct/Main.vm"))
        
    def test_Square(self):
        """Test how your compiler handles object-oritened features of the Jack language.
        
        Constructor
        Methods
        Expressions that include method calls
        """
        JackCompiler("./Square").generate_vm_files()
        self.assertTrue(compare_files("./Square/Main.vm", "./Square/correct/Main.vm"))
        self.assertTrue(compare_files("./Square/Square.vm", "./Square/correct/Square.vm"))
        self.assertTrue(compare_files("./Square/SquareGame.vm", "./Square/correct/SquareGame.vm"))

    def test_Average(self):
        """Test how your compiler handles Arrays and Strings."""
        JackCompiler("./Average").generate_vm_files()
        self.assertTrue(compare_files("./Average/Main.vm", "./Average/correct/Main.vm"))

    def test_Pong(self):
        """Test how your compiler handles a complete object-oritened application,
        including the handling of objects and static variables."""
        JackCompiler("./Pong").generate_vm_files()
        self.assertTrue(compare_files("./Pong/Main.vm", "./Pong/correct/Main.vm"))
        self.assertTrue(compare_files("./Pong/PongGame.vm", "./Pong/correct/PongGame.vm"))
        self.assertTrue(compare_files("./Pong/Bat.vm", "./Pong/correct/Bat.vm"))

    def test_ComplexArrays(self):
        """Tests how your compiler handles array manipulations using index expression that
        include complex array references."""
        JackCompiler("./ComplexArrays").generate_vm_files()
        self.assertTrue(compare_files("./ComplexArrays/Main.vm", "./ComplexArrays/correct/Main.vm"))
        

if __name__ == "__main__":
    unittest.main()
