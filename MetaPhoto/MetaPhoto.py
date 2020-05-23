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
        self.meta_pictures = []
        for image in self.raw_pictures:
            try:
                self.meta_pictures.append(MetaPicture(image))
            except CannotReadImageException:
                print("Skipping file " + image)

    def _get_date_object(self, date_string):
        """ Convert the date string into a date object using configured exif date format """
        date = datetime.strptime(date_string, self.exif_date_format)
        return date

    def _get_formatted_date_for_file_name(self, picture):
        """ Return a string containing the creation date using the configured format """
        # Get data and format
        date_string = picture.get_date()
        date = self._get_date_object(date_string)
        formatted_date = date.strftime(self.date_format_file_name)
        return formatted_date

        return date.strftime(self.date_format_file_name)

    def _build_new_file_name(self, picture):
        """ Create a name for the file using date, tag and the original file name """
        file_name = picture.picture_path.name
        formatted_date = self._get_formatted_date_for_file_name(picture)
        # Build new file name
        new_file_name = f"{formatted_date}_{self.tag}_{file_name}"
        return new_file_name

    def _build_new_folder_name(self, picture):
        """ Create the name for the folder for the new fies. Use date and the tag """
        date = self._get_date_object(picture.get_date())

        return f"{date.strftime(self.date_format_folder)}_{self.tag}"

    def _build_and_create_target_path(self, picture):
        """ Create the full target path for the new file. Create folders if necessary """
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
        copy2(picture.picture_path, self.target_path)

    def copy(self):
        """ Read the source directory and copy the files to the target directory """
        failed = False
        self._read_dir()
        self._read_meta()
        for picture in self.meta_pictures:
            try:
                self._copy_picture(picture)
            except Exception as e:
                failed = True
                print(f"Could not copy file {picture.picture_path} because of {e}")
            if failed:
                self._copy_failed_picture(picture)

    def _copy_failed_picture(self, picture):
        new_folder_name = self._build_and_create_failed_target_path()
        copy2(picture.picture_path, join(new_folder_name, picture.picture_path.name))

    def _build_and_create_failed_target_path(self):
        new_folder_name = join(self.target_directory, "failed_" + self.tag)
        try:
            makedirs(new_folder_name)
            print(f"Folder {new_folder_name} created")
        except FileExistsError:
            pass
        return new_folder_name


class MetaPicture:
    """ Proxy for the exif.Image class"""

    def __init__(self, picture_path):
        self.picture_path = Path(picture_path)
        self.image = None
        self._read()

    def _read(self):
        try:
            with open(self.picture_path, 'rb') as file:
                self.image = Image(file)
        except AssertionError as e:
            raise CannotReadImageException from e

    def get_date(self):
        if hasattr(self.image, "datetime_original"):
            date = str(self.image.datetime_original)
        else:
            date = ""
        return date


class CannotReadImageException(Exception):
    pass
