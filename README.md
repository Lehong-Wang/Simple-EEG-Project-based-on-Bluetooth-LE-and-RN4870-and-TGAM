
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
TGAM chip can support three electrodes (EG,GND,REF), with can record EEG data from one point. The chip outputs the data through UART in the form of data packets.[^1]
![Final Setup](pictures/setup.png)

[^1] this is foot note

## Setup the experiment

### Setup RN4870








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