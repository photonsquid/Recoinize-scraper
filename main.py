from scrapers.ECB_Com_Scraper import ECB_Com_Scraper
from scrapers.ECB_Scraper import ECB_Scraper
from src.arguments import check_safe_ouput, log_args, parse_args
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

    scrapers = [
        ECB_Com_Scraper(args, logger),
    ]

    # for each scrapers, scrape
    for scraper in scrapers:
        images = scrape(scraper, logger, args)
        # download the images


if __name__ == "__main__":
    main()
