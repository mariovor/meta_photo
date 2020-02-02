from datetime import datetime
from os import listdir
from os.path import isfile, join
from pathlib import Path
from shutil import move

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
        self.date_format_file_name = "%Y%m%d-%H%M"
        self.date_format_folder = "%Y"
        self.exif_date_format = "%Y:%m:%d %H:%M:%S"

    def _read_dir(self):
        """ Read all files from the input directory """
        self.raw_pictures = sorted(
            [join(self.input_folder, file) for file in listdir(self.input_folder) if
             isfile(join(self.input_folder, file))])

    def _read_meta(self):
        """ Convert the found files to objects handling exif information """
        self.meta_pictures = [MetaPicture(image) for image in self.raw_pictures]

    def _get_date_object(self, date_string):
        date = datetime.strptime(date_string, self.exif_date_format)
        return date

    def _get_formatted_date_for_file_name(self, picture):
        # Get data and format
        date_string = picture.get_date()
        date = self._get_date_object(date_string)
        formatted_date = date.strftime(self.date_format_file_name)
        return formatted_date

        return date.strftime(self.date_format_file_name)

    def _build_new_file_name(self, picture):
        file_name = picture.picture_path.name
        formatted_date = self._get_formatted_date_for_file_name(picture)
        # Build new file name
        new_file_name = f"{formatted_date}_{file_name}"
        return new_file_name

    def _build_new_folder_name(self, picture):
        date = self._get_date_object(picture.get_date())

        return date.strftime(self.date_format_folder)

    def _build_target_path(self, picture, target_directory):
        new_file_name = self._build_new_file_name(picture)
        new_folder_name = self._build_new_folder_name(picture)
        target_path = join(target_directory, new_folder_name, new_file_name)
        return target_path

    def _move_picture(self, picture: 'MetaPicture', target_directory: Path):
        """ Move a given MetaPicture to a new directory. Rename it based on it's date """
        target_path = self._build_target_path(picture, target_directory)
        move(picture.picture_path, target_path)


class MetaPicture:
    """ Proxy for the exif.Image class"""

    def __init__(self, picture_path):
        self.picture_path = Path(picture_path)
        self.image = None
        self._read()

    def _read(self):
        with open(self.picture_path, 'rb') as file:
            self.image = Image(file)

    def get_date(self):
        if hasattr(self.image, "datetime_original"):
            date = str(self.image.datetime_original)
        else:
            date = ""
        return date
