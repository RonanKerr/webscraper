import datetime

class Article:
    def __init__(self, title: str, site: str, link: str, creation_time = str(datetime.datetime.now())[:-7], last_seen_at = str(datetime.datetime.now())[:-7]):
  
        self.title = title
        self.site = site
        self.link = link
        self.creation_time = creation_time
        self.last_seen_at = last_seen_at


    def to_json(self):
        return self.__dict__