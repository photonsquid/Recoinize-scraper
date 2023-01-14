import logging

from src.error_messages import JSON_WRONG_SCHEMA
from src.json import (check_json_file, check_json_schema, read_json,
                      save_to_json)


def check_json(json_file: str, logger: logging.Logger):
    # check if the json file exists
    if not check_json_file(json_file, logger):
        return 1

    # check if the json file respects the schema
    if not check_json_schema(json_file, logger):
        return 2

    return 0


def get_images(scraper, logger: logging.Logger, args):

    json_path = scraper.json_path
    json_data = {}
    need_to_scrape = False

    # if args.scrape_only, then do not read the json file, but scrape the data
    if args.scrape_only:
        need_to_scrape = True
        logger.info(
            "-s (--scrape-only) flag is set, scraping data without reading any json file...")
    else:
        # check if the json file is valid
        isFile = check_json(json_path, logger)
        if isFile == 1:
            # file is not present, we need to scrape data, and generate the json file
            need_to_scrape = True
        elif isFile == 2:
            # file is present, but does not respect the schema
            raise Exception(JSON_WRONG_SCHEMA)
        else:
            # file is present, and respects the schema
            need_to_scrape = False

    if need_to_scrape:
        # file is not present, we need to scrape data, and generate the json file
        logger.info("Scraping data...")
        # scrape data from the website
        json_data = scraper.scrape()

        # save the data to a json file
        save_to_json(json_path, json_data, logger)
    else:
        # file is present, and respects the schema
        # read data from json file
        logger.info("Reading data from json file...")
        json_data = read_json(json_path, logger)

    return json_data


def scrape(scraper, logger, args):
    """Scrape the data from the website"""

    # get lis of images
    jsonData = get_images(scraper, logger, args)

    # for each image, download it
    return jsonData
