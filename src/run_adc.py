from adc import adc0832
from time import sleep

if __name__ == '__main__':
    try:
        adc = adc0832()
        while True:
            print(adc.read_result())
            sleep(0.5)
    except KeyboardInterrupt:
        adc.destroy()