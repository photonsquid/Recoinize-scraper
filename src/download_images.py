import os
import urllib.request

from src.arguments import Arguments
from src.constants import IMAGES_FOLDER


def download_images(images, args: Arguments, logger):
    """Download images from a list of urls"""

    errors = []

    # create the output folder
    output_folder = os.path.join(args.root_folder, IMAGES_FOLDER)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    nb_of_images = len(images)

    # for each image, download it
    for i in range(nb_of_images):
        image = images[i]
        special_path = image["specialPath"]

        if (special_path is not None):
            image_folder = os.path.join(output_folder, special_path)

            # create the folder if it does not exist
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)
        else:
            image_folder = output_folder

        # get the image url
        url = image["url"]

        # get the image name
        particulartiy = image["particularity"]
        extension = image["imageExtension"]
        country_code = image["countryCode"]
        value = image["value"]

        if (particulartiy is None):
            image_name = f"{country_code}_{value}.{extension}"
        else:
            image_name = f"{country_code}_{value}_{particulartiy}.{extension}"

        # download the image
        image_path = os.path.join(image_folder, image_name)

        if os.path.exists(image_path):
            # remove the image if it already exists
            os.remove(image_path)

        try:
            logger.info(
                f"Downloading image {image_name} from {url} ({i + 1}/{nb_of_images})")
            urllib.request.urlretrieve(url, image_path)
        except Exception as e:
            logger.error(
                f"Error while downloading image {image_name} from {url}")
            logger.error(e)
            # save the url in the errors list
            errors.append(url)
            continue

    if len(errors) > 0:
        # save them in a file
        errors_file = os.path.join(output_folder, "errors.txt")
        with open(errors_file, "w") as f:
            f.write("\n".join(errors))
