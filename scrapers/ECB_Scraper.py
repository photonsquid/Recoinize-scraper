from playwright.sync_api import sync_playwright

from scrapers.Scraper import Scraper

COIN_VALUES = [
    "2euro",
    "1euro",
    "50cents",
    "20cents",
    "10cents",
    "5cents",
    "2cents",
    "1cent"
]

NAME = "ECB"
BASE_URL = "https://www.ecb.europa.eu/euro/coins/$value$/html/index.en.html"


class ECB_Scraper(Scraper):
    def __init__(self, args, logger):
        super().__init__(args, logger, NAME, BASE_URL)

    def scrape(self) -> dict:
        images = []

        with sync_playwright() as p:
            browser_type = p.firefox
            browser = browser_type.launch()
            page = browser.new_page()
            # for each coin value, scrape the data
            for coin_value in COIN_VALUES:
                # format the url
                url = self.base_url.replace("$value$", coin_value)

                # get root of the url:
                # for example, if url is https://www.ecb.europa.eu/euro/coins/2euro/html/index.en.html
                # then root is https://www.ecb.europa.eu/
                root = "/".join(url.split("/")[:3])

                self.logger.info(
                    "Scraping data for coin value {}".format(coin_value))
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
                            url = root + img.get_attribute("src")
                            imageName = url.split("/")[-1]
                            imageWithoutExtension = ".".join(
                                imageName.split(".")[:-1])
                            particularity = imageWithoutExtension.split(
                                "_")[-1]
                            # add a new object to src list
                            src.append({
                                "url": url,
                                "particularity": particularity
                            })

                    else:
                        src = [
                            {
                                "url": root + imgs[0].get_attribute("src"),
                                "particularity": None
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
                        img["value"] = coin_value
                        img["special_path"] = self.special_path

                    # append src to images and flatten the list
                    images.extend(src)

        with open("test_countries.txt", "w") as f:
            for img in images:
                f.write(img["countryName"] + ": " + img["countryCode"] + "\n")
        return images
