
from apt_decoder import apt_decoder


def main():
    app = apt_decoder("sample16.wav")
    #app.display_plot()
    app.display_image()

if __name__ == "__main__":

    main()