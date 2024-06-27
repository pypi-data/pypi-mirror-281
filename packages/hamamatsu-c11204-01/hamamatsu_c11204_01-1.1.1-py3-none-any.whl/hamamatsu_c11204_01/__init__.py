# -*- coding: utf-8 -*-
"""init modif set values.ipynb
"""

import serial

def open_port(port_name):
    baudrate = 38400
    ser = serial.Serial(port_name,baudrate,parity='E')
    ser.timeout=1
    if (ser.is_open is False):
        ser.open()
    return ser

def close_port(ser):
    ser.close()

def number_to_ascii(number):
    # Keep the first 8 bits
    first_8_bits = number & 0xFF

    # Split the first 8 bits into two nibbles
    nibble1 = first_8_bits >> 4
    nibble2 = first_8_bits & 0x0F

    # Convert each nibble to its ASCII representation
    ascii_nibble1 = nibble1 + ord('0') if nibble1 < 10 else nibble1 - 10 + ord('A')
    ascii_nibble2 = nibble2 + ord('0') if nibble2 < 10 else nibble2 - 10 + ord('A')

    return ascii_nibble1, ascii_nibble2

def command_to_hex(command, *argv):
    STX = 0x02
    ETX = 0x03
    CR = 0x0D
    hex_STX = f"0x{STX:02X}"
    hex_ETX = f"0x{ETX:02X}"
    hex_CR = f"0x{CR:02X}"
    hex_command = [f"0x{ord(c):02X}" for c in command]
    # Dictionary that associates each command with the expected number of parameters
    command_parameters = {
        'HPO': 0, 'HST': 6, 'HRT': 0, 'HOF': 0, 'HON': 0, 'HCM': 1,
        'HRE': 0, 'HBV': 1, 'HGT': 0, 'HGV': 0, 'HGC': 0, 'HGS': 0
    }
    if command not in command_parameters:
        raise ValueError(f"Command '{command}' not recognized.")
    if len(argv) != command_parameters[command]:
        raise ValueError(f"The command '{command}' requires exactly {command_parameters[command]} parameters, received {len(argv)}.")
    # Convert all parameters to integers
    hex_parameters = []
    if command == 'HST':
        hst_dec = [
        int(argv[0] / dict_conv['sec_high_temp']),
        int(argv[1] / dict_conv['sec_low_temp']),
        int(argv[2] / dict_conv['prim_high_temp']),
        int(argv[3] / dict_conv['prim_low_temp']),
        int(argv[4] / dict_conv['volt_ref']),
        int((argv[5] * -5.5e-3+1.035)/1.907e-5)]
        for dec in hst_dec:
            hex_val = f"{dec:04X}"
            for h in hex_val:
                hex_parameters.append(hex(ord(h)))
    elif command == 'HBV':
            hex_val = f"{int(argv[0]):04X}"
            hex_parameters = [hex(ord(i)) for i in hex_val]
    elif command == 'HCM':
            hex_param = f"{argv[0]:01X}"
            hex_parameters = [hex(ord(hex_param))]
    # Calculate the checksum value

    if (command=='HBV') or (command=='HST') or (command=='HCM'):
        checksum_val = (
            STX +
            sum(ord(c) for c in command) +
            sum([int(hex_parameters[i],16) for i in range(len(hex_parameters))]) +
            ETX
        )
    else:
        checksum_val = (
            STX +
            sum(ord(c) for c in command) +
            sum(int(hex_parameters[i], 16) for i in range(len(hex_parameters))) +
            ETX
        )

    checksum_val %= 256
    # Split the checksum value into two ASCII nibbles
    nibble1, nibble2 = number_to_ascii(checksum_val)
    result = [hex_STX] + hex_command + hex_parameters + [hex_ETX, f"0x{nibble1:02X}", f"0x{nibble2:02X}", hex_CR]
    return result

def send_command(ser,command, *argv):
    hex_string = command_to_hex(command, *argv)
    for hex_value in hex_string:
        send_hex(ser, hex_value)

