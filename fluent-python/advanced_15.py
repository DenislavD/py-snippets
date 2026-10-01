# Fluent Python: Metaprogramming II - Dynamic attributes and properties

# Reorganize the data structure to allow object access via its serial
import inspect
import json
from functools import cache

JSON_PATH = 'z_osconfeed.json'

class Record:
    "This class works by loading the feed into __index and querying it from there"
    "Only one instance is needed - food for thought for clasmethods refactor"
    __index = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs) # common shortcut to load a bunch of items in instance
        """ Differences to FrozenJSON:
        a) FrozenJSON is recursively building a new object in memory each time, no need now
        b) No .keys() or .items() attribute access here - we don't need it
        """

    def __repr__(self):
        return f'<{self.__class__.__name__} serial={self.serial!r}>'

    @staticmethod
    def fetch(key):
        if Record.__index is None:
            Record.__index = load()
        return Record.__index[key]


class Event(Record):
    def __repr__(self):
        try:
            return f'<{self.__class__.__name__} {self.name!r}>'
        except AttributeError:
            return super().__repr__()

    @property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return self.__class__.fetch(key) # not using self.fetch here to avoid attribute shadowing

    # this property has the same name as an attribute on the Record, overrides it
    @property
    @cache # this must be the order
    def speakers(self):
        speakers_serials = self.__dict__['speakers'] # avoids recursive __getattribute__(self, 'speakers')
        fetch = self.__class__.fetch
        return [fetch(f'speaker.{key}') for key in speakers_serials]


def load(path=JSON_PATH) -> dict[str, Record]:
    "Builds a flat dict of items like event.35912 , speaker.145, venue.23567 and so on."
    records = {}
    with open(path) as fh:
        raw_feed = json.load(fh)

    for collection, raw_records in raw_feed['Schedule'].items():
        record_type = collection[:-1] # events -> event
        cls_name = record_type.capitalize()
        cls = globals().get(cls_name, Record) # if not found, return Record (can get Event)
        if inspect.isclass(cls) and issubclass(cls, Record):
            factory = cls
        else:
            factory = Record # not sure in which case this is needed, maybe just a factory example

        for raw_record in raw_records:
            key = f'{record_type}.{raw_record["serial"]}' # like event.35912
            records[key] = factory(**raw_record)

    return records

event = Record.fetch('event.33950')
print(event)    
print(event.venue, '|', event.venue.name, '| Serial:', event.venue_serial)    

print(event.speakers[0].name) # Anna Martelli Ravenscroft
