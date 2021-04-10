#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Tom Riat"
__version__ = "1.0.0"
__license__ = "GNU General Public License v3.0"

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

parser = argparse.ArgumentParser(description="Update liquidations values for the LHPControl GUI")
parser.add_argument(
    "--config-file",
    type=Path,
    default="varPairs.json",
    dest="config_file",
    help="Path to LHPC config file (usually called `varPairs.json`)",
)
parser.add_argument(
    "--debug",
    action="store_true",
    dest="debug",
    help="Give additional debug output",
)

liquididation_datas: List[Dict[str, Any]] = [{}]


def get_liquidations_data() -> None:
    """Parse the data coming from https://liquidation.wtf/ to update the coins' avg liquidation
    price"""
    response = requests.get("https://liquidation.wtf/api/v0/liquidations/by_coin")
    logger.debug(response.status_code, response.text)
    response.raise_for_status()

    global liquididation_datas
    liquididation_datas = response.json()["data"]


def get_liquidation_value(coin_name: str, value: str) -> Optional[float]:
    """Get a specific coin liquidation value"""
    logger.debug(f"coin: {coin_name}, value: {value}")
    for data in liquididation_datas:
        if data["symbol"] == coin_name:
            return data[value]
    logger.debug("No liquidation value found")
    return None


def load_config_file(config_file: Path) -> Dict[str, Any]:
    """Parse the configuration file of LHPControl and load its values"""
    config_data = None
    logger.debug(f"file path: {config_file.name}")
    with open(config_file, "r") as file:
        config_data = json.load(file)
    logger.debug(f"file data: {config_data}")

    if config_data is None:
        raise ValueError("Could not load config file data")

    return config_data


def update_coin_configuration(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update the configuration with the latest coin liquidation values"""
    for coin in config_data["coins"]:
        new_lickvalue = get_liquidation_value(coin["symbol"], "average_usdt")
        if new_lickvalue is None:
            logger.warning(f"{coin['symbol']} has not been updated, no liquidation value found")
        logger.info(f"{coin['symbol']} \t {coin['lickvalue']} \t -> \t {new_lickvalue}")
        coin["lickvalue"] = f"{new_lickvalue}"
    return config_data


def save_new_configuration(config_data: Dict[str, Any], config_file: Path) -> None:
    """Update the configuration document with the new values"""
    logger.debug(f"new config data: {config_data}")
    with open(config_file, "w") as file:
        json.dump(config_data, file, indent=4)


def main(config_file: Path) -> None:
    get_liquidations_data()
    config_data = load_config_file(config_file)
    new_configuration = update_coin_configuration(config_data)
    save_new_configuration(new_configuration, config_file)


if __name__ == "__main__":
    logger.info("======= Starting to update the coins =======")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.debug(args)

    if not args.config_file.exists():
        raise ValueError(f"Config file does not exists at path {args.config_file.name}")

    try:
        main(config_file=Path(args.config_file))
    except Exception as e:
        logger.exception(e)
        logger.info("======= Update failed =======")
    else:
        logger.info("======= Update done =======")
