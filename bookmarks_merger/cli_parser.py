import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--list', action='store_true', help='Print titles and urls of all bookmarks')
    group.add_argument('--merge', action='store_true', help='Merge bookmarks into one file')
    group.add_argument('--sort', action='store_true', help='Sort bookmark folders alphabetically')

    parser.add_argument('--clean', action='store_true', help='Remove duplicated bookmarks and merge duplicated folders')
    parser.add_argument('--files', dest='files', help='List of files to process', nargs='+', required=True)
    parser.add_argument('--output', dest='output', help='Output file', nargs='+', required=False)
    return parser.parse_args()