def send_hex(ser, hex_value):
    value = int(hex_value, 16)
    ser.write(value.to_bytes(1, byteorder='big'))  # alternatively, could be 'little'

def read_from_source(ser):
    data = ser.read(32)
    ascii_data = data.decode('ascii', errors='ignore')
    return ascii_data


dict_conv = {
    'out_volt_mon': 1.812e-3,
    'out_curr_mon': 4.980e-3,
    'temp_conv_1': 1.907e-5/-5.5e-3,
    'temp_conv_2': 1.035/-5.5e-3,
    'sec_high_temp': 1.507e-3,
    'sec_low_temp': 1.507e-3,
    'prim_high_temp': 5.225e-2,
    'prim_low_temp': 5.225e-2,
    'volt_ref': 1.812e-3
}

def error_codes(lect):
  error_dict = {
    "0001": "UART communication error",
    "0002": "Timeout error",
    "0003": "Syntax error",
    "0004": "Checksum error",
    "0005": "Command error",
    "0006": "Parameter error",
    "0007": "Parameter size error"}
  error_no = lect.split('hxx')[-1].split('\x03')[0]
  return error_dict.get(error_no)

def hex_to_dec(hexa):
    return int(hexa, 16)

def status_dict(hex_string):

  '''Function for translating hexadecimal messages from the Hamamatsu Power
  Supply to the error description as detailed in the "Command Reference"
  operation manual.

  parameters:
    hex_string: Hexadecimal string of four bytes.

  returns: Dictionary of errors.'''

  if len(hex_string)>4:
    return 'Error: Hex value longer than 4 bytes.'
  else:
    hex_to_bin = bin(int(hex_string, 16))[2:].zfill(8)
    hvo_status_b = str(hex_to_bin)[-1]
    over_curr_status_b = str(hex_to_bin)[-2]
    curr_value_status_b = str(hex_to_bin)[-3]
    mppc_temp_sensor_status_3_b = str(hex_to_bin)[-4]
    mppc_temp_sensor_status_4_b = str(hex_to_bin)[-5]
    temp_corr_status_b = str(hex_to_bin)[-7]
    if hvo_status_b=='1':
      hvo_status = 'ON'
    else:
      hvo_status = 'OFF'
    if over_curr_status_b=='1':
      over_curr_status = 'Yes'
    else:
      over_curr_status = 'No'
    if curr_value_status_b=='1':
      curr_value_status = 'Outside specifications'
    else:
      curr_value_status = 'Within specifications'
    if mppc_temp_sensor_status_3_b=='1':
      mppc_temp_sensor_status_3 = 'Connect'
    else:
      mppc_temp_sensor_status_3 = 'Disconnect'
    if mppc_temp_sensor_status_4_b=='1':
      mppc_temp_sensor_status_4 = 'Outside specifications'
    else:
      mppc_temp_sensor_status_4 = 'Within specifications'
    if temp_corr_status_b=='1':
      temp_corr_status = 'Effectiveness'
    else:
      temp_corr_status = 'Invalid'

    return {'hvo_status': hvo_status, 'over_curr_status': over_curr_status, 'curr_value_status': curr_value_status,
          'mppc_temp_sensor_status_3': mppc_temp_sensor_status_3, 'mppc_temp_sensor_status_4': mppc_temp_sensor_status_4,
          'temp_corr_status': temp_corr_status}

