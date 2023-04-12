from queue import Queue
from glob import glob
import concurrent.futures as cf
from aptDecoder import AptDecoder


class aptManager(object):
    working_dir = None
    file_list = list()
    def __init__(self, w_dir):
        self.working_dir = w_dir
        for file in glob(self.working_dir):
            self.file_list.append(file)

    def createProcessPool(self) -> None:
        """
        Function for creating process pool for executing worker for file of images in working directory
        :return:
        """
        with cf.ProcessPoolExecutor(3) as executor:
            executor.map(AptDecoder, self.file_list)
