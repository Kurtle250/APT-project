
from aptDecoder import AptDecoder
from aptManager import aptManager

def main():
    #/home/kurt/downloads/jp1odj-air.proxy.kiwisdr.com_2023-04-07T03_19_00Z_137912.00_iq.wav
    path = "data/signals/sample16-0.wav"
    app = AptDecoder(path)

    #app = aptManager("data/signals/*").createProcessPool()

if __name__ == "__main__":
    main()