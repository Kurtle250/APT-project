from aptDecoder import AptDecoder
from aptManager import aptManager

def main():
    #/home/kurt/downloads/jp1odj-air.proxy.kiwisdr.com_2023-04-07T03_19_00Z_137912.00_iq.wav
    #app = AptDecoder("data/signals/sample16-2.wav")

    app = aptManager("data/signals/*").createProcessPool()

if __name__ == "__main__":
    main()