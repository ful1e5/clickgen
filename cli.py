import argparse
import os

from pkginfo import package_name, package_version, package_description
import clickgen


def main(name: str, config_dir: str, out_path: str, x11: bool, win: bool,
         archive: bool, logs: bool):
    clickgen.main(name=name,
                  config_dir=config_dir,
                  out_path=out_path,
                  x11=x11,
                  win=win,
                  archive=args.archive,
                  logs=logs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=package_description,
                                     add_help=False)

    parser.add_argument('-V',
                        '--version',
                        action='version',
                        version='%s-%s' % (package_name, package_version),
                        help='Display the version number and exit.')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        dest='logs',
                        help='Exec with verbose mode')
    parser.add_argument('-h',
                        '-?',
                        action='help',
                        help='Display the usage message and exit.')
    parser.add_argument('-n',
                        '--theme-name',
                        dest='theme_name',
                        metavar='string',
                        default=None,
                        help='Specified cursor-theme name')
    parser.add_argument(
        '-c',
        '--configs-dir',
        metavar='directory',
        dest='config_dir',
        default='-',
        help=
        'Find cursor config in the directory specified by dir. If not specified, the current directory is used.'
    )
    parser.add_argument(
        '-o',
        '--output-dir',
        metavar='directory',
        dest='output_dir',
        default='-',
        help=
        'output directory. If not specified, the current directory is used.')
    parser.add_argument('-x11',
                        action='store_true',
                        dest='x11',
                        help='generate theme for X11 System')
    parser.add_argument('-win',
                        action='store_true',
                        dest='win',\
                        help='generate theme for Windows System')
    parser.add_argument('--no-archive',
                        action='store_false',
                        dest='archive',
                        help='Generate cursor-theme without archive')

    args = parser.parse_args()

    if args.config_dir == '-':
        args.config_dir = os.getcwd()

    if args.output_dir == '-':
        args.output_dir = os.getcwd()

    main(name=args.theme_name,
         config_dir=args.config_dir,
         out_path=args.output_dir,
         x11=args.x11,
         win=args.win,
         archive=args.archive,
         logs=args.logs)
