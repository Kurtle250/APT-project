import dataclasses
import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.columns import Text, UUID
from cassandra.cqlengine.models import Model

class AptData(Model):
    __keyspace__ = "decoder"
    __table_name__ = "capture"
    id = columns.UUID(primary_key=True, default=uuid.uuid4())

    utc_time = columns.Text()
    location = columns.Text()
    description = columns.Text()
    wave_location = columns.Text()
    image_location = columns.Text()

    #
    # def __init__(self, u_uid, date: Text | UUID, loc: Text | UUID, desc: Text | UUID, wav_loc: Text | UUID,
    #              img_loc: Text | UUID, **values):
    #     super().__init__(**values)
    #     self.aptSchema["id"] = u_uid
    #     self.aptSchema["utc_time"] = date
    #     self.aptSchema["location"] = loc
    #     self.aptSchema["description"] = desc
    #     self.aptSchema["wave_location"] = wav_loc
    #     self.aptSchema["image_location"] = img_loc
