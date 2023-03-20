import os
import tempfile
import shutil
import unittest
from einkify.archive import extract_file


class TestExtractFile(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_extract_cbz_file(self):
        cbz_file = os.path.join(os.path.dirname(__file__), "assets/test.cbz")
        extracted_dir = extract_file(cbz_file, self.temp_dir)
        self.assertTrue(os.path.isdir(extracted_dir))
        self.assertGreater(len(os.listdir(extracted_dir)), 0)

    def test_extract_cbr_file(self):
        cbr_file = os.path.join(os.path.dirname(__file__), "assets/test.cbr")
        print(cbr_file)
        extracted_dir = extract_file(cbr_file, self.temp_dir)
        self.assertTrue(os.path.isdir(extracted_dir))
        self.assertGreater(len(os.listdir(extracted_dir)), 0)

    def test_nonexistent_file(self):
        nonexistent_file = os.path.join(
            os.path.dirname(__file__), "assets/nonexistent.cbz"
        )
        with self.assertRaises(FileNotFoundError):
            extract_file(nonexistent_file, self.temp_dir)


if __name__ == "__main__":
    unittest.main()
