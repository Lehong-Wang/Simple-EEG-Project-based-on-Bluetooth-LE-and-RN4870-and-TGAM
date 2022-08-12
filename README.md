
# Simple EEG Project
This project uses the TGAM chip from NeuroSky and the RN4870 chip from Microchip Technology to collect and process real time EEG data wirelessly with Bluetooth LE.


## Hardware
* [TGAM chip](https://store.neurosky.com/products/eeg-tgam)
* [RN4870 chip](https://www.microchip.com/en-us/product/rn4870)
* [USB to Serial Adapter](https://www.amazon.com/HiLetgo-CP2102-Converter-Adapter-Downloader/dp/B00LODGRV8/ref=asc_df_B00LODGRV8/?tag=hyprod-20&linkCode=df0&hvadid=563602091749&hvpos=&hvnetw=g&hvrand=18143711129221568371&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9001847&hvtargid=pla-576277438732&psc=1)
* Computer with Bluetooth LE support
* wires and 3.3V power supply

## Software
* Python
* [Bleak](https://github.com/hbldh/bleak)
* [Matplotlib](https://matplotlib.org/)

## Overview of the experiment
TGAM chip can support three electrodes (EG,GND,REF), with can record EEG data from one point. The chip outputs the data through UART in the form of data packets. 
The output is transfered to RN4870, which converts it to Bluetooth LE signal. 
Finally, your computer can run the program in "get_notification.py" file to get the data and parse the packets into the form of csv files in "parse" folder.
![Final Setup](pictures/setup.png)


## Setup the experiment

### Setup TGAM
- For the TGAM chip, wire it to power and make sure it’s running at baud rate of 57600 (factory default is 57600) and producing valid data packet. To check the output, we recommend using a USB to Serial adapter like the one mentioned above to connect to your computer and use a Serial terminal software like Coolterm to read the data. For details, please refer to the [TGAM data sheet](http://wearcam.org/ece516/neurosky_eeg_brainwave_chip_and_board_tgam1.pdf)

- For the RN4870 chip, we need to configure some settings before we can use it. 
  - First, wire chip like this: Vcc pin to 3.3V power, ground pin to ground, and TX/RX to computer. 
  - Then, set the Coolterm software baudrate to 115200 (because the factory setting for this chip is 115200). Type “$$$” into the Coolterm terminal, and you should get the response “CMD>” in the terminal. This means that the chip is in command mode, and you can type commands listed in the [user guide](http://ww1.microchip.com/downloads/en/DeviceDoc/50002466B.pdf) to make it do things. 
  - For the purpose of the experiment, please follow the guide in the "RN4870_setup_instructions.txt". You only need to setup once and the settings is preserved after power off. If you encounter some kind of port error when configuring the chip with 
  - Here is a screenshot communicating with RN4870 in command mode. Notice here there is "CMD>" at the front of each line to indecate that it is in command mode, and when a command is executed, it returns "AOK". "ERR" means the command is not valid, and "%REBOOT%" means it finished rebooting.
  ![](pictures/RN4870_command.png)

- Next, wire up the two chips. Connect the power and ground of both chips, and connect the TX pin from TGAM to RX pin of RN4870.



---

- one
- twojslkfdjfsdjkfsjdkfjdskfjkdsjfkdsjkfjksdjfkjsdkfjksdjkfjsdkjfksdjfkjsdkfjsdkjfksdjfkjsdkfjksdjfkjdskfjdksjfdsjk


- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media


`
code
`
```
print("hi)
```

this is a normal line of text
  * this is the first level of bullet points, made up of <space><space>*<space>
    * this is more indented, composed of <space><space><space><space>*<space>



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This will appear with six space characters in front of it



Line 1
> line 2 
>> line 3


Term 1
: definition 1
: definition 2

Term 2
: definition 1
: definition 2



<dl>
    <dt>Term 1</dt>
    <dd>definition 1</dd>
    <dd>definition 2</dd>
    <dt>Term 2</dt>
    <dd>definition 1</dd>
    <dd>definition 2</dd>
</dl>


hi hi
hi
hi



&nbsp;
This is the text that I want indented.  All text on the same line as the preceding colon will be included in this definition.
: If you include a second definition you'll get a new line; potentially separated by a space. <br />Some inline HTML may be supported within this too, allowing you to create new lines without spaces.
: Support for other markdown syntax varies; e.g. we can add a bullet list, but each one's wrapped in a separate definition term, so the spacing may be out.
: - item 1
: - item 2
: - item 3
-time
-time