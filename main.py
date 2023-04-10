from aptdecoder import AptDecoder


def main():
    #/home/kurt/downloads/jp1odj-air.proxy.kiwisdr.com_2023-04-07T03_19_00Z_137912.00_iq.wav
    app = AptDecoder("data/signals/sample16.wav")
    #app.display_plot()
    app.display_image()
    app.save_image(12)

if __name__ == "__main__":
    main()