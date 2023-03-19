import sys
import os
import unittest


class EInkifyTests(unittest.TestCase):
    def test_verify_file(self):
        from einkify.__main__ import verify_file

        self.assertTrue(verify_file("test.cbz"))
