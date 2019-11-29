from os import listdir
from os.path import isfile, join

from exif import Image


class MetaPhoto:
    """
    Copy images to a folder structure based on the creation date.
    Name the files based on date, a tag, and the original name.
    """
    def __init__(self, input_folder):
        self.input_folder = input_folder
        self.raw_pictures = []
        self.meta_pictures = []

    def _read_dir(self):
        """ Read all files from the input directory """
        self.raw_pictures = sorted(
            [join(self.input_folder, file) for file in listdir(self.input_folder) if
             isfile(join(self.input_folder, file))])

    def _read_meta(self):
        """ Convert the found files to objects handling exif information """
        self.meta_pictures = [MetaPicture(image) for image in self.raw_pictures]


class MetaPicture:
    """ Proxy for the exif.Image class"""
    def __init__(self, picture_path):
        self.picture_path = picture_path
        self.image = None
        self._read()

    def _read(self):
        with open(self.picture_path, 'rb') as file:
            self.image = Image(file)

    def _get_date(self):
        if hasattr(self.image, "datetime_original"):
            date = str(self.image.datetime_original)
        else:
            date = ""
        return date
