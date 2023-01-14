import datetime

from playwright.sync_api import sync_playwright

from scrapers.Scraper import Scraper

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
                    countryName = h3.inner_text()
                    # get the img
                    imgs = box.query_selector_all("img")

                    # if there is several src,
                    # split url by "/" abd get last one
                    # remove extension (split by "." and get all except last one, join with ".")
                    # get particularity (split by "_" and get last one)

                    src = []

                    if len(imgs) > 1:
                        for img in imgs:
                            img_url = img.get_attribute("src")
                            if (img_url != ""):
                                src.append(
                                    {
                                        "url": img_url,
                                        "particularity": "com_" + year
                                    }
                                )
                    else:
                        src = [
                            {
                                "url": imgs[0].get_attribute("src"),
                                "particularity": "com_" + year
                            }
                        ]
                    # for each src, get country code, and extension
                    for img in src:
                        url = img["url"]
                        countryCode = url.split("/")[-2]
                        extension = url.split("/")[-1].split(".")[-1]

                        img["countryCode"] = countryCode
                        img["imageExtension"] = extension
                        img["countryName"] = countryName
                        img["value"] = "2euro"

                    # append src to images and flatten the list
                    images.extend(src)
        # save to test.txt file all urls
        with open("test.txt", "w") as f:
            for img in images:
                f.write(img["url"] + "\n")
        return images
