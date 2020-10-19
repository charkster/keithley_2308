# keithley_2308
Python class for Keithley 2308 Battery/Charger Simulator
The best part of this class is the function "get_unique_scpi_list" as this will query all the settings of the instrument individually and return a list of settings that are different to the default settings. With this list you can just reset the instrument and load the list to get back to a specific configuration. The unique settings list is human readable. I will include these lists in my various instrument scripts.
