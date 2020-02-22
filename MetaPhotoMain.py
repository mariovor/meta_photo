import getopt
import sys

from MetaPhoto.MetaPhoto import MetaPhoto


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:t:", ["input_dir=", "output_dir=", "tag="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    source_directory = None
    target_directory = None
    tag = None
    for option, arg in opts:
        if option == "-i":
            source_directory = arg
        elif option == "-o":
            target_directory = arg
        elif option == "-t":
            tag = arg
        else:
            assert False, "unhandled option"

    meta = MetaPhoto(source_directory=source_directory, target_directory=target_directory, tag=tag)
    meta.copy()


if __name__ == "__main__":
    main()
