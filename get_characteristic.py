import sys
import platform
import asyncio
import logging

from bleak import BleakScanner, BleakClient


async def scan_ble():
  devices = await BleakScanner.discover(timeout=5)
  for d in devices:
    print(d)



logger = logging.getLogger(__name__)
ADDRESS = (
  "E6:F8:E8:8D:D7:68"
  if platform.system() != "Darwin"
  else "A820502D-7BCE-73F6-63E8-0E8B4E2D0583"
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


async def time_counter():
  """test docstring"""
  for i in range(10):
    print(i)
    await asyncio.sleep(.5)

async def timed_scan_ble():
  await asyncio.gather(scan_ble(), time_counter())

async def timed_scan_characteristic():
  await asyncio.gather(scan_characteristic(ADDRESS), time_counter())


if __name__ == "__main__":
  # asyncio.run(timed_scan_ble())
  # asyncio.run(scan_ble())

  logging.basicConfig(level=logging.INFO)
  asyncio.run(timed_scan_characteristic())

