#!/usr/bin/env python3

import os
import subprocess
import unittest


def run_hdl_tst_file(tst_file):
    command = "../../tools/HardwareSimulator.sh {}".format(tst_file)
    try:
        subprocess.run(command, check=True, shell=True,
                        capture_output=True, text=True)
        print("Test {} success".format(tst_file))
    except subprocess.CalledProcessError as e:
        raise Exception("Error: {} for test {}".format(e.stderr, tst_file))


class Test(unittest.TestCase):
    def test_half_adder(self):
        tst_files = [
            "./HalfAdder.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_full_adder(self):
        tst_files = [
            "./FullAdder.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_inc_16(self):
        tst_files = [
            "./Inc16.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_ALU_without_status_output(self):
        tst_files = [
            "./ALU-nostat.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_ALU(self):
        tst_files = [
            "./ALU.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)
    

if __name__ == "__main__":
    unittest.main()



