import sys
import platform
import asyncio
import logging

from bleak import BleakScanner, BleakClient


async def scan_ble():
  devices = await BleakScanner.discover(timeout=3)
  for d in devices:
    print(d)



logger = logging.getLogger(__name__)
ADDRESS = (
  "E6:F8:E8:8D:D7:68"
  if platform.system() != "Darwin"
  else "6E3B11C9-B578-2579-D03C-783760E9FD5A"
)

async def scan_characteristic(address):
  async with BleakClient(address) as client:
    logger.info(f"Connected: {client.is_connected}")

    for service in client.services:
      logger.info(f"[Service] {service}")
      for char in service.characteristics:
        if "read" in char.properties:
          try:
            value = bytes(await client.read_gatt_char(char.uuid))
            logger.info(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}")
          except Exception as e:
            logger.error(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {e}")

        else:
          value = None
          logger.info(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}")

        for descriptor in char.descriptors:
          try:
            value = bytes(
              await client.read_gatt_descriptor(descriptor.handle)
            )
            logger.info(f"\t\t[Descriptor] {descriptor}) | Value: {value}")
          except Exception as e:
            logger.error(f"\t\t[Descriptor] {descriptor}) | Value: {e}")

if __name__ == "__main__":

  asyncio.run(scan_ble())

  logging.basicConfig(level=logging.INFO)
  # asyncio.run(scan_characteristic(ADDRESS))

