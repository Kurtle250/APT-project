import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class apt_data(Model):
    __keyspace__ = "APT-data"
    __table_name__ = "NOAA-X"

    aptSchema = {
        "id": columns.UUID(primary_key=True, default=uuid.uuid4()),
        "utc_time": columns.Text(),
        "location": columns.Text(),
        "description": columns.Text(),
        "wave_location": columns.Text(),
        "image_location": columns.Text()
    }

    def __init__(self, date: str, loc: str, desc: str, wav_loc: str, img_loc: str):
        self.aptSchema["utc_time"] = date
        self.aptSchema["location"] = loc
        self.aptSchema["description"] = desc
        self.aptSchema["wave_location"] = wav_loc
        self.aptSchema["image_location"] = img_loc
