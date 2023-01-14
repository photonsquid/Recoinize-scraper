import json
import os

import jsonschema
from jsonschema import validate

from src.error_messages import (JSON_FILE_INVALID, JSON_FILE_NOT_FOUND,
                                JSON_FILE_SCHEMA_INVALID,
                                JSON_FILE_SCHEMA_VALID, JSON_READING_ERROR,
                                JSON_SCHEMA_NOT_FOUND, JSON_WRITING_ERROR,
                                READING_ERROR, SAVING_ERROR)


def check_json_schema(json_file, logger):
    """Check if the json file respects the schema"""

    schma_path = './src/schema.json'
    try:
        # import schema from ./schema.json
        try:
            with open(schma_path) as f:
                schema = json.load(f)
        except:
            logger.error(JSON_SCHEMA_NOT_FOUND.format(schma_path))
            return False

        # read data from the json file
        try:
            with open(json_file, "r") as f:
                jsonData = json.load(f)
        except:
            logger.error(JSON_READING_ERROR.format(json_file))
            return False

        # check if the json file respects the schema
        validate(instance=jsonData, schema=schema)
        logger.debug(JSON_FILE_SCHEMA_VALID.format(json_file))

    except jsonschema.exceptions.ValidationError as err:
        logger.error(JSON_FILE_SCHEMA_INVALID.format(json_file))
        logger.error(err)
        return False
    return True


def check_json_file(json_path: str, logger) -> bool:
    """Check if the json file exists, and if it respects the schema"""
    # check if the json file exists
    if not os.path.isfile(json_path):
        logger.info(JSON_FILE_NOT_FOUND.format(json_path))
        return False

    # check if the json file is valid
    try:
        with open(json_path, "r") as f:
            json.load(f)
    except json.decoder.JSONDecodeError:
        logger.error(JSON_FILE_INVALID.format(json_path))
        return False

    return True


def read_json(json_file: str, logger) -> dict:
    """Read the json file and return a dict"""
    try:
        with open(json_file, "r") as f:
            jsonData = json.load(f)
        return jsonData
    except:
        logger.error(JSON_READING_ERROR.format(json_file))
        raise Exception(READING_ERROR)


def save_to_json(json_path: str, data: dict, logger) -> None:
    """Save the data to a json file"""
    try:
        logger.info("Saving data to {}".format(json_path))
        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)
    except:
        logger.error(JSON_WRITING_ERROR.format(json_path))
        raise Exception(SAVING_ERROR)
