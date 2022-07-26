
"""
Handles notification and parse data upon receiving
"""

import sys
import asyncio
import platform
import os

from bleak import BleakClient
from parse import SYNC, FILE, parse_packet

CHARACTERISTIC_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
ADDRESS = (
  "24:71:89:cc:09:05"
  if platform.system() != "Darwin"
  else "A820502D-7BCE-73F6-63E8-0E8B4E2D0583"
)


async def main(address, char_uuid):
  """Get notification from characteristic and pass on the data to handler"""
  async with BleakClient(address) as client:
    print(f"Connected: {client.is_connected}")

    await client.start_notify(char_uuid, notification_handler)
    await asyncio.sleep(5.0)
    await client.stop_notify(char_uuid)



def notification_handler(sender, data):
  """Function called when got a notification"""
  int_list = list(data)
  print_as_hex(int_list)
  current_list.extend(int_list)
  process_data()


current_list = []

def process_data():
  """Process data from notification"""
  while parse_packet(current_list):
    print(f"Parsing {current_list}")

  # print(f"Processing {data_list}")

  # while data_list:
  #   current_byte = data_list.pop(0)
  #   if current_byte == SYNC:
  #     current_byte = data_list.pop(0)
  #     if current_byte == SYNC:
  #       if current_list:
  #         # print(f"Parsing {current_list}")
  #         parse_packet(current_list)
  #       current_list.clear()
  #     current_list.append(SYNC)
  #   current_list.append(current_byte)




def print_as_hex(data_to_print):
  """Helper for printing data in hex form"""
  print(list(map(hex, data_to_print)))






if __name__ == "__main__":
  if os.path.exists(FILE):
    os.remove(FILE)

  asyncio.run(
    main(
      sys.argv[1] if len(sys.argv) > 1 else ADDRESS,
      sys.argv[2] if len(sys.argv) > 2 else CHARACTERISTIC_UUID,
    )
  )


