#!/usr/bin/python3

# coppied from https://github.com/arraylabs/pymyq/blob/master/example.py

"""Run an example script to quickly test."""
import asyncio
import logging
import sys
import os

from aiohttp import ClientSession

from pymyq import login
from pymyq.errors import MyQError, RequestError



_LOGGER = logging.getLogger()

# main Configuration
EMAIL = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as websession:
        try:
            # Create an API object:
            api = await login(EMAIL, PASSWORD, websession)

            for account in api.accounts:
                _LOGGER.info(f"Account ID: {account}")
                _LOGGER.info(f"Account Name: {api.accounts[account]}")

                # Get all devices listed with this account – note that you can use
                # api.covers to only examine covers or api.lamps for only lamps.
                _LOGGER.info(f"  GarageDoors: {len(api.covers)}")
                _LOGGER.info("  ---------------")
                if len(api.covers) != 0:
                    for idx, device_id in enumerate(
                        device_id
                        for device_id in api.covers
                        if api.devices[device_id].account == account
                    ):
                        device = api.devices[device_id]
                        _LOGGER.info("---------")
                        _LOGGER.info("Device %s: %s", idx + 1, device.name)
                        _LOGGER.info("Device Online: %s", device.online)
                        _LOGGER.info("Device ID: %s", device.device_id)
                        _LOGGER.info("Parent Device ID: %s", device.parent_device_id)
                        _LOGGER.info("Device Family: %s", device.device_family)
                        _LOGGER.info("Device Platform: %s", device.device_platform)
                        _LOGGER.info("Device Type: %s", device.device_type)
                        _LOGGER.info("Firmware Version: %s", device.firmware_version)
                        _LOGGER.info("Open Allowed: %s", device.open_allowed)
                        _LOGGER.info("Close Allowed: %s", device.close_allowed)
                        _LOGGER.info("Current State: %s", device.state)

                        try:
                            if len(sys.argv) > 2:
                                device_name_lower = device.name.lower()
                                command = sys.argv[1].lower()
                                door_name_lower = sys.argv[2].lower()
                                if command == 'close' and door_name_lower == device_name_lower:
                                    await device.close()
                                elif command == 'open' and door_name_lower == device_name_lower:
                                    await device.open()
                            # await device.open()
                            # await asyncio.sleep(15)
                            # await device.close()
                        except RequestError as err:
                            _LOGGER.error(err)
                            sys.exit(1)

        except MyQError as err:
            _LOGGER.error("There was an error: %s", err)
            sys.exit(1)


asyncio.get_event_loop().run_until_complete(main())