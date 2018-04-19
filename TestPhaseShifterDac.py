# coding=utf-8
# ---------------------------------------------------------------------------------
# -- Project Name      : SPI DAC test code                                       --
# -- Design Engineer   : Murteza ÇALIŞKAN                                        --
# -- Date              : 19.04.2018                                              --
# -- Short Description : This is code written for test PhaseShifterDac.py        --
# ---------------------------------------------------------------------------------

from PhaseShifterDac import SingleDac

Resolution = 2 ** 12  # 12#  bits for the MCP 4921

try:
    while True:
        value = input('Enter an output level from 0-4095 : ')
        V_Ref = input('Enter a voltage referance: ')
        ChipSelect = input('Enter an chip select from 1-5 : ')
        Sleeptime = input('Enter a sleep time: ')
        print("Output level should be : {:f} mV".format(value * V_Ref / Resolution))
        SingleDac(value, ChipSelect, V_Ref, False, Sleeptime)

except (KeyboardInterrupt, Exception) as e:
    print(e)
    print("Closing SPI channel")
