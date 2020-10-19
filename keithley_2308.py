import time

class keithley_2308():

    def __init__(self, pyvisa_instr):
        self.ke2308 = pyvisa_instr # this is the pyvisa instrument, rm.open_resource('GPIB0::20::INSTR')

    def show_present_state(self):
        channel_list = [1, 2]
        for channel in channel_list:
            output_state = int((self.ke2308.query("OUTPut{0}:STATe?".format(channel))).rstrip('\r\n'))
            print "Channel %d output state is %s" % (channel,output_state)
            if (output_state == 1):
                voltage = (self.ke2308.query("SOURce{0}:VOLTage?".format(channel))).rstrip('\r\n')
                current_limit = (self.ke2308.query("SOURce{0}:CURRent?".format(channel))).rstrip('\r\n')
                self.ke2308.write("SENSe{0}:CURRent:RANGe:AUTO ON".format(channel))
                self.ke2308.write("SENSe{0}:FUNCtion CURRent".format(channel))
                print "Channel %d is ON, set to %s volts with a current limit of %s" % (channel,voltage,current_limit)

    def get_all_scpi_dict(self):
        channel_list = [1, 2]
        result_dict = {}
        for channel in channel_list:
            for command in self.source_w_channel_dict:
                time.sleep(1)
                result = (self.ke2308.query(command.format(channel, "?"))).rstrip('\r\n')
                result = " " + result
                result_dict[command.format(channel, "?")] = result
        return result_dict

    def get_all_scpi_list(self):
        channel_list = [1, 2]
        result_list = []
        for channel in channel_list:
            for command in self.source_w_channel_dict:
                time.sleep(0.1)
                result = (self.ke2308.query(command.format(channel,"?"))).rstrip('\r\n')
                result = " " + result
                result_list.append(command.format(channel, result))
            if (channel == 1):
                for command in self.source_w_channel_1_dict:
                    time.sleep(0.1)
                    result = (self.ke2308.query(command.format(channel, "?"))).rstrip('\r\n')
                    result = " " + result
                    result_list.append(command.format(channel, result))
        return result_list

    # this will query the instrument and output a list of all setings that are not the default settings
    # this is useful after you have manually configured the instrument and you want to get a human readable list of settings
    def get_unique_scpi_list(self):
        unique_scpi_list = []
        inst_settings_list = self.get_all_scpi_list()
        for setting in inst_settings_list:
            if (setting not in self.settings_por_scpi_list):
                unique_scpi_list.append(setting)
        return unique_scpi_list

    source_w_channel_dict = {
        "SOURce{0}:VOLTage{1}"                  : "Set voltage amplitude in volts: 0 to 15 (1mV resolution)",
        "SOURce{0}:VOLTage:PROTection{1}"       : "Sets VPT (voltage protection) range (0-8V)",
        "SOURce{0}:VOLTage:PROTection:CLAMp{1}" : "Sets VPT clamp mode ON or OFF",
        "SOURce{0}:CURRent{1}"                  : "Set current limit value in amps: 0.006 to 5 (100uA res)",
        "SOURce{0}:CURRent:TYPe{1}"             : "Select current limit type: LIMit or TRIP",
        "OUTPut{0}:STATe{1}"                    : "Turn the power supply output ON or OFF",
        "OUTPut{0}:BANDwidth{1}"                : "Specifies output bandwidth (HIGH or LOW)"
    }

    # these are only for channel 1
    source_w_channel_1_dict = {
        "OUTPut{0}:IMPedance{1}": "Specifies output impedance (0-1 Ohm in 10 milli ohm steps)"
    }

    source_w_channel_info_dict = {
        "SOURce{0}:VOLTage:PROTection:STATe{1}": "Query state of VPT, information only",
        "SOURce{0}:CURRent::STATe{1}"          : "Query state of current limit, information only"
    }

    sense_w_channel_dict = {
        "SENSe{0}:CURRent:RANGe:UPPer{1}" : "Specify expected current in amps: 0 to 5",
        "SENSe{0}:CURRent:RANGe:AUTO{1}"  : "Enable or disable auto range",
        "SENSe{0}:FUNCtion{1}"            : "Select readback function: VOLTage or CURRent",
        "SENSe{0}:NPLCycles{1}"           : "Set integration rate (in line cycles) for voltage, current, measurements: 0.002 to 10",
        "SENSe{0}:AVERage{1}"             : "Specify the average count for voltage and current measurements: 1 to 10",
        "READ{0}?"                        : "Trigger and return one reading for specified channel",
        "READ{0}:ARRay?"                  : "Trigger an array of readings and return them for specified channel"
    }

    settings_por_scpi_list = [
        'SOURce1:VOLTage:PROTection:CLAMp 0',
        'OUTPut1:BANDwidth LOW',
        'SOURce1:CURRent:TYPe LIM',
        'SOURce1:VOLTage:PROTection 8.000000E+00',
        'OUTPut1:STATe 0',
        'SOURce1:VOLTage 0.000000E+00',
        'SOURce1:CURRent 2.500000E-01',
        'OUTPut1:IMPedance 0.000',
        'SOURce2:VOLTage:PROTection:CLAMp 0',
        'OUTPut2:BANDwidth LOW',
        'SOURce2:CURRent:TYPe LIM',
        'SOURce2:VOLTage:PROTection 8.000000E+00',
        'OUTPut2:STATe 0',
        'SOURce2:VOLTage 0.000000E+00',
        'SOURce2:CURRent 2.500000E-01' ]