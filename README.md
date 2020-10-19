# keithley_2308
Python class for Keithley 2308 Battery/Charger Simulator
The best part of this class is the function "get_unique_scpi_list" as this will query all the settings of the instrument individually and return a list of settings that are different to the default settings. With this list you can just reset the instrument and load the list to get back to a specific configuration. The unique settings list is human readable. I will include these lists in my various instrument scripts.

Here is an example usage (it will read all unique settings into a list, reset the instrument and then program the unique settings back into the instrument):

import time
import pyvisa
from keithley_2308 import keithley_2308

rm = pyvisa.ResourceManager()
ke2308 = rm.open_resource('GPIB0::20::INSTR')
keithley_2308 = keithley_2308(pyvisa_instr=ke2308)

current_setting_list = keithley_2308.get_unique_scpi_list()

ke2308.write('*RST')
time.sleep(2)
for scpi_cmd in current_setting_list:
  ke2308.write(scpi_cmd)
time.sleep(4)
