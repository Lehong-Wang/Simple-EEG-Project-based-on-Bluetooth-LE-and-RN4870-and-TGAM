
"""
Handles notification and parse data upon receiving
"""

import sys
import asyncio
import platform
import os
import time
import shutil


from bleak import BleakClient
from parse import SYNC, parse_packet, generate_graph

CHARACTERISTIC_UUID = "49535343-1e4d-4bd9-ba61-23c647249616"
ADDRESS = (
  "24:71:89:cc:09:05"
  if platform.system() != "Darwin"
  else "A46EB02C-7B16-0696-8ED6-9F5679DE8270"
)


async def main(address, char_uuid):
  """Get notification from characteristic and pass on the data to handler"""
  async with BleakClient(address) as client:
    print(f"Connected: {client.is_connected}")

    await client.start_notify(char_uuid, notification_handler)
    await asyncio.sleep(180.0)
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
  delta_time = "{:.5f}".format(time.time() - start_time)
  # while current_list:
  while parse_packet(current_list, delta_time):
    delta_time = "{:.5f}".format(time.time() - start_time)

    print(f"Parsing {list(map(hex, current_list))}")
  # current_list.clear()

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



# def notification_handler(sender, data):
#   print(list(data))




if __name__ == "__main__":
  directory_name = "parse"

  try:
    shutil.rmtree(directory_name)
  except OSError as e:
    print ("Error: %s - %s." % (e.filename, e.strerror))
  os.makedirs(directory_name)

  start_time = time.time()


  asyncio.run(
    main(
      sys.argv[1] if len(sys.argv) > 1 else ADDRESS,
      sys.argv[2] if len(sys.argv) > 2 else CHARACTERISTIC_UUID,
    )
  )
  # generate_graph()


  # if __name__ == '__main__':
  # if os.path.exists(FILE):
  #   os.remove(FILE)


  # data = read_from_file("capture with new wire 57600.txt")

  # while len(data) >= 8:
  #   delta_time = "{:.5f}".format(time.time() - start_time)
  #   parse_packet(data, delta_time)


