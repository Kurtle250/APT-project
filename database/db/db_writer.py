# /database/db/database_writer.py
import uuid
from database.db.db_apt_Schema import AptData


def write_aptdata(data):
    data_write = AptData.create(
        id=uuid.uuid4(),
        date=str(data['date']),
        loc=str(data['loc']),
        desc=str(data['desc']),
        wav_loc=str(data['wav_loc']),
        img_loc=str(data['img_loc'])
    )
    return data_write
