from datetime import datetime
from os import listdir, makedirs
from os.path import isfile, join
from pathlib import Path
from shutil import copy2

from exif import Image


class MetaPhoto:
    """
    Copy images to a folder structure based on the creation date.
    Name the files based on date, a tag, and the original name.
    """

    def __init__(self, source_directory: str, target_directory: str, tag: str):
        self.source_directory = Path(source_directory)
        self.target_directory = Path(target_directory)
        self.tag = tag

        self.raw_pictures = []
        self.meta_pictures = []
        self.date_format_file_name = "%Y%m%d-%H%M"
        self.date_format_folder = "%Y"
        self.exif_date_format = "%Y:%m:%d %H:%M:%S"

        self._target_path = None

    def _read_dir(self):
        """ Read all files from the input directory """
        self.raw_pictures = sorted(
            [join(self.source_directory, file) for file in listdir(self.source_directory) if
             isfile(join(self.source_directory, file))])

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
        new_file_name = f"{formatted_date}_{self.tag}_{file_name}"
        return new_file_name

    def _build_new_folder_name(self, picture):
        date = self._get_date_object(picture.get_date())

        return f"{date.strftime(self.date_format_folder)}_{self.tag}"

    def _build_and_create_target_path(self, picture):
        new_file_name = self._build_new_file_name(picture)
        new_folder_name = join(self.target_directory, self._build_new_folder_name(picture))
        try:
            makedirs(new_folder_name)
            print(f"Folder {new_folder_name} created")
        except FileExistsError:
            pass
        self.target_path = join(new_folder_name, new_file_name)

    def _copy_picture(self, picture: 'MetaPicture'):
        """ Move a given MetaPicture to a new directory. Rename it based on it's date and tag """
        self._build_and_create_target_path(picture)
        print(f"Copy file {picture.picture_path} to {self.target_path}")
        copy2(picture.picture_path, self.target_path)

    def copy(self):
        self._read_dir()
        self._read_meta()
        for picture in self.meta_pictures:
            self._copy_picture(picture)


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
