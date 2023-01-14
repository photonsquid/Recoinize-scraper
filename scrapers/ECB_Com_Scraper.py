import datetime

from playwright.sync_api import sync_playwright

from scrapers.ECB_country_names import COUNTRY_NAMES
from scrapers.Scraper import Scraper
from src.error_messages import COUNTRY_CODE_NOT_FOUND

NAME = "ECB_COM"
BASE_URL = "https://www.ecb.europa.eu/euro/coins/comm/html/comm_$year$.en.html"
FIRST_YEAR = 2004
# -1 because we don't have the data for the current year
LAST_YEAR = datetime.date.today().year - 1


class ECB_Com_Scraper(Scraper):
    def __init__(self, args, logger):
        super().__init__(args, logger, NAME, BASE_URL)

    def scrape(self) -> dict:
        images = []

        with sync_playwright() as p:
            browser_type = p.firefox
            browser = browser_type.launch()
            page = browser.new_page()
            # get current year
            for year_int in range(FIRST_YEAR, LAST_YEAR + 1):
                year = str(year_int)
                # format the url
                url = self.base_url.replace("$year$", year)

                # get root of the url:
                # for example, if url is https://www.ecb.europa.eu/euro/coins/2euro/html/index.en.html
                # then root is https://www.ecb.europa.eu/
                root = "/".join(url.split("/")[:3])

                self.logger.info(
                    "Scraping data for coin value {}".format(year))
                page.goto(url)
                # wait for the data to be loaded
                page.wait_for_selector(".coins")
                # get the data
                data = page.query_selector_all(".box")
                # in all these boxes, query_selector h3, and querySelectorAll("img")
                # for each box, get the h3, and the img

                for box in data:
                    # get the h3
                    h3 = box.query_selector("h3")
                    # get the text of the h3
                    country_name = h3.inner_text()

                    # get the img
                    imgs = box.query_selector_all("img")

                    # for each img, remove all one that have src=""

                    for img in imgs:
                        img_url = img.get_attribute("src")
                        if (img_url == ""):
                            imgs.remove(img)

                    # if there is several src,
                    # split url by "/" abd get last one
                    # remove extension (split by "." and get all except last one, join with ".")
                    # get particularity (split by "_" and get last one)

                    src = []

                    part = "com_" + year

                    if len(imgs) > 1:
                        for img in imgs:
                            img_url = img.get_attribute("src")
                            if (img_url != ""):
                                # get country name
                                # split by "_" and get last one
                                country_name = img_url.split("/")[-1]
                                # remove extension: split by "." and get all except last one, join with "."
                                country_name = ".".join(
                                    country_name.split(".")[:-1])
                                # get country code*
                                [country_code, parti] = self._find_country_code(
                                    country_name, img_url)
                                if parti != "":
                                    parti = part + "_" + parti
                                else:
                                    parti = part

                                src.append(
                                    {
                                        "countryCode": country_code,
                                        "countryName": country_name,
                                        "url": root + img_url,
                                        "particularity": "eu_" + parti
                                    }
                                )
                    else:
                        local_url = imgs[0].get_attribute("src")
                        [country_code, parti] = self._find_country_code(
                            country_name, local_url)
                        if parti != "":
                            parti = part + "_" + parti
                        else:
                            parti = part
                        src = [
                            {
                                "countryCode": country_code,
                                "countryName": country_name,
                                "url": root + local_url,
                                "particularity": parti
                            }
                        ]
                    # for each src, get country code, and extension
                    if (len(src) == 0):
                        self.logger.error("No image found for {}".format(url))
                        continue
                    for img in src:
                        url = img["url"]

                        extension = url.split("/")[-1].split(".")[-1]

                        img["imageExtension"] = extension
                        img["value"] = "2euro"
                        img["specialPath"] = self.special_path

                    # append src to images and flatten the list
                    images.extend(src)

        return images

    def _find_country_code(self, country_name: str, url) -> str:
        country_code = ""
        particularity = ""
        country_names = country_name.split("_")
        # for each word in country_names, check if it is in the list of country names
        # if there is one, keep it, and keep all words after it as particularity

        for i in range(len(country_names)):
            word = country_names[i]

            for country in COUNTRY_NAMES:
                if word in country["long_names"]:
                    country_code = country["code"]
                    particularity = "_".join(country_names[i + 1:])
                    break
            if country_code != "":
                break
        if country_code == "":
            self.logger.error(COUNTRY_CODE_NOT_FOUND.format(country_name))
            self.logger.error(url)
            country_code = "XX"

        return [country_code, particularity]

        # for country in COUNTRY_NAMES:
        #     if country_name in country["long_names"]:
        #         country_code = country["code"]
        #         break
        # return country_code
