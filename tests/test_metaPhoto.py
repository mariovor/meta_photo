from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from MetaPhoto.MetaPhoto import MetaPhoto, MetaPicture


class TestMetaPhoto(TestCase):
    def test_read_dir(self):
        meta = MetaPhoto("../samples/")
        meta._read_dir()
        self.assertListEqual(sorted(["../samples/astro.jpg"]), meta.raw_pictures)

    def test_read_meta(self):
        meta = MetaPhoto("../samples/")
        meta._read_dir()
        meta._read_meta()
        self.assertEqual("2008:11:22 19:29:04", meta.meta_pictures[0].get_date())

    @patch("MetaPhoto.MetaPhoto.move")
    def test_move_picture(self, mock_copy):
        meta = MetaPhoto("../samples/")
        meta._read_dir()
        meta._read_meta()
        meta._move_picture(meta.meta_pictures[0], "/test/folder/")
        mock_copy.assert_called_once()
        mock_copy.assert_called_once_with(Path("../samples/astro.jpg"), "/test/folder/2008/20081122-1929_astro.jpg")

    def test_format_data(self):
        meta = MetaPhoto("../samples/")
        meta.date_format_file_name = "%Y%m%d-%H%M"
        original_date_as_str = "2008:11:22 19:29:04"
        formatted_date = meta._format_date(original_date_as_str)
        self.assertEqual("20081122-1929", formatted_date, "Format the date")
