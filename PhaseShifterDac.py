# coding=utf-8
# ---------------------------------------------------------------------------------
# -- Project Name      : SPI DAC                                                 --
# -- Design Engineer   : Murteza ÇALIŞKAN                                        --
# -- Date              : 19.04.2018                                              --
# -- Short Description : This is code written for the SPI communication between  --
# --                     DAC(MCP4921) and Beaglebone. The DAC is used for the    --
# --                     control five phase shifter circuit.                     --
# ---------------------------------------------------------------------------------


import spidev
from time import sleep
import Adafruit_BBIO.GPIO as GPIO

CS1 = "P8_45"
CS2 = "P8_46"
CS3 = "P8_43"
CS4 = "P8_44"
CS5 = "P8_42"

GPIO.setup(CS1, GPIO.OUT)
GPIO.setup(CS2, GPIO.OUT)
GPIO.setup(CS3, GPIO.OUT)
GPIO.setup(CS4, GPIO.OUT)
GPIO.setup(CS5, GPIO.OUT)

spi_max_speed = 4 * 1000000  # 4 MHz
CE = 0  # CE0 or CE1, select SPI device on bus standart CE
Resolution = 2 ** 12  # 12#  bits for the MCP 4921


def SingleDac(value=1, ChipSelect=1, V_Ref=3300, DEBUG=False, sleeptime=0):
    # value must be interval between 0-4095
    # ChipSelect must be interval between 0-5
    # V_red can bu adjust depending on the connected voltage value,

    chip_select = {
        1: GPIO.output(CS1, 1),
        2: GPIO.output(CS2, 1),
        3: GPIO.output(CS3, 1),
        4: GPIO.output(CS4, 1),
        5: GPIO.output(CS5, 1)
    }
    ChipSelect = chip_select.get(ChipSelect)  # Open the chip select pin

    # setup and open an SPI channel
    spi = spidev.SpiDev()
    spi.open(1, CE)  # Using default chip select open the SPI bus,
    spi.max_speed_hz = spi_max_speed

    # lowbyte has 6 data bits
    # B7, B6, B5, B4, B3, B2, B1, B0
    # D7, D6, D5, D4, D3, D2, D1, D0,
    lowByte = value & 0b11111111

    # highbyte has control and 4 data bits
    # control bits are:
    # B7, B6,   B5,  B4,     B3,   B2,  B1,  B0
    # W  ,BUF, !GA, !SHDN,  D11,  D10,  D9,  D8
    # B7=0:write to DAC, B6=0:unbuffered, B5=1:Gain=1X, B4=1:Output is active
    highByte = ((value >> 8) & 0xff) | 0b0 << 7 | 0b0 << 6 | 0b1 << 5 | 0b1 << 4

    # write the value on the SPI bus
    spi.xfer2([highByte, lowByte])

    # write the information about low byte, high byte and the output voltage level
    # Default DEBUG value is false so depending on the default value system does not write out normally,
    if DEBUG:
        print("Highbyte = {0:12b}".format(highByte))
        print("Lowbyte =  {0:12b}".format(lowByte))
        print([highByte, lowByte])
        print("Output level should be : {:f} mV".format(value * V_Ref / Resolution))
        print("Closing SPI channel")

    GPIO.cleanup()
    # Close the SPI comminication
    spi.close()

    sleep(sleeptime)

    return 1
