import RPi.GPIO as GPIO
import time

'''
DATA SHEET: http://www.ti.com/lit/ds/symlink/adc0832-n.pdf
GPIO BCM: I/O (5/6) to GPIO 16, CS (1) to GPIO 21, CLK (7) TO GPIO 20
'''

class adc0832():
    def __init__(self):
        self.ADC_CS = 21
        self.ADC_CLK = 20
        self.ADC_DIO = 16
        self.setup()

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)    #Number GPIOs by its physical location
        GPIO.setup(self.ADC_CS, GPIO.OUT)
        GPIO.setup(self.ADC_CLK, GPIO.OUT)

    def destroy(self):
        GPIO.cleanup()

    def read_result(self,prct = False):
        GPIO.setup(self.ADC_DIO, GPIO.OUT)
        GPIO.output(self.ADC_CS, 0)

        GPIO.output(self.ADC_CLK, 0)
        GPIO.output(self.ADC_DIO, 1);  time.sleep(0.000002)
        GPIO.output(self.ADC_CLK, 1);  time.sleep(0.000002)
        GPIO.output(self.ADC_CLK, 0)

        GPIO.output(self.ADC_DIO, 1);  time.sleep(0.000002)
        GPIO.output(self.ADC_CLK, 1);  time.sleep(0.000002)
        GPIO.output(self.ADC_CLK, 0)

        GPIO.output(self.ADC_DIO, 0);  time.sleep(0.000002)

        GPIO.output(self.ADC_CLK, 1)
        GPIO.output(self.ADC_DIO, 1);  time.sleep(0.000002)
        GPIO.output(self.ADC_CLK, 0)
        GPIO.output(self.ADC_DIO, 1);  time.sleep(0.000002)

        dat1 = 0
        for i in range(0, 8):
            GPIO.output(self.ADC_CLK, 1);  time.sleep(0.000002)
            GPIO.output(self.ADC_CLK, 0);  time.sleep(0.000002)
            GPIO.setup(self.ADC_DIO, GPIO.IN)
            dat1 = dat1 << 1 | GPIO.input(self.ADC_DIO)  # or ?

        dat2 = 0
        for i in range(0, 8):
            dat2 = dat2 | GPIO.input(self.ADC_DIO) << i
            GPIO.output(self.ADC_CLK, 1);  time.sleep(0.000002)
            GPIO.output(self.ADC_CLK, 0);  time.sleep(0.000002)

        GPIO.output(self.ADC_CS, 1)
        GPIO.setup(self.ADC_DIO, GPIO.OUT)

        if dat1 == dat2:
            if prct == True:
                res = (dat1/255)*100
            else:
                res = dat1
            return res
        else:
            return 0
