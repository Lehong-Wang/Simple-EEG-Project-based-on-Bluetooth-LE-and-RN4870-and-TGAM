import sys
import platform
import asyncio
import logging

from bleak import BleakScanner, BleakClient




# paste the device address you want to scan for characteristics here
ADDRESS = (
  "E6:F8:E8:8D:D7:68"
  # If using Mac, paste address below
  if platform.system() != "Darwin"
  else "29C7009C-8371-A06B-A395-A8C97F8A9FDA"
)

# paste the characteristic UUID here
CHARACTERISTIC_UUID = "49535343-1e4d-4bd9-ba61-23c647249616"


# Scan time to find devices in seconds
SCAN_TIME = 8

logger = logging.getLogger(__name__)



async def scan_ble():
  """Scan for available BLE devices"""
  devices = await BleakScanner.discover(timeout=SCAN_TIME)
  for d in devices:
    print(d)


async def scan_characteristic(address):
  """Scan the characteristic UUID for a given device address"""
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
  """A simple count up timer to make the long scan time feel shorter"""
  for i in range(2*SCAN_TIME):
    print(i)
    await asyncio.sleep(.5)

async def timed_scan_ble():
  """Wraper Function"""
  await asyncio.gather(scan_ble(), time_counter())

async def timed_scan_characteristic():
  """Wraper Function"""
  await asyncio.gather(scan_characteristic(ADDRESS), time_counter())


if __name__ == "__main__":

  # # Uncomment this line to scan for Bluetooth LE devices
  # asyncio.run(timed_scan_ble())

  logging.basicConfig(level=logging.INFO)
  # # Uncomment this line to get the characteristic of the given device address
  asyncio.run(timed_scan_characteristic())

