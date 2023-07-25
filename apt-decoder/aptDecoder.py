#!/usr/bin/python3

import json
from database.db.db_apt_Schema import AptData
from SignalProcessing import SignalProcessing
from ImageProcessing import ImageProcessing
class AptDecoder(AptData):
    # image parameters
    generated_img: ImageProcessing
    img_fh = str()
    json_output = None

    def __init__(self,
                 captured_signal: SignalProcessing):
        # initial Signal
        self.captured_signal = captured_signal
        # Decode Signal
        self._decode_signal()
        # Generate Image
        self.img = ImageProcessing(self.captured_signal.data, self.captured_signal.sample_rate)


    def _decode_signal(self):
        self.captured_signal.hilbert()
        self.captured_signal.resample()
        self.captured_signal.quantize_signal()



    def display_image(self) -> None:
        """
        Display's image
        :return: None
        """
        self.img.show()

    def _save_image(self) -> None:
        """
        Save matplot figure as png
        :return: None
        """
        self.img_fh = "../data/images/" + self.wav_fh.split('/')[2].split('.')[0] + ".png"
        print(self.img_fh)
        self.img.save(self.img_fh)

    def generate_json_file(self):
        """
        Generating json output, which will be used for passing to db
        :return: Json formatted apt schema for passing to db
        """
        aptSchema = {
            'id': "2",
            'utc_time': "HHMMSS",
            'location': ["XXX","XXX","XXX"],
            'description':  "",
            'wave_location':   self.wav_fh,
            'image_location':  self.img_fh
        }
        with open("../data/tmp.json", "w") as fh:
            fh.write(json.dumps(aptSchema))
