# /database/db/database_reader.py
from database.db.db_apt_Schema import AptData


def read_aptdata():
    values = AptData.objects()
    return values

