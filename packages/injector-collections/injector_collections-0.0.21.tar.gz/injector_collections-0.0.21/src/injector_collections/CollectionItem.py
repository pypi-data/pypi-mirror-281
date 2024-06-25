from typing import Type, TypeVar
from collections import defaultdict

T = TypeVar('T')

class CollectionItem:
    #_items: defaultdict[Type, list[tuple[Any, Any]]] = defaultdict(list)
    _items: defaultdict[Type, list['CollectionItem']] = defaultdict(list)

    def __init__(self, collectionClass: Type, assisted: bool = False):
        self._collectionClass: Type = collectionClass
        self._assisted = assisted

    def __call__(self, classVar: Type[T]) -> Type[T]:
        #self._items[self._collectionClass].append((classVar.__name__, classVar))
        self.classVar = classVar
        self._items[self._collectionClass].append(self)

        return classVar

    @property
    def className(self):
        return self.classVar.__name__

    @property
    def classModule(self):
        return self.classVar.__module__

    @property
    def isPartial(self):
        return self._assisted

    @classmethod
    def getItems(cls) -> dict[Type, list['CollectionItem']]:
        return cls._items
