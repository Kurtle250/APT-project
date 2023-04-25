class apt_data():
    aptSchema = {
        "id": str(),
        "utc_time": str(10),
        "location": list(),
        "description": str(1028),
        "wave_location": str(128),
        "image_location": str(128)
    }

    def __init__(self, db_id: str, date: str, loc: list, desc: str, wav_loc: str, img_loc: str):
        self.aptSchema["id"] = db_id
        self.aptSchema["utc_time"] = date
        self.aptSchema["location"] = loc
        self.aptSchema["description"] = desc
        self.aptSchema["wave_location"] = wav_loc
        self.aptSchema["image_location"] = img_loc
