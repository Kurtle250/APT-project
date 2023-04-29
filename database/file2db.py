#!/usr/bin/python

# /database/db/file_to_database.py

import json
import pandas as pd
import subprocess
import logging
from database.db.cassandra_cluster import CassandraCluster

LOGGING = " <file_to_database.py> :: "

TEN_ROWS = {
    "model": None,
    "filepath": None,
    "num_frames": 9,
    "start": 0,
    "multiplier": 1,
    "mode_type": 'csv'
}

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
            from database.db.db_writer import write_apt as database_write
        else:
            err_msg = f"{LOGGING} Database model not found for >> {self.model}"
            logging.error(err_msg)
            raise Exception(err_msg)
        logging.info(f"{LOGGING} Loading database write model: {database_write}")
        return database_write


    def load_numbered_json_file(self, counter: int = 0) -> dict:
        """
        This function loads from {self.filepath}/{naming_schema}{counter}.json
        # expects files to be named nvidia_eo_1.json, nvidia_eo_2.json, nvidia_eo_100.json
        Parameters
        ----------
        counter: external loop counter that is used to load a numbered file.
        Returns
        -------
        data: a python dictionary
        """
        filename = f"{self.file_path}/{self.model}_{counter}.json"

        with open(filename) as f:
            data = json.load(f)
        if counter == 0:
            logging.info(f"{LOGGING} Loaded 1st JSON file from folder ({self.file_path})")
        if not any(data):
            error_message = (f"{LOGGING} file_to_kafka() ::ERROR::\n***** cannot find frame number `{counter}` *****\n")
            logging.error(error_message)
            logging.info(f"{LOGGING} Json file contains nothing :: data ({data}) :: counter ({counter})")
            raise Exception(error_message)
        return data

    def file_to_database(self, starting_frame: int = 0, nth_frame: int = 1, number_of_frames_to_send: int = 1) -> None:
        """
        Parameters
        ----------
        number_of_frames_to_send: number of frames that you wish to send.
        starting_frame: will start reading rows based on number in 'frame' column
        nth_frame: send every nth frame (3rd => 0, skip, skip, 3, skip, skip, 6 ...
        Returns
        -------
        """
        logging.info(f"{LOGGING} entered file_to_database()")
        logging.info(f"{LOGGING} LENGTH :: {self.file_length}")
        if starting_frame < 0:
            err_msg = f"{LOGGING} must have a starting frame greater than zero"
            logging.error(err_msg)
            raise Exception(err_msg)

        if number_of_frames_to_send > self.file_length:
            number_of_frames_to_send = self.file_length
            logging.info(
                f"{LOGGING} file_to_database() detected that csv length ({self.file_length})\n"
                f"Setting maximum read size to complete task."
            )
        if nth_frame <= 0:
            logging.error(f"{LOGGING} file_to_database() detected arg `nth_frame=0`. Setting to 1!")
            nth_frame = 1
        end_with_offset = number_of_frames_to_send * nth_frame + (starting_frame - nth_frame)

        if starting_frame < 0:
            logging.error(f"{LOGGING} file_to_database() detected arg `start < 0`. Setting to 0!")
            start = 0  # noqa F841
        if end_with_offset < starting_frame:
            error_message = f"{LOGGING} ERROR :: check folder/file frames and configure self.produce_number accordingly"
            logging.error(f"frame_end_including_offset {end_with_offset} :: starting_frame {starting_frame}")
            logging.error(error_message)
            raise Exception(error_message)

        counter = starting_frame

        logging.debug(
            f"{LOGGING} {self.mode} DUMP to database, "
            f"sending ({number_of_frames_to_send}) frames, "
            f"start ({starting_frame}), "
            f"sending every nth frame ({nth_frame}), "
            f"ending before or on ({end_with_offset})"
        )
        send_number = 0

        while counter <= end_with_offset:
            # load json file
            if self.mode == "csv":
                data = self.read_csv_line(counter)
            elif self.mode == "json":
                data = self.load_numbered_json_file(counter)

            # logging.info(f"{LOGGING}: write number ({counter})")
            if send_number == 1:
                # logging.info(f"{LOGGING}: type ({type(data)}) >> json data\n\n{data}\n")
                pass
            send_number += 1
            counter += nth_frame

            try:
                # ts_datetime = StringToTimeConverter(data["timestamp"], separator="space")
                # ts_epoch = StringToTimeConverter(data["timestamp"], separator="space", mode="epoch")
                # data["timestamp"] = ts_datetime.converted_ts
                # data["ts_epoch"] = ts_epoch.converted_ts
                print(f"Data input: \n{data}")
                data["packet_count"] = send_number
                # data["frame"] = int(data["frame"])
                print(data)
                self.database_write(data)

            except Exception as err_msg:
                logging.error(
                    f"{LOGGING}file_to_database() :: ERROR :: index({counter}) ::  {err_msg}"
                )
                raise Exception(err_msg)


if __name__ == "__main__":
    setup_logging()
    logging.getLogger('cassandra').setLevel(logging.WARNING)

    import sys
    args = None

    if len(sys.argv) != 3:
        logging.warning(f"{LOGGING} usage: sudo make database_load number_rows=100")
        logging.warning(f"{LOGGING} usage: python3 {sys.argv[0]} <modality> <number_rows>")
        logging.warning(f"{LOGGING} View configs: {sys.argv[0]}")
        exit()

    if sys.argv[1].lower() == 'ds_eo':
        args = TEN_ROWS
        args["model"] = 'ds_eo'
        args['filepath'] = '/data/test/lav_eo_klv_6293_8991_final_target.csv'
        args['num_frames'] = int(sys.argv[2])
    elif sys.argv[1].lower() == 'ds_ir':
        args = TEN_ROWS
        args["model"] = 'ds_ir'
        args['filepath'] = '/data/test/lav_ir_klv_6293_8991_final_target.csv'
        args['num_frames'] = int(sys.argv[2])
    elif sys.argv[1].lower() == 'fusion':
        args = TEN_ROWS
        args["model"] = 'fusion'
        args['filepath'] = '/data/results/deepstream_fusion_results_eo_ir.csv'
        args['num_frames'] = int(sys.argv[2])

    else:
        print(f"Dataset not configured, check configs: {sys.argv[0]}")

    logging.info(f"{LOGGING} args >> {args}")

    logging.info("\n\n\n************************************ STARTING ************************************\n")
    driver = FileToDatabase(
        file_path=args['filepath'], input_mode=args['mode_type'], database_write_model=args['model'])
    driver.file_to_database(
        starting_frame=args['start'], nth_frame=args['multiplier'], number_of_frames_to_send=args['num_frames'])

    logging.info("\n\n\n************************************ SUCCESS ************************************\n")
    logging.info(
        ">>>>>>>>>>>\n\nView changes to database with the following:\n"
        "sudo make database_login\n\n"
        "cassandra@cqlsh> select count(*) from sensor.ds_eo;\n"
        "cassandra@cqlsh> select count(*) from sensor.ds_ir;\n"
        "cassandra@cqlsh> select count(*) from fusion.features;\n\n"
    )