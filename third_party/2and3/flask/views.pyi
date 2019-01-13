# Stubs for flask.views (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from ._compat import with_metaclass
from .globals import request
from typing import Any

http_method_funcs: Any

class View:
    methods: Any = ...
    provide_automatic_options: Any = ...
    decorators: Any = ...
    def dispatch_request(self) -> None: ...
    @classmethod
    def as_view(cls, name: Any, *class_args: Any, **class_kwargs: Any): ...

class MethodViewType(type):
    def __init__(cls, name: Any, bases: Any, d: Any) -> None: ...

class MethodView:
    def dispatch_request(self, *args: Any, **kwargs: Any): ...
