from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, MagicMock

from MetaPhoto.MetaPhoto import MetaPhoto


class TestMetaPhoto(TestCase):
    def test_read_dir(self):
        meta = MetaPhoto(source_directory="../samples/", target_directory="/test/folder/", tag="TAG")
        meta._read_dir()
        self.assertListEqual(sorted(["../samples/astro.jpg"]), meta.raw_pictures)

    def test_read_meta(self):
        meta = MetaPhoto(source_directory="../samples/", target_directory="/test/folder/", tag="TAG")
        meta._read_dir()
        meta._read_meta()
        self.assertEqual("2008:11:22 19:29:04", meta.meta_pictures[0].get_date())

    @patch("MetaPhoto.MetaPhoto.copy2")
    @patch("MetaPhoto.MetaPhoto.makedirs")
    def test_copy_single_picture(self, mock_makedirs, mock_copy):
        meta = MetaPhoto(source_directory="../samples/", target_directory="/test/folder/", tag="TAG")
        meta._read_dir()
        meta._read_meta()
        meta._copy_picture(meta.meta_pictures[0])
        mock_makedirs.assert_called_once_with("/test/folder/2008_TAG")
        mock_copy.assert_called_once_with(Path("../samples/astro.jpg"),
                                          "/test/folder/2008_TAG/20081122-1929_TAG_astro.jpg")

    @patch("MetaPhoto.MetaPhoto.copy2")
    @patch("MetaPhoto.MetaPhoto.makedirs")
    def test_copy_picture(self, mock_makedirs, mock_copy):
        meta = MetaPhoto(source_directory="../samples/", target_directory="/test/folder/", tag="TAG")
        meta.copy()
        mock_makedirs.assert_called_once_with("/test/folder/2008_TAG")
        mock_copy.assert_called_once()
        mock_copy.assert_called_once_with(Path("../samples/astro.jpg"),
                                          "/test/folder/2008_TAG/20081122-1929_TAG_astro.jpg")

    def test_format_data(self):
        meta = MetaPhoto(source_directory="../samples/", target_directory="/test/folder/", tag="TAG")
        meta.date_format_file_name = "%Y%m%d-%H%M"
        original_date_as_str = "2008:11:22 19:29:04"
        mock_pic = MagicMock()
        mock_pic.get_date.return_value = original_date_as_str
        formatted_date = meta._get_formatted_date_for_file_name(mock_pic)
        self.assertEqual("20081122-1929", formatted_date, "Format the date")
