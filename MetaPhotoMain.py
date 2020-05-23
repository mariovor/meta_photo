import getopt
import sys

from MetaPhoto.MetaPhoto import MetaPhoto
from MetaPhoto.MetaPhotoGui import init_gui


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:t:g", ["input_dir=", "output_dir=", "tag=", "gui"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    source_directory = None
    target_directory = None
    tag = None
    gui_set = False
    for option, arg in opts:
        if option == "-i":
            source_directory = arg
        elif option == "-o":
            target_directory = arg
        elif option == "-t":
            tag = arg
        elif option == "-g":
            gui_set = True
        else:
            assert False, "unhandled option"

    # Run Gui
    if gui_set:
        init_gui()
        sys.exit(0)

    if source_directory is None or target_directory is None or tag is None:
        print("Please state a source directory, target directory, and a tag")
        sys.exit(2)

    meta = MetaPhoto(source_directory=source_directory, target_directory=target_directory, tag=tag)
    meta.copy()


if __name__ == "__main__":
    main()
