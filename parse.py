
"""
Parse TGAM data packet
Following ThinkGear Serial Stream Guide
http://developer.neurosky.com/docs/doku.php?id=thinkgear_communications_protocol
"""

import csv
import os
import time

SYNC = 0xAA
# FILE = "parse.csv"
FILE = "parse_1.csv"

def parse_packet(byte_list, current_time):
  """
  Parse the original packet
  Hand over to parse_data if packet is valid
  """

  packet = byte_list[:]

  try:
    current_byte = packet.pop(0)
    if current_byte != SYNC:
      print("Error: First byte not SYNC")
      print_error_package(packet[:10])
      del byte_list[0]
      return

    current_byte = packet.pop(0)
    if current_byte != SYNC:
      print("Error: Second byte not SYNC")
      print_error_package(packet[:10])
      return

    current_byte = packet.pop(0)
    if current_byte >= SYNC:
      print("Error: PLength byte too large")
      print_error_package(packet[:10])
      return
    p_length = current_byte
    # print(f"p_length: {p_length}")

    data_packet = packet[:p_length]
    packet = packet[p_length:]

    original_sum = 0
    for byte in data_packet:
      original_sum += byte
    chk_sum = original_sum & 0xFF
    chk_sum = ~chk_sum & 0xFF

    check_sum = packet.pop(0)

  except IndexError:
    print(f"Error: Index out of bound, p_length = {p_length}")
    print_error_package(packet[:p_length+4])
    return

  if check_sum == chk_sum:
    # print("CheckSum is correct, preseed to parse data packet")
    packet_length = len(byte_list) - len(packet)
    del byte_list[:packet_length]
    parse_data(data_packet, current_time)
    return True
  else:
    print("CheckSum is wrong")
    print(f"Original Sum is {hex(original_sum)}")
    print(f"chk_sum is {hex(chk_sum)}")
    print(f"CheckSum byte is {hex(check_sum)}")
    print_error_package(packet[:10])
    return



EXCODE = 0x55
BATTERY = 0x01
POOR_SIGNAL = 0x02
HEART_RATE = 0x03
ATTENTION = 0x04
MEDITATION = 0x05
RAW_WAVE_8 = 0x06
RAW_MARKER = 0x07

RAW_WAVE = 0x80
EEG_POWER = 0x81
ASIC_EEG_POWER = 0x83
RRINTERVAL = 0x86


index = -1

