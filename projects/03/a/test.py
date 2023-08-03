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
    def test_bit(self):
        tst_files = [
            "./Bit.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_Register(self):
        tst_files = [
            "./Register.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_RAM8(self):
        tst_files = [
            "./RAM8.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_RAM64(self):
        tst_files = [
            "./RAM64.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_PC(self):
        tst_files = [
            "./PC.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)
    

if __name__ == "__main__":
    unittest.main()



