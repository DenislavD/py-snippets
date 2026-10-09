# Fluent Python: Class Metaprogramming

""" NOTE:
It's beter to use lighter Python 3 features such as class decorators,
__init_subclass__, __set_name__, and the built-in dict preserving order
and leave class metaprogramming only for library development.
"""

from collections.abc import Callable
from typing import Any, NoReturn, get_type_hints

class Field:
    "Descriptor to hold and validate the instance attributes"

    def __init__(self, name: str, constructor: Callable) -> None:
        if not callable(constructor) or constructor is type(None): # class NoneType
            raise TypeError(f'{name!r} type hint must be callable')
        self.name = name
        self.storage_name = '_' + name
        self.constructor = constructor

    def __get__(self, instance, owner=None):
        if instance is None:
            return self # read from the managed class, return descr. class by convention
        return getattr(instance, self.storage_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if value is ...:
            value = self.constructor()
        else:
            try:
                value = self.constructor(value)
            except (TypeError, ValueError) as e:
                type_name = self.constructor.__name__
                msg = f'{value!r} is not compatible with {self.name}:{type_name}'
                raise TypeError(msg) from e

        # can use setattr directly now instead of going through instance.__dict__[name]
        setattr(instance, self.storage_name, value)


class CheckedMeta(type): # subclassing type -> creates classes -> Metaclass
    "Metaclass that creates user-defined classes with checked properties"

    def __new__(meta_cls, cls_name, bases, cls_dict):
        # only enhance the class if no slots. If set, assume it's the Checked base class
        if '__slots__' not in cls_dict:
            slots = []
            type_hints = cls_dict.get('__annotations__', {}) # no class yet for typing.get_type_hints
            for name, constructor in type_hints.items():
                field = Field(name, constructor)
                cls_dict[name] = field # dynamically configure descriptors
                slots.append(field.storage_name)

            cls_dict['__slots__'] = slots # populate the namespace of the class under construction

        return super().__new__(meta_cls, cls_name, bases, cls_dict)


class Checked(metaclass=CheckedMeta):
    "Users of this lib will use the Checked base class to enhance their classes like Movie"

    __slots__ = () # skip CheckedMeta.__new__ processing

    @classmethod
    def _fields(cls) -> dict[str, type]:
        return get_type_hints(cls)

    def __init__(self, **kwargs: Any) -> None:
        for name in self._fields():
            value = kwargs.pop(name, ...) # Ellipsis default
            setattr(self, name, value)
        if kwargs:
            self.__flag_unknown_attrs(*kwargs)

    def __flag_unknown_attrs(self, *names: str) -> NoReturn: # will raise error
        s = 's' if len(names) > 1 else ''
        unknown = ', '.join(f'{name!r}' for name in names)
        cls_name = repr(self.__class__.__name__)
        raise AttributeError(f'{cls_name} object has no attribute{s} {unknown}')

    def _asdict(self) -> dict[str, Any]:
        return {
            name: getattr(self, name)
            for name, attr in self.__class__.__dict__.items()
            if isinstance(attr, Field)
        }

    def __repr__(self) -> str:
        kwargs = ', '.join(f'{key}={value!r}' for key, value in self._asdict().items())
        return f'{self.__class__.__name__}({kwargs})'


# tests
class Movie(Checked):
    title: str
    year: int
    box_office: float

if __name__ == '__main__':
    movie = Movie(title='Revolver', year=2001, box_office=56.2)
    print(movie)
    movie.title = 'No Title'
    print(movie.title)

    # Checks:
    #movie.wer = 3 # 'Movie' object has no attribute 'wer' and no __dict__ for setting new attributes
    #movie.box_office = 'box what?' # 'box what?' is not compatible with year:int
    #b = Movie(title='The Accountant', year=2005) # box_office=0.0 default float constructor
    #c = Movie(peaches='Bebo', pears=2000) # 'Movie' object has no attributes 'peaches', 'pears'

# END of FLuent Python (page 951).