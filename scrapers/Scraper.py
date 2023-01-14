
import os
from abc import ABC, abstractmethod

from playwright.sync_api import sync_playwright

from src.error_messages import (CHANGING_JSON_PATH, SCRAPER_BASE_URL_NOT_SET,
                                SCRAPER_NAME_NOT_SET)


class Scraper(ABC):
    __json_filename = None
    __json_path = None
    __special_path = None
    __name = None
    __base_url = None
    __args = None
    __logger = None

    def __init__(self, args, logger, name, base_url, special_path=None):
        self.__args = args
        self.__logger = logger
        self.__name = name
        self.__base_url = base_url
        self.special_path = special_path

        if (self.name is None):
            raise ValueError(SCRAPER_NAME_NOT_SET)

        if (self.base_url is None):
            raise ValueError(SCRAPER_BASE_URL_NOT_SET)

        self.json_filename = "{}.json".format(self.name)

    @abstractmethod
    def scrape(self) -> dict:
        pass

    @property
    def json_filename(self):
        return self.__json_filename

    @json_filename.setter
    def json_filename(self, json_filename):
        self.__json_filename = json_filename

        # update json_path
        root = self.args.root_folder
        if (self.special_path is not None):
            root = os.path.join(root, self.special_path)

        self.json_path = os.path.join(root, self.json_filename)

    @property
    def json_path(self):
        return self.__json_path

    @json_path.setter
    def json_path(self, json_path):
        self.__json_path = json_path

    @property
    def name(self):
        return self.__name

    @property
    def base_url(self):
        return self.__base_url

    @property
    def page(self):
        return self.__page

    @property
    def browser(self):
        return self.__browser

    @property
    def args(self):
        return self.__args

    @property
    def logger(self):
        return self.__logger

    @property
    def special_path(self):
        return self.__special_path

    @special_path.setter
    def special_path(self, special_path):
        self.__special_path = special_path
        root = self.args.root_folder
        # update json_path
        if (self.special_path is not None):
            root = os.path.join(root, self.special_path)

        self.json_path = os.path.join(root, self.name)
        self.logger.debug(CHANGING_JSON_PATH.format(self.json_path))
