#!/usr/bin/env python3
"""Update liquidations values for the LHPControl GUI"""

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
    "--add-liq-percentage",
    type=float,
    default="0.0",
    dest="liq_percentage",
    help=(
        "Add a percentage to the liq value of each coin. e.g: add percentage = 10, liq value = "
        "1000, coin liq value will be set at 1100"
    ),
)
parser.add_argument(
    "--debug",
    action="store_true",
    dest="debug",
    help="Give additional debug output",
)

LIQUIDATION_DATAS: List[Dict[str, Any]] = [{}]


def get_liquidations_data() -> None:
    """Parse the data coming from https://liquidation.wtf/ to update the coins' avg liquidation
    price"""
    response = requests.get("https://liquidation.wtf/api/v0/liquidations/by_coin")
    logger.debug(response.status_code, response.text)
    response.raise_for_status()

    global LIQUIDATION_DATAS  # pylint: disable=global-statement
    LIQUIDATION_DATAS = response.json()["data"]


def get_liquidation_value(coin_name: str, value: str) -> Optional[float]:
    """Get a specific coin liquidation value"""
    logger.debug("coin: %s, value: %s", coin_name, value)
    for data in LIQUIDATION_DATAS:
        if data["symbol"] == coin_name:
            return data[value]
    logger.debug("No liquidation value found")
    return None


def load_config_file(config_file: Path) -> Dict[str, Any]:
    """Parse the configuration file of LHPControl and load its values"""
    config_data = None
    logger.debug("file path: %s", config_file.name)
    with open(config_file, "r") as file:
        config_data = json.load(file)
    logger.debug("file data: %s", config_data)

    if config_data is None:
        raise ValueError("Could not load config file data")

    return config_data


def update_coin_configuration(config_data: Dict[str, Any], liq_percentage: float) -> Dict[str, Any]:
    """Update the configuration with the latest coin liquidation values"""
    for coin in config_data["coins"]:
        new_lickvalue = get_liquidation_value(coin["symbol"], "average_usdt")
        if new_lickvalue is None:
            logger.warning(
                "%s has not been updated, no liquidation value found. Old value is kept",
                coin["symbol"],
            )
            continue
        if liq_percentage > 0:
            new_lickvalue = new_lickvalue + (new_lickvalue * liq_percentage / 100)
        new_lickvalue = round(new_lickvalue)
        percent_change = get_percent_change(int(coin["lickvalue"]), new_lickvalue)
        logger.info("%s \t %s \t -> \t %s (%s)",
                    coin["symbol"],
                    coin["lickvalue"],
                    new_lickvalue,
                    percent_change)
        coin["lickvalue"] = f"{new_lickvalue}"
    return config_data


def save_new_configuration(config_data: Dict[str, Any], config_file: Path) -> None:
    """Update the configuration document with the new values"""
    logger.debug("new config data: %s", config_data)
    with open(config_file, "w") as file:
        json.dump(config_data, file, indent=4)


def main(config_file: Path, liq_percentage: float) -> None:
    get_liquidations_data()
    config_data = load_config_file(config_file)
    new_configuration = update_coin_configuration(config_data, liq_percentage)
    save_new_configuration(new_configuration, config_file)


def get_percent_change(previous, current):
    """Get percentage of change between current and previous liq values"""
    if current == previous:
        return 0
    try:
        change = round((abs(current - previous) / previous) * 100.0, 2)
        sign = '+' if current >= previous else '-'
        return sign + str(change) + '%'
    except ZeroDivisionError:
        return 0


if __name__ == "__main__":
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.debug(args)

    if not args.config_file.exists():
        raise ValueError(f"Config file does not exists at path {args.config_file.name}")

    try:
        logger.info("======= Starting to update the coins =======")
        main(config_file=Path(args.config_file), liq_percentage=args.liq_percentage)
    except Exception:  # pylint: disable=broad-except
        logger.exception("Unexpected error while running the script")
        logger.info("======= Update failed =======")
    else:
        logger.info("======= Update done =======")
