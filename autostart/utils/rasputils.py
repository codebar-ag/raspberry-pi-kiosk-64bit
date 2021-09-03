
"""

UTILITY FUNCTIONS
for the Raspberry Pi & Raspberry Pi OS

"""


import psutil
import subprocess


def get_mac(interface='eth0'):
  """
  Return the MAC ADRESS of the Raspberry Pi
  via psutil. and given interface.
  Via psutil and NICS

  The network interface card (NIC) or network card is the hardware device most essential to establishing communication between computers

  """

  nics = psutil.net_if_addrs().get(interface) # None if interface not in nics.
  if nics:
    for interface in nics:
      if interface.family == 17:
          return interface.address
  else: # if interface was not found return empty adress
    return '00:00:00:00:00:00'



def get_temperature():
  """get the temperatur of Raspberry pi 

  Note: This will work only on Raspberry pi hardware.
  Note: Only tested on Raspberry Pi 4B 8GB

  vcgencmd meure_temp returns a bytes-like object: b"temp=65.2'C\n" 
  will be decoded and split to return a float (eg. 65.2)
  will Return None on any Exception reading from subprocess

  """
  try:
    measured_temp = subprocess.check_output(["vcgencmd","measure_temp"])
    return float(measured_temp.decode().split('=')[1][:-3])
  except Exception:
    print(f'ERROR READING PIE TEMPERATURE VIA vcgencmd')
    return None

