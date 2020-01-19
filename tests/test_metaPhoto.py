from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from MetaPhoto.MetaPhoto import MetaPhoto


class TestMetaPhoto(TestCase):
    def test_read_dir(self):
        meta = MetaPhoto("../samples/")
        meta._read_dir()
        self.assertListEqual(sorted(["../samples/astro.jpg"]), meta.raw_pictures)

    def test_read_meta(self):
        meta = MetaPhoto("../samples/")
        meta._read_dir()
        meta._read_meta()
        self.assertEqual("2008:11:22 19:29:04", meta.meta_pictures[0]._get_date())

    @patch("MetaPhoto.MetaPhoto.move")
    def test_move_picture(self, mock_copy):
        meta = MetaPhoto("../samples/")
        meta._read_dir()
        meta._read_meta()
        meta._move_picture(meta.meta_pictures[0], "/test/folder/")
        mock_copy.assert_called_once()
        mock_copy.assert_called_once_with(Path("../samples/astro.jpg"), "/test/folder/2008:11:22 19:29:04_astro.jpg")
