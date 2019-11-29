from unittest import TestCase

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
