#!/usr/bin/env python3

import os
import subprocess
import unittest


def run_hdl_tst_file(tst_file):
    command = "../../../tools/CPUEmulator.sh  {}".format(tst_file)
    try:
        subprocess.run(command, check=True, shell=True,
                        capture_output=True, text=True)
        print("Test {} success".format(tst_file))
    except subprocess.CalledProcessError as e:
        raise Exception("Error: {} for test {}".format(e.stderr, tst_file))


class Test(unittest.TestCase):
    def test_mult(self):
        tst_files = [
            "FillAutomatic.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)



if __name__ == "__main__":
    unittest.main()



