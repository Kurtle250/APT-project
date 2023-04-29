# /database/db/database_reader.py
from database.db.aptDbSchema import apt_data


def read_aptData():
    values = apt_data.objects()
    return values