def poling(ser):
    '''Gets the actual measurements of the Hamamatsu C11204-01 power supply.
    returns: status (dict), output voltage setting (V), output voltage monitor (V), output current monitor (A) and the MPPC temperature monitor (°C).
    '''
    send_command(ser,'HPO')
    reading = read_from_source(ser)
    lect_pol = reading.split('hpo')[-1].split('\x03')[0]
    list_coefs = [lect_pol[i:i+4] for i in range(0, len(lect_pol), 4)]
    status = status_dict(list_coefs[0])
    out_volt_sett = list_coefs[1]
    out_volt_mon = list_coefs[2]
    out_curr_mon = list_coefs[3]
    MPPC_temp_mon = list_coefs[4]
    if 'hpo' in reading:
        out_volt_sett_f = int(out_volt_sett, 16) * dict_conv['volt_ref']
        out_volt_mon_f = int(out_volt_mon, 16) * dict_conv['out_volt_mon']
        out_curr_mon_f = int(out_curr_mon, 16) * dict_conv['out_curr_mon']

        if status['mppc_temp_sensor_status_3'] == 'Disconnect' or hex_to_dec(MPPC_temp_mon)*dict_conv['temp_conv_1']-dict_conv['temp_conv_2'] < -100:
            MPPC_temp_mon_f = 'Sensor disconnected'
        else:
            MPPC_temp_mon_f = int(MPPC_temp_mon, 16) * dict_conv['temp_conv_1']-dict_conv['temp_conv_2']
        return status, out_volt_sett_f, out_volt_mon_f, out_curr_mon_f, MPPC_temp_mon_f
    else:
        return f'Error: {error_codes(reading)}.'

def set_temperature_factor(ser,secondary_coefs_high, secondary_coefs_low, primary_coefs_high, primary_coefs_low, ref_volt, ref_temp):
    '''Sets the secondly coefficients, primary coefficients, reference voltage (V) and reference temperature (°C).

    parameters:
        secondary_coefs_high: float.
        secondary_coefs_low: float.
        primary_coefs_high: float.
        primary_coefs_low: float.
        ref_volt: reference voltage in Volts, float.
        ref_temp: reference temperature in Celsius, float.

    returns: 'OK' if succesful.
    '''
    send_command(ser,'HST', secondary_coefs_high, secondary_coefs_low, primary_coefs_high, primary_coefs_low, ref_volt, ref_temp)
    reading = read_from_source(ser)
    temp_factor = reading.split('HST')[-1].split('\x03')[0]
    if 'hst' in reading:
        secondary_coefs_high_t = int(secondary_coefs_high/dict_conv['sec_high_temp'])*dict_conv['sec_high_temp']
        secondary_coefs_low_t = int(secondary_coefs_low/dict_conv['sec_low_temp'])*dict_conv['sec_low_temp']
        primary_coefs_high_t = int(primary_coefs_high/dict_conv['prim_high_temp'])*dict_conv['prim_high_temp']
        primary_coefs_low_t = int(primary_coefs_low/dict_conv['prim_low_temp'])*dict_conv['prim_low_temp']
        ref_volt_t = int(ref_volt/1.812e-3)*dict_conv['volt_ref']
        ref_temp_t = int((ref_temp*-5.5e-3+1.035)/1.907e-5)*dict_conv['temp_conv_1']-dict_conv['temp_conv_2']
        return f'OK. Parameters setted: {secondary_coefs_high_t}, {secondary_coefs_low_t}, {primary_coefs_high_t}, {primary_coefs_low_t}, {ref_volt_t}, {ref_temp_t}'
    else:
        return f'Error: {error_codes(reading)}.'

def read_temperature_factor(ser):
    '''Returns the secondly coefficients (decimal value), primary coefficients (decimal value), reference voltage (V) and reference temperature (°C).'''
    send_command(ser,'HRT')
    reading = read_from_source(ser)
    coefs = reading.split('\x03')[0].split('hrt')[-1]
    list_coefs = [coefs[i:i+4] for i in range(0, len(coefs), 4)]
    secondary_coefs_high = list_coefs[0]
    secondary_coefs_low = list_coefs[1]
    primary_coefs_high = list_coefs[2]
    primary_coefs_low = list_coefs[3]
    ref_volt = list_coefs[4]
    ref_temp = list_coefs[5]
    if 'hrt' in reading:
        secondary_coefs_high_f = hex_to_dec(secondary_coefs_high)*dict_conv['sec_high_temp']
        secondary_coefs_low_f = hex_to_dec(secondary_coefs_low)*dict_conv['sec_low_temp']
        primary_coefs_high_f = hex_to_dec(primary_coefs_high)*dict_conv['prim_high_temp']
        primary_coefs_low_f = hex_to_dec(primary_coefs_low)*dict_conv['prim_low_temp']
        ref_volt_f = hex_to_dec(ref_volt) * dict_conv['volt_ref']
        ref_temp_f = hex_to_dec(ref_temp) * dict_conv['temp_conv_1']-dict_conv['temp_conv_2']
        return secondary_coefs_high_f, secondary_coefs_low_f, primary_coefs_high_f, primary_coefs_low_f, ref_volt_f, ref_temp_f
    else:
        return f'Error: {error_codes(reading)}.'


