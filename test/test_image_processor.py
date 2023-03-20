import os
import tempfile
import shutil
import unittest
from PIL import Image
from einkify.image import has_allowed_extension, get_image_paths, save_image


class TestHasAllowedExtension(unittest.TestCase):
    def test_allowed_extension(self):
        image_path = os.path.join(
            os.path.dirname(__file__), "assets/images/test.jpg"
        )
        allowed_extensions = [".jpg", ".png"]
        self.assertTrue(has_allowed_extension(image_path, allowed_extensions))

    def test_disallowed_extension(self):
        image_path = os.path.join(
            os.path.dirname(__file__), "assets/images/test.bmp"
        )
        allowed_extensions = [".jpg", ".png"]
        self.assertFalse(has_allowed_extension(image_path, allowed_extensions))

    def test_empty_allowed_extensions(self):
        image_path = os.path.join(
            os.path.dirname(__file__), "assets/images/test.jpg"
        )
        allowed_extensions = []
        self.assertFalse(has_allowed_extension(image_path, allowed_extensions))

    def test_empty_image_path(self):
        image_path = ""
        allowed_extensions = [".jpg", ".png"]
        with self.assertRaises(ValueError):
            has_allowed_extension(image_path, allowed_extensions)


class TestGetImagePaths(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

        # Create some image files in the temporary directory
        with open(os.path.join(self.temp_dir, "image1.jpg"), "w") as f:
            f.write("dummy content")
        with open(os.path.join(self.temp_dir, "image2.png"), "w") as f:
            f.write("dummy content")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_get_image_paths(self):
        image_directory = self.temp_dir
        image_paths = get_image_paths(image_directory)
        self.assertIsInstance(image_paths, list)
        self.assertGreater(len(image_paths), 0)
        self.assertIn("image1.jpg", image_paths)
        self.assertIn("image2.png", image_paths)
        self.assertNotIn("image3.bmp", image_paths)

    def test_empty_directory(self):
        empty_dir = tempfile.mkdtemp()
        image_paths = get_image_paths(empty_dir)
        self.assertIsInstance(image_paths, list)
        self.assertEqual(len(image_paths), 0)

    def test_nonexistent_directory(self):
        nonexistent_dir = os.path.join(
            os.path.dirname(__file__), "test_data/nonexistent"
        )
        with self.assertRaises(FileNotFoundError):
            get_image_paths(nonexistent_dir)


class TestSaveImage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_save_image(self):
        # Create a test image
        test_image = Image.new("RGB", (100, 100), color="red")

        # Save the image to the temporary directory
        output_directory = self.temp_dir
        image_path = "test_image.jpeg"
        image_type = "jpeg"
        save_image(test_image, output_directory, image_path, image_type)

        # Check that the image was saved with the correct filename and extension
        expected_file_path = os.path.join(output_directory, image_path)
        input()
        self.assertTrue(os.path.exists(expected_file_path))
        self.assertTrue(os.path.isfile(expected_file_path))
        self.assertEqual(
            os.path.splitext(expected_file_path)[1], f".{image_type}"
        )
