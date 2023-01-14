<!-- omit in toc -->
# Coins parser

A simple parser for euro coins images.

<!-- omit in toc -->
## Table of Contents

- [Context](#context)
- [Description](#description)
- [Installation](#installation)
- [Usages](#usages)
- [Arguments](#arguments)
- [Add a scraper](#add-a-scraper)
- [JSON file](#json-file)
- [Special coins](#special-coins)
- [List of countries](#list-of-countries)
- [List of coins](#list-of-coins)

## Context

For a [deep learning project](https://huggingface.co/BSoDium/coin-face-recognition),
we need a data set of all different euro coins.
The main idea is to generate a lot of different photographs in [Blender](https://www.blender.org/) (different lighting, camera angles, background, focus distances, etc.)
For this we need to dynamically build all coins in Blender, and for this, we need textures of all these coins.
Here we are, scraping all this images.

## Description

This script can scrape image URLs from different websites, and download them.
Some scrapers are already implemented, but you can easily add your own
(see [Add a scraper](#add-a-scraper)).

Currently, there are two scrapers implemented:

- [European Central Bank for regular coins](https://www.ecb.europa.eu/euro/coins/html/index.en.html).
- [European Central Bank for 2€ commemorative coins](https://www.ecb.europa.eu/euro/coins/comm/html/index.en.html).

Images are downloaded in the following folder structure:

```bash
{root}/coins/{countryCode}_{value}_{particularity}.{imageExtension}
```

Where:

- `{root}` is the root folder given as argument (cf. [here](#-r---root))
- `{countryCode}` is the country code in two letters of the coin (e.g. `fr` for France, `ad` for Andorra, etc.)
- `{value}` is the value of the coin (e.g. 1euro, 2cents, etc.), cf. [this list](#regular-coins)
- `{particularity}` is the particularity of the coin (e.g. 2019, 2018, 2017, etc.) or null if there is only one coin for this country (cf. [here](#special-coins))
- `{imageExtension}` is the extension of the image (`jpg`, `.png`, etc.) from the scraped website.

Examples of images:

- `./coins/va_50cents_2017.jpg`
- `./coins/lv_1euro.jpg`
- `./coins/va_10cents_SedeVacante.jpg`

## Installation

It depends on the script you want to execute. If you already get JSON files,
and don't want to do the scraping part, you can simply run:

```bash
pip install -r requirements-downloader.txt
```

Else, you need to install [playwright](https://playwright.dev/):
(`requirements-scraper.txt`) includes `requirements-downloader.txt`, so you don't need to install it twice.

```bash
pip install -r requirements-scraper.txt
```

## Usages

If, for example, you want to provide the root folder argument, you can do it like this:

```bash
python ./main.py -r ./images
```

## Arguments

This is the list of different arguments that can be passed to the command.

| short | long     | default      | short description                                                  |
| ----- | -------- | ------------ | ------------------------------------------------------------------ |
| -r    | --root   | `"./images"` | root folder where images will be downloaded, and JSON file created |
| -s    | --scrape | `false`      | if true, no image download, only JSON scraping                     |
| -h    | --help   |              | display help                                                       |
| -d    | --debug  | `false`      | if true, debug mode (lot of logs)                                  |
| -q    | --quiet  | `false`      | if true, quiet mode (no output)                                    |

<!-- omit in toc -->
### `-r`, `--root`

This is the root folder that contains the JSON file.
All images will be downloaded in `{root}/coins/`

<!-- omit in toc -->
### `-s`, `--scrape`

If true, no image download, only JSON scraping.
If a JSON file (`{root}/{json}`) file already exists, it will override it.

## Add a scraper

## JSON file

When data is scraped, a new JSON file is created containing data for each image.
It must respect the schema defined in `./schema.json`:

Example of JSON file:

```json
[
    {
        "countryCode": "va",
        "value": "50cents",
        "particularity": "2017",
        "url": "https://www.ecb.europa.eu/euro/coins/html/va/50c_2017.en.html"
    },
]
```

| field           | type               | description                                                      |
| --------------- | ------------------ | ---------------------------------------------------------------- |
| `countryCode`   | `string`           | country code in two letters, cf. [this list](#list-of-countries) |
| `value`         | `string`           | value of the coin, cf. [this list](#regular-coins)               |
| `particularity` | `string` or `null` | particularity of the coin, cf. [here](#special-coins)            |
| `url`           | `uri` (`string`)   | URL of the scraped website                                       |

## Special coins

Some countries have only one coin since 2002, and some have more than one.
For example, Vatican City has a new coin for each pope.
So, for these countries, the particularity is saved. It can be a year, or a name.
It is null if there is only one coin.

## List of countries

You can find the list of countries in this file.

## List of coins

You can find the list of all euro coins in this file.

<!-- omit in toc -->
### Regular coins

| coin values |
| ----------- |
| `2euro`     |
| `1euro`     |
| `50cents`   |
| `20cents`   |
| `10cents`   |
| `5cents`    |
| `2cents`    |
| `1cent`     |
