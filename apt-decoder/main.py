
from aptDecoder import AptDecoder
from aptManager import aptManager
from database.file2db import APT_DATA, FileToDatabase
def main():
    #/home/kurt/downloads/jp1odj-air.proxy.kiwisdr.com_2023-04-07T03_19_00Z_137912.00_iq.wav
    path = '../data/signals/sample16-1.wav'
    app = AptDecoder(path)

    #app = aptManager("../data/signals/*").createProcessPool()
    #driver = FileToDatabase(file_path=APT_DATA['filepath'],
                            # input_mode=APT_DATA['mode_type'],
                            # database_write_model=APT_DATA['model'])
    #driver.file_to_database()
if __name__ == "__main__":
    main()