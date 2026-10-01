# Fluent Python: Metaprogramming I - Dynamic attributes

# Exploratory Data Analysis of z_osconfeed.json
import json
with open('z_osconfeed.json') as fh:
    raw_feed = json.load(fh)

data = sorted(raw_feed['Schedule'].keys())
print(data)
print('Event name:', raw_feed['Schedule']['events'][40]['name'])
# gets cumbersome, we can remodel it to use . attribute access

from collections import abc
import keyword

# read-only JSON-like object reader using attribute notation:
class FrozenJSON:
    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls) # object's __new__ will create a FrozenJSON instance
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg] # return collection of objects
        else:
            return arg # not a dict or a list, return the item as-is

    # __new__ created a FrozenJSON object istance and we are now here
    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name): # gets called for attributes that are not found by __getattribute__
        try:
            return getattr(self.__data, name) # allows feed.keys(), .values() etc.
        except AttributeError:
            print('AttributeError on', name, ', converting to FrozenJSON')
            return FrozenJSON(self.__data[name])

    def __dir__(self):
        return self.__data.keys()


# test it!
print('-' * 50)
feed = FrozenJSON(raw_feed)
event_name = feed.Schedule.events[40].name # much cooler now
print('Event name:', event_name)
print(len(feed.Schedule.speakers))
print(feed.Schedule.keys())
print('Speakers:', feed.Schedule.events[40].speakers) # Speakers: [3471, 5199]
# next step is to remodel the data structure to allow object access via its serial (ORM-like)