def turn_on(ser):
    send_command(ser,'HON')
    reading = read_from_source(ser)
    output_voltage = reading.split('hon')[-1].split('\x03')[0]
    if 'hon' in reading:
        return output_voltage
    else:
        return f'Error: {error_codes(reading)}.'


def turn_off(ser):
    '''Turns off the power supply (activates the 'stand by, low power' mode).'''
    send_command(ser,'HOF')
    reading = read_from_source(ser)
    output = reading.split('hof')[-1].split('\x03')[0]
    if output == '':
        return "Power turned off."
    else:
        return f'Error: {error_codes(reading)}.'

def switch_tcm(ser,mode):
    '''Switches the temperature compensation mode.

    parameters:
        mode: 0 or 1. Read the manual for more information.

    returns: 'OK' if succesful.
    '''
    send_command('HCM', mode=mode)
    reading = read_from_source(ser)
    output = reading.split('hcm')[-1].split('\x03')[0]
    if 'hcm' in reading:
        return 'OK'
    else:
        return f'Error: {error_codes(reading)}.'

def reset_ps(ser):
    '''Resets the power supply.'''
    send_command(ser,'HRE')
    reading = read_from_source(ser)
    output = reading.split('hre')[-1].split('\x03')[0]
    if 'hre' in reading:
        return output
    else:
        return f'Error: {error_codes(reading)}.'


def set_voltage(ser,v_ref):
    '''Temporarily sets the power supply voltage. The setting is lost when turned off.
    parameters:
        v_ref: reference voltage in Volts, float.
    '''
    if (v_ref < 50) or (v_ref > 90):
        return 'Reference voltage out of operating limits.'
    else:
        v_ref_int = int(v_ref / 1.812e-3)
        send_command(ser,'HBV', v_ref_int)
        reading = read_from_source(ser)
        set_voltage = reading.split('hbv')[-1].split('\x03')[0]
        if 'hbv' in reading:
            return f'Successfully set reference voltage to {v_ref_int * 1.812e-3}V.'
        else:
            return f'Error: {error_codes(reading)}.'


def get_temp_aq_mppc(ser):
    '''Gets the temperature of the MPPC module.

    returns: MPPC temperature in Celsius degrees, float.
    '''
    send_command(ser,'HGT')
    reading = read_from_source(ser)
    temp_mppc = reading.split('hgt')[-1].split('\x03')[0]
    if 'hgt' in reading:
        dec = hex_to_dec(temp_mppc)
        float_temp = dec * dict_conv['temp_conv_1']-dict_conv['temp_conv_2']
        return f'MPPC Temperature: {float_temp}°C'
    else:
        return f'Error: {error_codes(reading)}.'

def get_voltage(ser):
    send_command(ser,'HGV')
    reading = read_from_source(ser)
    output_voltage = reading.split('hgv')[-1].split('\x03')[0]
    if 'hgv' in reading:
        dec = hex_to_dec(output_voltage)
        float_voltage = dec * dict_conv['out_volt_mon']
        return float_voltage
    else:
        return f'Error: {error_codes(reading)}.'

def get_current(ser):
    send_command(ser,'HGC')
    reading = read_from_source(ser)
    output_current = reading.split('hgc')[-1].split('\x03')[0]
    if 'hgc' in reading:
        dec = hex_to_dec(output_current)
        float_current = dec * dict_conv['out_volt_mon']
        return float_current
    else:
        return f'Error: {error_codes(reading)}.'




