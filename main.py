
from apt_decoder import apt_decoder


def main():
    #/home/kurt/downloads/jp1odj-air.proxy.kiwisdr.com_2023-04-07T03_19_00Z_137912.00_iq.wav
    app = apt_decoder("/home/kurt/Downloads/sample.wav")
    #app.display_plot()
    # testing CICD
    app.display_image()

if __name__ == "__main__":

    main()