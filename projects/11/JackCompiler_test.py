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
        JackCompiler("./Seven").generate_vm_files()
        self.assertTrue(compare_files("./Seven/Main.vm", "./Seven/correct/Main.vm"))
        

if __name__ == "__main__":
    unittest.main()
