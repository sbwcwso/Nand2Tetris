#!/usr/bin/env python

import os
import subprocess
import unittest

def run_shell_command(command: str) -> bool:
    try:
        subprocess.run(command,
                        check=True,
                        shell=True,
                        capture_output=True,
                        text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(e.stdout)
        return False

def VMEmulator_test(tst_file: str) -> bool:
    command = "../../tools/VMEmulator.sh {}".format(tst_file)
    if run_shell_command(command):
        print("VMEmulator run test {} success!".format(tst_file))
        return True
    else:
        return False

def JackCompile(dir: str) -> bool:
    command = "../../tools/JackCompiler.sh {}".format(dir)
    if run_shell_command(command):
        print("Compile {} success!".format(dir))
        return True
    else:
        return False

class TestOS(unittest.TestCase):
    """Test JackCompiler with the given Jack project."""
    def test_Memory(self):
        JackCompile("./MemoryTest")
        VMEmulator_test("./MemoryTest/MemoryTest.tst")

if __name__ == "__main__":
    unittest.main()
