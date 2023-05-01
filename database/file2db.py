#!/usr/bin/python

# /database/db/file_to_database.py

import json
import subprocess
import logging
from database.db.cassandra_cluster import CassandraCluster
from utils.setup_logging import setup_logging

LOGGING = " <file_to_database.py> :: "

""" Example configurations to run this file """
APT_DATA = {
    "model": 'apt_data',
    "filepath": 'data/images/',
    "mode_type": 'json'
}


class FileToDatabase:
    """
    Descriptor: loads a file (csv, json) into the database
    """

    def __init__(self, file_path: str = None, input_mode: str = None, database_write_model: str = None):
        valid_modes = ("csv", "json")
        if input_mode not in valid_modes or input_mode is None:
            err_msg = f"{LOGGING} Invalid mode. Select from {valid_modes}"
            raise Exception(err_msg)
        self.mode = input_mode
        self.file_path = str(file_path)
        self.model = database_write_model
        self.connection = CassandraCluster()
        self.session = self.connection.connect()
        self.database_write = self.load_database_model()

        self.column_list = None
        self.file_length = int(subprocess.check_output(
            f"ls -l {self.file_path} | grep ^- | wc -l", shell=True, encoding='UTF-8'))  # number of files in path

    def load_database_model(self):
        if self.model == 'apt_data':
            from database.db.db_writer import write_aptdata as database_write
        else:
            err_msg = f"{LOGGING} Database model not found for >> {self.model}"
            logging.error(err_msg)
            raise Exception(err_msg)
        logging.info(f"{LOGGING} Loading database write model: {database_write}")
        return database_write

    def load_json_file(self):
        """
        This function loads from {self.filepath}/{naming_schema}{counter}.json
        # expects files to be named nvidia_eo_1.json, nvidia_eo_2.json, nvidia_eo_100.json
        Parameters
        ----------
        Returns
        -------
        data: a python dictionary
        """
        filename = f"{self.file_path}/{self.model}.json"

        with open(filename) as f:
            data = json.load(f)
        if not any(data):
            error_message = (f"{LOGGING} file not there ::ERROR::\n*****")
            logging.error(error_message)
            logging.info(f"{LOGGING} Json file contains nothing :: data ({data})")
            raise Exception(error_message)
        return data

    def file_to_database(self) -> None:
        """
        Parameters
        ----------
        -------
        """
        logging.info(f"{LOGGING} entered file_to_database()")
        logging.info(f"{LOGGING} LENGTH :: {self.file_length}")

        data = self.load_json_file()

        try:
            print(f"Data input: \n{data}")
            self.database_write(data)

        except Exception as err_msg:
            logging.error(
                f"{LOGGING}file_to_database() :: ERROR ::  {err_msg}"
            )
        raise Exception(err_msg)


if __name__ == "__main__":
    setup_logging()
    logging.getLogger('cassandra').setLevel(logging.WARNING)

    import sys

    args = None

    if len(sys.argv) != 1:
        logging.warning(f"{LOGGING} usage: sudo make database_load number_rows=100")
        logging.warning(f"{LOGGING} usage: python3 {sys.argv[0]} <modality> <number_rows>")
        logging.warning(f"{LOGGING} View configs: {sys.argv[0]}")
        exit()

    else:
        print(f"Dataset not configured, check configs: {sys.argv[0]}")

    logging.info(f"{LOGGING} args >> {args}")

    logging.info("\n\n\n************************************ STARTING ************************************\n")
    driver = FileToDatabase(
        file_path=APT_DATA['filepath'], input_mode=APT_DATA['mode_type'], database_write_model=APT_DATA['model'])
    driver.file_to_database()
    logging.info("\n\n\n************************************ SUCCESS ************************************\n")
    logging.info(
        ">>>>>>>>>>>\n\nView changes to database with the following:\n"
        "sudo make database_login\n\n"
        "cassandra@cqlsh> select count(*) from sensor.ds_eo;\n"
        "cassandra@cqlsh> select count(*) from sensor.ds_ir;\n"
        "cassandra@cqlsh> select count(*) from fusion.features;\n\n"
    )
