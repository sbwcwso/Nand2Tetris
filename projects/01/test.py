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
    def test_not(self):
        tst_files = [
            "./Not.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_and(self):
        tst_files = [
            "./And.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_or(self):
        tst_files = [
            "./Or.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_xor(self):
        tst_files = [
            "./Xor.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_mux(self):
        tst_files = [
            "./Mux.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_dmux(self):
        tst_files = [
            "./DMux.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_not16(self):
        tst_files = [
            "./Not16.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_and16(self):
        tst_files = [
            "./And16.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_or16(self):
        tst_files = [
            "./Or16.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_mux16(self):
        tst_files = [
            "./Mux16.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)
    
    def test_Or8Way(self):
        tst_files = [
            "./Or8Way.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_Mux4Way16(self):
        tst_files = [
            "./Mux4Way16.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_Mux8Way16(self):
        tst_files = [
            "./Mux8Way16.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_DMux4Way(self):
        tst_files = [
            "./DMux4Way.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)

    def test_DMux8Way(self):
        tst_files = [
            "./DMux8Way.tst",
        ]
        for tst_file in tst_files:
            run_hdl_tst_file(tst_file)



if __name__ == "__main__":
    unittest.main()



