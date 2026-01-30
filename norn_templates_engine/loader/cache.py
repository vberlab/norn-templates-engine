"""
    Templates cache class and functions
"""
import time
import numbers
from dataclasses import dataclass, field
from typing import Any
from itertools import zip_longest
from norn_templates_engine.loader import template_pack as tp
from norn_templates_engine.loader import errors
from norn_templates_engine.misc import int_now_ts


@dataclass(frozen=True)
class TemplateLoaderCacheObject:
    obj: tp.Template | tp.IncludePart
    created: int = field(default_factory=int_now_ts)
    ttl: int = 0

    def _validate_ttl(self, value: Any) -> int:
        """
            Check ttl value type.
            Make attempt to convert to an interger
        """
        if not isinstance(value, numbers.Number):
            raise errors.TemplateCacheTtlInvalidType(f"Ttl has invalid type {type(value)}, expected Number")
        try:
            return int(value)
        except Exception as e:
            raise errors.TemplateCacheError(f"Unable to convert ttl value to integer") from e

    def __post_init__(self):
        object.__setattr__(self, "ttl", self._validate_ttl())

    @property
    def expired(self) -> bool:
        return int(time.time()) - self.created >= self.ttl

    @property
    def cached_type(self):
        return type(self.obj)


@dataclass
class TemplateLoaderCache:
    cache_objects: list[TemplateLoaderCacheObject] = field(default_factory=list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._template_indx = list()
        self._include_indx = list()
        self._indexing()

    @property
    def cache_size(self) -> int:
        """
            Return len of cached object list
        """
        return len(self.cache_objects)

    @property
    def last_index(self) -> int:
        return self.cache_size - 1

    def _indexing(self):
        """
            Make initial template objects index
        """
        for i in range(0, len(self.cache_objects)):
            _obj = self.cache_objects[i]
            if _obj.cached_type is tp.Template:
                self._template_indx.append(i)
            elif _obj.cached_type is tp.IncludePart:
                self._include_indx.append(i)
            else:
                raise errors.TemplateCacheObjectInvalidType(
                    f"Cached object {_obj} has ivalid type {type(_obj)}, expected Template|IncludePart"
                )
        return

    @property
    def templates_index(self):
        """
            Index of templates objects
        """
        return self._template_indx

    @property
    def templates_objects(self):
        """
            List of templates objects
        """
        return list([self.cache_objects[i] for i in self.templates_index])

    @property
    def include_index(self):
        """
            Index of include parts
        """
        return self._include_indx

    @property
    def include_objects(self):
        """
            List of include objects
        """
        return list([self.cache_objects[i] for i in self.include_index])

    def _expired(self):
        """
            list of pair with expired object and his index
        """
        return list(
            [(self.cache_objects[i], i) for i in range(0, len(self.cache_objects)) if self.cache_objects[i].expired])

    @property
    def expired_index(self):
        """
            Index of expired objects
        """
        return list([indx for _, indx in self._expired()])

    @property
    def expired_objects(self):
        """
            List of expired objects
        """
        return list([obj for obj, _ in self._expired()])

    def exists(self, obj: tp.Template|tp.IncludePart|TemplateLoaderCacheObject) -> (bool, int):
        """
            Check object existing in cache
        """
        _name = None
        status = False
        indx = -1
        if isinstance(obj, (tp.Template, tp.IncludePart)):
            _name = obj.name
        elif isinstance(obj, TemplateLoaderCacheObject):
            _name = obj.obj.name
        else:
            raise errors.TemplateCacheObjectInvalidType(
                f"Cached object {obj} has ivalid type {type(obj)}, expected Template|IncludePart"
            )
        for tmpl_i, incl_i in zip_longest(self.templates_index, self.include_index, fillvalue=None):
            if tmpl_i is not None:
                if self.cache_objects[tmpl_i].obj.name == _name:
                    status = True
                    indx = tmpl_i
                    break
            if incl_i is not None:
                if self.cache_objects[incl_i].obj.name == _name:
                    status = True
                    indx = incl_i
                    break
        return status, indx

    def get_object_by_index(self, indx: int) -> TemplateLoaderCacheObject|None:
        return self.cache_objects[indx]

    def _add_to_cache(self, obj: TemplateLoaderCacheObject):
        """
            Add object to cache
        """
        pass

    def _update_cached(self, obj: TemplateLoaderCacheObject):
        """
            Update object in cache
        """
        pass

    def caching(self, obj: TemplateLoaderCacheObject) -> bool:
        """
            Wrapper method for caching object
        """
        _obj = obj
        #TODO: Develop add and update methods