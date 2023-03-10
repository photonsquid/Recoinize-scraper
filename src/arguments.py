import argparse
import logging
import os
from os.path import isdir

from src.constants import DEFAULT_ROOT_FOLDER, PROG_VERSION
from src.error_messages import FOLDER_CREATED


class Arguments:
    def __init__(self):
        scrape_only = False
        json_file = None
        root_folder = None
        debug = False
        quiet = False
        json_path = None
        images_folder = None


def define_args() -> argparse.ArgumentParser:
    # parse the console arguments
    parser = argparse.ArgumentParser(description="Coin image scraper")

    parser.add_argument("-r", "--root", action="store_true",
                        default=DEFAULT_ROOT_FOLDER,
                        help="The root folder to save the images to")
    parser.add_argument("-s", "--scrape-only", action="store_true",
                        default=False,
                        help="Only scrape the data, don't download the images")
    parser.add_argument("-v", "--version", action="version",
                        version=f"%(prog)s {PROG_VERSION}")
    parser.add_argument("-d", "--debug",
                        default=False,
                        action="store_true", help="Enable debug mode")
    parser.add_argument("-q", "--quiet",
                        default=False,
                        action="store_true", help="Enable quiet mode, no output")

    return parser


def check_safe_ouput(args: Arguments, logger: logging.Logger):
    """Check if the arguments are valid"""

    # check if root folder exists, else create it
    if not isdir(args.root_folder):
        os.makedirs(args.root_folder)
        logging.info(FOLDER_CREATED.format(args.root_folder))


def log_args(args: Arguments) -> str:
    """Log the arguments"""

    scrape_only = "True" if args.scrape_only else "False"
    debug = "True" if args.debug else "False"
    quiet = "True" if args.quiet else "False"
    root_folder = args.root_folder

    return f"\n\tScrape only: {scrape_only}\n\tDebug: {debug}\n\tQuiet: {quiet}\n\tRoot folder: {root_folder}"


def parse_args() -> Arguments:
    parser = define_args()
    args = parser.parse_args()

    safe_args = Arguments()

    safe_args.scrape_only = args.scrape_only
    safe_args.debug = args.debug
    safe_args.quiet = args.quiet
    safe_args.root_folder = args.root

    return safe_args
