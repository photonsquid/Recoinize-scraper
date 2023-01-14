import json
import os

from src.arguments import check_safe_ouput, log_args, parse_args
from src.json import check_json_file, check_json_schema
from src.logger import set_logger
from src.scrape import scrape


# main can take arguments from the command line
def main():
    """Main function"""
    # parse the console arguments
    try:
        args = parse_args()
        logger = set_logger(args)
    except ValueError as e:
        print(e)
        return

    # check ouput overwriting
    check_safe_ouput(args, logger)

    logger.debug(log_args(args))

    # if 'scrape_only' is set, then scrape (override the json file if it exists), and exit
    # if 'scrape_only' is not set, then scrape and download the images

    images = scrape(logger, args)

    # download_images(images, logger, args)


if __name__ == "__main__":
    main()