def parse_data(byte_list, current_time):
  """Parse data packet"""
  global index
  index += 1
  data_packet = byte_list[:]
  data_dict = {}
  field_list = ["Index", "Time", "Raw_Wave", "Attention", "Meditation", "Delta", "Theta", "LowAlpha", "HighAlpha", "LowBeta", "HighBeta", "LowGamma", "MidGamma", "Poor_Signal", "Battery"]
  for field_name in field_list:
    data_dict[field_name] = "null"
  
  data_dict["Time"] = current_time
  data_dict["Index"] = index

  while data_packet:

    current_byte = data_packet.pop(0)

    excode_level = 0
    while current_byte == EXCODE:
      excode_level += 1
      current_byte = data_packet.pop(0)

    code_byte = current_byte
    if code_byte >= 0x80:
      v_length = data_packet.pop(0)

    if code_byte == BATTERY:
      value = data_packet.pop(0)
      full_battery = 0x7F
      battery_level = int(value / full_battery * 100)
      print(f"Battery Level is {battery_level}%")
      data_dict["Battery"] = battery_level

    elif code_byte == POOR_SIGNAL:
      value = data_packet.pop(0)
      if value == 0:
        print("Good Signal")
      elif value == 200:
        print("WARNING: Off head signal detected")
      else:
        print(f"Signal Quality: {value}/255")
      data_dict["Poor_Signal"] = value

    elif code_byte == HEART_RATE:
      value = data_packet.pop(0)
      print(f"Heart Rate: {value}")

    elif code_byte == ATTENTION:
      value = data_packet.pop(0)
      value_meaning = ""
      if value == 0:
        print("WARNING: Unable to calculate Attention eSense")
      elif 1 <= value < 20:
        value_meaning = "strongly lowered"
      elif 20 <= value < 40:
        value_meaning = "reduced"
      elif 40 <= value < 60:
        value_meaning = "neutral"
      elif 60 <= value < 80:
        value_meaning = "slightly elevated"
      elif 80 <= value <= 100:
        value_meaning = "elevated"
      else:
        print("ERROR: Attention eSense value out of bound (0-100)")
      print(f"Attention eSense value: {value}\t{value_meaning}")
      data_dict["Attention"] = value

    elif code_byte == MEDITATION:
      value = data_packet.pop(0)
      value_meaning = ""
      if value == 0:
        print("WARNING: Unable to calculate Meditation eSense")
      elif 1 <= value < 20:
        value_meaning = "strongly lowered"
      elif 20 <= value < 40:
        value_meaning = "reduced"
      elif 40 <= value < 60:
        value_meaning = "neutral"
      elif 60 <= value < 80:
        value_meaning = "slightly elevated"
      elif 80 <= value <= 100:
        value_meaning = "elevated"
      else:
        print("ERROR: Meditation eSense value out of bound (0-100)")
      print(f"Meditation eSense value: {value}\t{value_meaning}")
      data_dict["Meditation"] = value

    # only available on TGEM, not available on TGAM/TGAM1
    elif code_byte == RAW_WAVE_8:
      value = data_packet.pop(0)
      print(f"8 Bit Raw Wave value: {value}")

    # this value is for debug, always 0
    elif code_byte == RAW_MARKER:
      value = data_packet.pop(0)
      print(f"Raw Maker value: {value}")


    # multi byte values
    elif code_byte == RAW_WAVE:
      value = data_packet[:v_length]
      data_packet = data_packet[v_length:]

      raw = value[0]*256 + value[1]
      if raw >= 32768:
        raw = raw - 65536
      print(f"Raw Wave value: {raw}")
      data_dict["Raw_Wave"] = raw

    # I'm not fucking going to spend time parsing this shit!
    # If you want to use it, do it yourself!
    elif code_byte == EEG_POWER:
      value = data_packet[:v_length]
      data_packet = data_packet[v_length:]
      print(f"EEG Power value: {value}")

    elif code_byte == ASIC_EEG_POWER:
      value = data_packet[:v_length]
      data_packet = data_packet[v_length:]

      def to_int(int_list):
        return int_list[0]*256*256 + int_list[1]*256 + int_list[2]

      delta = value[:3]
      delta_value = to_int(delta)
      print(f"delta value: {delta_value}")
      data_dict["Delta"] = delta_value

      theta = value[3:6]
      theta_value = to_int(theta)
      print(f"theta value: {theta_value}")
      data_dict["Theta"] = theta_value

      low_alpha = value[6:9]
      low_alpha_value = to_int(low_alpha)
      print(f"low_alpha value: {low_alpha_value}")
      data_dict["LowAlpha"] = low_alpha_value

      high_alpha = value[9:12]
      high_alpha_value = to_int(high_alpha)
      print(f"high_alpha value: {high_alpha_value}")
      data_dict["HighAlpha"] = high_alpha_value

      low_beta = value[12:15]
      low_beta_value = to_int(low_beta)
      print(f"low_beta value: {low_beta_value}")
      data_dict["LowBeta"] = low_beta_value

      high_beta = value[15:18]
      high_beta_value = to_int(high_beta)
      print(f"high_beta value: {high_beta_value}")
      data_dict["HighBeta"] = high_beta_value

      low_gamma = value[18:21]
      low_gamma_value = to_int(low_gamma)
      print(f"low_gamma value: {low_gamma_value}")
      data_dict["LowGamma"] = low_gamma_value

      mid_gamma = value[21:24]
      mid_gamma_value = to_int(mid_gamma)
      print(f"mid_gamma value: {mid_gamma_value}")
      data_dict["MidGamma"] = mid_gamma_value

      # print(f"ASIC EEG Power value: {value}")

    elif code_byte == RRINTERVAL:
      value = data_packet[:v_length]
      data_packet = data_packet[v_length:]
      print(f"RRInterval value: {value}")

    else:
      print(f"ERROR: Unexpected code detected: {code_byte}")
      print_error_package(byte_list)


  with open(FILE, "a") as f:
    csv_writer = csv.DictWriter(f, fieldnames=field_list)
    if os.stat(FILE).st_size == 0:
      csv_writer.writeheader()

    csv_writer.writerow(data_dict)




def print_error_package(packet):
  """Helper for printing out package that caused error"""
  print("Error packet: [", end = "")
  end_byte = packet.pop()
  for byte in packet:
    print(hex(byte), end = ", ")
  print(hex(end_byte), end = "")
  print("]")





def read_from_file(filename):
  """parse a txt file into int list"""
  hex_list = []
  with open(filename, 'r') as f:
    data = f.read()
    while data:
      word = data[:2]
      data = data[2:]
      # print("str:", word)
      if not word.isspace():
        num = int(word, 16)
        hex_list.append(num)

  return hex_list


# def parse_whole_list(full_list):
#   """devide up an int list into packages with SYNC"""
#   data_list = full_list[:]
#   curret_list = []
#   parsed_list = []
#   while data_list:
#     current_byte = data_list.pop(0)
#     if current_byte == SYNC:
#       current_byte = data_list.pop(0)

#       if current_byte == SYNC:
#         if curret_list:
#           parsed_list.append(curret_list)
#         curret_list = []
#       curret_list.append(SYNC)
#     curret_list.append(current_byte)

#   parsed_list.append(curret_list)
#   print(parsed_list)

#   for l in parsed_list:
#     # print(l)
#     parse_packet(l)






if __name__ == '__main__':
  if os.path.exists(FILE):
    os.remove(FILE)


  data = read_from_file("capture with new wire 57600.txt")
  start_time = time.time()

  while len(data) >= 8:
    delta_time = "{:.5f}".format(time.time() - start_time)
    parse_packet(data, delta_time)

  # sample_packet = [0xAA, 0xAA, 0x08, 0x02, 0x20, 0x01, 0x7E, 0x04, 0x12, 0x05, 0x60, 0xE3]
  # parse_packet(sample_packet)




