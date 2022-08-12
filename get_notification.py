
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
from get_characteristic import ADDRESS, CHARACTERISTIC_UUID



RECORD_TIME = 300.0


async def main(address, char_uuid):
  """Get notification from characteristic and pass on the data to handler"""
  async with BleakClient(address) as client:
    print(f"Connected: {client.is_connected}")

    await client.start_notify(char_uuid, notification_handler)
    await asyncio.sleep(RECORD_TIME)
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

  while parse_packet(current_list, delta_time):
    delta_time = "{:.5f}".format(time.time() - start_time)

    print(f"Parsing {list(map(hex, current_list))}")



def print_as_hex(data_to_print):
  """Helper for printing data in hex form"""
  print(list(map(hex, data_to_print)))




if __name__ == "__main__":
  # dirctory name to store the parsed data (don't change)
  directory_name = "parse"
  # clean previous parsing results
  # move/copy the data files outside the parse folder if you want keep the resultes
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


  # # If you want to generate a graph from the recorded data, uncomment the line below
  # # Don't recomand ploting data recorded for more than 15 seconds, it will take significant time to plot
  # # List of choices for X, Y axis value to plot:
  # # ["Index", "Time", "Raw_Wave", "Attention", "Meditation", "Delta", "Theta", "LowAlpha", "HighAlpha", "LowBeta", "HighBeta", "LowGamma", "MidGamma", "Poor_Signal", "Battery"]
  # generate_graph(field_x = "Time", field_y = "Raw_Wave")



