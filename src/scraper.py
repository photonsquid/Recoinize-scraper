
import logging

from playwright.sync_api import sync_playwright

from src.json import save_to_json


def main(_url: str, coin_values: list, logger: logging.Logger) -> list:
    with sync_playwright() as p:
        browser_type = p.firefox
        browser = browser_type.launch()
        page = browser.new_page()

        images = []

        # for each coin value, scrape the data
        for coin_value in coin_values:
            # format the url
            url = _url.replace("$value$", coin_value)

            # get root of the url:
            # for example, if url is https://www.ecb.europa.eu/euro/coins/2euro/html/index.en.html
            # then root is https://www.ecb.europa.eu/
            root = "/".join(url.split("/")[:3])

            logger.info("Scraping data for coin value {}".format(coin_value))
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
                        particularity = imageWithoutExtension.split("_")[-1]
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

                # append src to images and flatten the list
                images.extend(src)

        browser.close()
    return images
