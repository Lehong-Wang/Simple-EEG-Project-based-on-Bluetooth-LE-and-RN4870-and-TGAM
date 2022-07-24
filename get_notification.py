
"""
Handles notification and parse data upon receiving
"""

import sys
import asyncio
import platform
import os

from bleak import BleakClient
from parse import SYNC, parse_packet

CHARACTERISTIC_UUID = "bf3fbd80-063f-11e5-9e69-0002a5d5c501"
ADDRESS = (
  "24:71:89:cc:09:05"
  if platform.system() != "Darwin"
  else "6E3B11C9-B578-2579-D03C-783760E9FD5A"
)


async def main(address, char_uuid):
  """Get notification from characteristic and pass on the data to handler"""
  async with BleakClient(address) as client:
    print(f"Connected: {client.is_connected}")

    await client.start_notify(char_uuid, notification_handler)
    await asyncio.sleep(3.0)
    await client.stop_notify(char_uuid)



def notification_handler(sender, data):
  """Function called when got a notification"""
  int_list = list(data)
  print_as_hex(int_list)
  process_data(int_list)


current_list = []

def process_data(data_list):
  """Process data from notification"""
  while data_list:
    current_byte = data_list.pop(0)
    if current_byte == SYNC:
      current_byte = data_list.pop(0)
      if current_byte == SYNC:
        if current_list:
          parse_packet(current_list)
        current_list.clear()
      current_list.append(SYNC)
    current_list.append(current_byte)




def print_as_hex(data_to_print):
  """Helper for printing data in hex form"""
  print(list(map(hex, data_to_print)))






if __name__ == "__main__":
  if os.path.exists("parse.csv"):
    os.remove("parse.csv")

  asyncio.run(
    main(
      sys.argv[1] if len(sys.argv) > 1 else ADDRESS,
      sys.argv[2] if len(sys.argv) > 2 else CHARACTERISTIC_UUID,
    )
  )


