# /database/db/database_writer.py
import uuid
from database.db.aptDbSchema import apt_data


def write_apt(data):
    data_write = apt_data.create(
        id=uuid.uuid4(),
        date=str(data['date']),
        loc=str(data['loc']),
        desc=str(data['desc']),
        wav_loc=str(data['wav_loc']),
        img_loc=str(data['img_loc'])
    )
    return data_write
