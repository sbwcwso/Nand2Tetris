#!/usr/bin/env python3

import os
import subprocess
import unittest


def run_hdl_tst_file(tst_file):
    command = "../../../tools/HardwareSimulator.sh  {}".format(tst_file)
    try:
        subprocess.run(command, check=True, shell=True,
                        capture_output=True, text=True)
        print("Test {} success".format(tst_file))
    except subprocess.CalledProcessError as e:
        raise Exception("Error: {} for test {}".format(e.stderr, tst_file))


class Test(unittest.TestCase):

    def test_RAM512(self):
        tst_files = [
            "./RAM512.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_RAM4K(self):
        tst_files = [
            "./RAM4K.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_RAM16K(self):
        tst_files = [
            "./RAM16K.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)
    

if __name__ == "__main__":
    unittest.main()



